require 'rubygems'
require 'json'

require 'dataset/element'
require 'dataset/site'
require 'dataset/artifact'
require 'dataset/member'
require 'dataset/relationship'
require 'dataset/timestamped_relationship'
require 'dataset/weighted_relationship'
require 'dataset/weighted_network'
require 'dataset/node_type'
require 'dataset/detailed_network'

class EdgerydersDataset
  
  attr_accessor :site, :timed_relationships, :artifacts_map, :weighted_network, :detailed_network
  
  def initialize args
    @site = Site.new

    jusers = JSON.parse args[:json_users]
    jusers["users"].each do |m|
      member = Member.new(m["user"])
      @site.members[member.code] = member
    end

    @artifacts_map = Hash.new
    @other_nodes_map = Hash.new #we use this for debugging purposes
    
    jnodes = JSON.parse args[:json_nodes]
    jnodes["nodes"].each do |n|
      if NodeType.mission_report?(n["node"])
        artifact = Artifact.new( "mission_report.#{n["node"]["nid"]}", @site.members[n["node"]["uid"]], n["node"] )
        @site.artifacts << artifact
        @artifacts_map[artifact.code] = artifact
      else
        @other_nodes_map[n["node"]["nid"]] = n["node"]
      end
    end
    
    # add qualifying attributes from the nodes structure to be exported
    # for the mission reports they are the mission brief and the campaign
    # and for both the id and the description
    @artifacts_map.values.each do |artifact|
      # add the parent: mission brief
      if mission_brief = @other_nodes_map[artifact.gid] 
        artifact.additional_data[:mission_brief_id] = mission_brief["nid"]
        artifact.additional_data[:mission_brief_title] = mission_brief["title"]
        
        if campaign = @other_nodes_map[mission_brief["parent-gid"]]
          artifact.additional_data[:campaign_id] = campaign["nid"]
          artifact.additional_data[:campaign_title] = campaign["title"]          
        end 
      end
      
    end
    
    jcomments = JSON.parse args[:json_comments]
    jcomments["comments"].each do |c|
      comment = Artifact.new( "comment.#{c["comment"]["cid"]}", @site.members[c["comment"]["uid"]], c["comment"] )
      @artifacts_map[comment.code] = comment
    end
    
    # processing threaded comments and building the artifacts tree
    # we do this in a second step to prevent problems from the json file
    # possibly not being ordered
    @errors = {:without_pid=>[], :parent_not_a_mission_report=>[], :without_nid=>[]}
    @artifacts_map.each do |code, artifact|
      if artifact.pid
         # this is a threaded comment
         parent = @artifacts_map["comment.#{artifact.pid}"]
         @errors[:without_pid] << artifact unless parent
      elsif artifact.cid
         # this is an comment on a mission case
         parent = @artifacts_map["mission_report.#{artifact.nid}"]
         unless parent
           if other_node = @other_nodes_map[artifact.nid]
             @errors[:parent_not_a_mission_report] << [artifact, other_node]
           else
             @errors[:without_nid] << artifact
           end
         end
        
      end
      
      parent.children << artifact if parent     
    end
    
    puts "The following comments had a pid defined but no parent comment was found:\n"
    @errors[:without_pid].each do |artifact|
      puts "    #{artifact.dump_data}"
    end
    puts "======\n"
    
    puts "The following comments had a nid defined that was not a mission_report (the node found is shown in ()):\n"
    @errors[:parent_not_a_mission_report].each do |artifact, other_node|
      puts "    #{artifact.dump_data} (#{other_node.inspect})"
    end      
    puts "======\n"
    
    puts "The following comments had a nid defined but no node with that nid was found:\n"
    @errors[:without_nid].each do |artifact|
      puts "    #{artifact.dump_data}"
    end
    puts "======\n"
    
  end
  
  # builds the list of timed relationships formed
  # by connecting two members A and B if A commented
  # on a post or cmment from B
  def build_timed_relationships!
    @timed_relationships = Array.new
    @site.artifacts.each do |artifact|
      additional_data = artifact.additional_data
      # adding the mission report id and title
      additional_data.merge!(:mission_report_id=>$1, :mission_report_title=>artifact.title) if artifact.code =~ /mission_report\.(\d+)/
      @timed_relationships += build_timed_relationships_for(artifact, additional_data)
    end
  end
  
  # recursively builds the relationships to the 
  # artifact author from the artifact children authors
  # recurses on the children
  def build_timed_relationships_for(artifact, additional_data)
    rels = Array.new
    
    if artifact.author.nil?
      puts "Error reading artifact #{artifact.code}: author not defined [[ #{ artifact.dump_data } ]]"
      return rels
    end
    
    artifact.children.each do |child|
      if child.author.nil?
        puts "Error reading artifact #{child.code} (child of: #{artifact.code}) author not defined [[ #{ child.dump_data } ]]"
      else
        puts "Warning reading artifact #{child.code}: same author of the parent #{artifact.code} [[ #{ artifact.author.code } ]]" if child.author.to_s == artifact.author.to_s
        rels << TimestampedRelationship.new(child.author, artifact.author, child.timestamp, additional_data)
        rels += build_timed_relationships_for(child, additional_data)
      end
    end
    rels 
  end
  
  def build_member_to_member_thread_network!(options={})
    puts "\nBuilding the member to member network based on threaded comments\n"
    build_timed_relationships!
    @weighted_network = WeightedNetwork.new
    @timed_relationships.each do |rel|
      @weighted_network << rel if allowed_relationship?( rel, options )
    end

    @weighted_network.members = @site.
                                  members.
                                  values.
                                  reject{|c| c.respond_to?(:timestamp) && options[:until] && c.timestamp > options[:until] }
  end

  def build_member_to_member_thread_network_detailed!(options={})
    puts "\nBuilding the member to member detailed network based on threaded comments (multi edge)\n"
    build_timed_relationships!
    @detailed_network = DetailedNetwork.new
    @timed_relationships.each do |rel|
      @detailed_network << rel if allowed_relationship?( rel, options )
    end

    @detailed_network.members = @site.
                                  members.
                                  values.
                                  reject{|c| c.respond_to?(:timestamp) && options[:until] && c.timestamp > options[:until] }
  end

  # builds the list of timed relationships formed
  # by connecting members A and post B if A commented
  # on B or on a comment on B
  def build_member_post_relationships!
    @member_post_relationships = Array.new
    @site.artifacts.each do |artifact|
      @member_post_relationships += build_timed_member_post_relationships_for(artifact, artifact)
    end
  end
  
  # recursively builds the relationships to the 
  # root_artifact from the artifact author and children authors
  # recurses on the children
  def build_timed_member_post_relationships_for(root_artifact, artifact)
    rels = Array.new
    
    if artifact.author.nil?
      puts "Error reading artifact #{artifact.code}: author not defined [[ #{ artifact.dump_data } ]]"
      return rels
    else
      rels << TimestampedRelationship.new(artifact.author, root_artifact, artifact.timestamp)      
    end
    
    artifact.children.each do |child|
      rels += build_timed_member_post_relationships_for(root_artifact, child)
    end
    rels 
  end

  def build_member_to_post_network!(options={})
    puts "\nBuilding the member to post network\n"
    build_member_post_relationships!
    @weighted_network = WeightedNetwork.new
    @member_post_relationships.each do |rel|
      @weighted_network << rel if allowed_relationship?( rel, options )
    end

    @weighted_network.members = @site.
                                  members.
                                  values.
                                  reject{|c| c.respond_to?(:timestamp) && options[:until] && c.timestamp > options[:until] }
  end

  def build_member_to_post_detailed_network!(options={})
    puts "\nBuilding the member to post network without merging the arcs\n"
    build_member_post_relationships!
    @detailed_network = DetailedNetwork.new
    @member_post_relationships.each do |rel|
      @detailed_network.relationships << rel if allowed_relationship?( rel, options )
    end

    @detailed_network.members = @site.
                                  members.
                                  values.
                                  reject{|c| c.respond_to?(:timestamp) && options[:until] && c.timestamp > options[:until] }
  end

  def allowed_relationship?( rel, options={} )
    
    excluded_users = ['0'] 
    excluded_users += (options[:excluded_users]||[])
    allowed = true
    allowed &&= ( !rel.a.is_a?(Member) || !excluded_users.include?(rel.a.code) )
    allowed &&= ( !rel.b.is_a?(Member) || !excluded_users.include?(rel.b.code) )
    if rel.respond_to?(:timestamp) && options[:until] 
      allowed &&= ( rel.timestamp <= options[:until] )
    end
    allowed
  end
  
  def export_pajek( filename, options )
    write_file "#{filename}.net", convert_to_pajek(@weighted_network, options)

    puts
    puts "EXPORT PAJEK WITH OPTIONS #{options.inspect} DONE"
    puts
  end
  

  def convert_to_pajek( weighted_network, options={} )
    member_node_field = options[:member_node_field]||:code
    exclude_isolated = options[:exclude_isolated]||false
    
    if exclude_isolated
      contributors = weighted_network.relationships.map{|r| [r.a.send(member_node_field), r.b.send(member_node_field)]}.flatten.uniq 
    else
      contributors = weighted_network.members.map{|m| m.send(member_node_field) }
    end

    pajek = "*Vertices #{contributors.size}" +"\r\n"

    contributors.each_with_index do |c,i|
      pajek << %{#{i+1} "#{c}"}+"\r\n"
    end

    pajek << "*Edges"+"\r\n"

    weighted_network.relationships.each do |r| 
      a = contributors.index(r.a.send(member_node_field))+1
      b = contributors.index(r.b.send(member_node_field))+1
      pajek << %{#{a} #{b} #{r.weight}}+"\r\n"
    end

    return pajek
  end

  def export_member_artifact_csv( filename, options )
    nodes,edges = convert_to_member_artifact_csv(@detailed_network, options)
    
    write_file "#{filename}-nodes.csv", %{"Id","Label","Type","TimeInterval","Mission Brief Id","Mission Brief Title","Campaign Id","Campaign Title","Roles"\n}+nodes.join("\n")
    write_file "#{filename}-edges.csv", %{"Source","Target","TimeInterval"\n}+edges.join("\n")
    puts
    puts "EXPORT MEMBER TO ARTIFACT CSV WITH OPTIONS #{options.inspect} DONE"
    puts
  end
  

  def convert_to_member_artifact_csv( detailed_network, options={} )
    member_node_field = options[:member_node_field]||:code
    timestamp_method = options[:timestamp_method]||:gephi_time_interval
    
    nodes = Array.new
    
    contributors = detailed_network.relationships.map{|r| [r.a, r.b] }.flatten.uniq{|s| s.send(member_node_field)}  
    contributors.each do |c|
      n = %{"#{c.code}","#{c.send(member_node_field)}","#{c.class.name}",#{self.send(timestamp_method, c.timestamp)}}
      if c.respond_to?(:additional_data)
        n << %{,"#{c.additional_data[:mission_brief_id]}","#{c.additional_data[:mission_brief_title]}","#{c.additional_data[:campaign_id]}","#{c.additional_data[:campaign_title]}"}
      else
        n << %{,,,,}
      end
      if c.respond_to?(:roles) 
        n << %{,"#{c.roles}"}
      else
        n << %{,}
      end
      nodes << n
    end

    edges = Array.new
    detailed_network.relationships.each do |r|
      edges << %{"#{r.a.code}","#{r.b.code}",#{self.send(timestamp_method, r.timestamp)}}
    end

    return nodes,edges
  end

  def export_member_member_csv( filename, options )
    nodes,edges = convert_to_member_member_csv(@detailed_network, options)
    
    write_file "#{filename}-nodes.csv", %{"Id","Label","Type","TimeInterval","Roles"\n}+nodes.join("\n")
    write_file "#{filename}-edges.csv", %{"Source","Target","TimeInterval","Mission Report Id","Mission Report Title","Mission Brief Id","Mission Brief Title","Campaign Id","Campaign Title"\n}+edges.join("\n")
    puts
    puts "EXPORT MEMBER TO MEMBER CSV WITH OPTIONS #{options.inspect} DONE"
    puts
  end
  

  def convert_to_member_member_csv( detailed_network, options={} )
    member_node_field = options[:member_node_field]||:code
    timestamp_method = options[:timestamp_method]||:gephi_time_interval
    
    nodes = Array.new
    
    contributors = detailed_network.relationships.map{|r| [r.a, r.b] }.flatten.uniq{|s| s.send(member_node_field)}  
    contributors.each do |c|
      n = %{"#{c.code}","#{c.send(member_node_field)}","#{c.class.name}",#{self.send(timestamp_method, c.timestamp)},"#{c.roles rescue ''}"}
      nodes << n
    end

    edges = Array.new
    detailed_network.relationships.each do |r|
      e = %{"#{r.a.code}","#{r.b.code}",#{self.send(timestamp_method, r.timestamp)}}
      e << %{,"#{r.additional_data[:mission_report_id] rescue ''}"}
      e << %{,"#{r.additional_data[:mission_report_title] rescue ''}"}
      e << %{,"#{r.additional_data[:mission_brief_id] rescue ''}"}
      e << %{,"#{r.additional_data[:mission_brief_title] rescue ''}"}
      e << %{,"#{r.additional_data[:campaign_id] rescue ''}"}
      e << %{,"#{r.additional_data[:campaign_title] rescue ''}"}
      edges << e
    end

    return nodes,edges
  end

  def write_file filename, content
    File.open(filename, 'w') {|f| f.write content }
  end
  
  def gephi_time_interval(from, to=nil)
    f = from.strftime("%Y-%m-%dT%H:%M:%S:000")
    t = to.nil? ? "Infinity" : to.strftime("%Y-%m-%dT%H:%M:%S:000")
    %{"<[#{f}, #{t}]>"}
  end
  def epoch_timestamp(from, to=nil)
    "#{from.to_i}"
  end
end