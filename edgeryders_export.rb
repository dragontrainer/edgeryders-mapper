require 'edgeryders_dataset'
require 'fileutils'

ts = Time.new.strftime("%Y%m%d-%H%M")
EXCLUDED_USERS = ['229', '624', '353', '595', '426', '462', '185', '592'] # these are spambots or other blocked users                               

puts "------------------------"
puts "Loading and parsing"

dataset = EdgerydersDataset.new :json_users => File.read('json/users.json'), 
                                :json_nodes => File.read('json/nodes.json'), 
                                :json_comments => File.read('json/comments.json')
                                 
puts "------------------------"

dataset.build_member_to_member_thread_network!(:excluded_users=>EXCLUDED_USERS)

puts ""
puts "Members count: #{dataset.site.members.size}"
puts "Connected members count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-ANON.net", :member_node_field=>:code, :exclude_isolated=>false
dataset.export_pajek "export/#{ts}/edgeryders-NAMES.net", :member_node_field=>:name, :exclude_isolated=>false

puts "------------------------"

dataset.build_member_to_post_network!(:excluded_users=>EXCLUDED_USERS)

puts ""
puts "Members count: #{dataset.site.members.size}"
puts "Posts count: #{dataset.site.artifacts.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-ANON.net", :member_node_field=>:code, :exclude_isolated=>true
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-NAMES.net", :member_node_field=>:name, :exclude_isolated=>true
