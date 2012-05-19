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

class EdgerydersDataset
  
  attr_accessor :site, :timed_relationships, :artifacts_map, :weighted_network
  
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
      if n["node"]["type"] == 'mission_case'
        artifact = Artifact.new( "mission_case.#{n["node"]["nid"]}", @site.members[n["node"]["uid"]], n["node"] )
        @site.artifacts << artifact
        @artifacts_map[artifact.code] = artifact
      else
        @other_nodes_map[n["node"]["nid"]] = n["node"]
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
    @errors = {:without_pid=>[], :parent_not_a_mission_case=>[], :without_nid=>[]}
    @artifacts_map.each do |code, artifact|
      if artifact.pid
         # this is a threaded comment
         parent = @artifacts_map["comment.#{artifact.pid}"]
         @errors[:without_pid] << artifact unless parent
      elsif artifact.cid
         # this is an comment on a mission case
         parent = @artifacts_map["mission_case.#{artifact.nid}"]
         unless parent
           if other_node = @other_nodes_map[artifact.nid]
             @errors[:parent_not_a_mission_case] << [artifact, other_node]
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
    
    puts "The following comments had a nid defined that was not a mission_case (the node found is shown in ()):\n"
    @errors[:parent_not_a_mission_case].each do |artifact, other_node|
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
      @timed_relationships += build_timed_relationships_for(artifact)
    end
  end
  
  # recursively builds the relationships to the 
  # artifact author from the artifact children authors
  # recurses on the children
  def build_timed_relationships_for(artifact)
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
        
        rels << TimestampedRelationship.new(child.author, artifact.author, child.timestamp)
        rels += build_timed_relationships_for(child)
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
  end

  def allowed_relationship?( rel, options={} )
    
    excluded_users = ['0'] 
    excluded_users += (options[:excluded_users]||[])
    
    ( !rel.a.is_a?(Member) || !excluded_users.include?(rel.a.code) ) && ( !rel.b.is_a?(Member) || !excluded_users.include?(rel.b.code) )
  end
  
  def export_pajek( filename, options )
    write_file filename, convert_to_pajek(@weighted_network.relationships, options)

    puts
    puts "EXPORT PAJEK WITH OPTIONS #{options.inspect} DONE"
    puts
  end
  

  def convert_to_pajek( relationships, options={} )
    member_node_field = options[:member_node_field]||:code
    exclude_isolated = options[:exclude_isolated]||false
    
    if exclude_isolated
      contributors = relationships.map{|r| [r.a.send(member_node_field), r.b.send(member_node_field)]}.flatten.uniq 
    else
      contributors = @site.members.values.map{|m| m.send(member_node_field) }
    end

    pajek = "*Vertices #{contributors.size}" +"\r\n"

    contributors.each_with_index do |c,i|
      pajek << %{#{i+1} "#{c}"}+"\r\n"
    end

    pajek << "*Edges"+"\r\n"

    relationships.each do |r| 
      a = contributors.index(r.a.send(member_node_field))+1
      b = contributors.index(r.b.send(member_node_field))+1
      pajek << %{#{a} #{b} #{r.weight}}+"\r\n"
    end

    return pajek
  end

  def write_file filename, content
    File.open(filename, 'w') {|f| f.write content }
  end

end