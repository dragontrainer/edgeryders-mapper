$LOAD_PATH.unshift(File.dirname(__FILE__))
require 'edgeryders_dataset'
require 'fileutils'
require 'date'

ts = Time.new.strftime("%Y%m%d-%H%M")
EXCLUDED_USERS = ['229', '624', '353', '595', '426', '462', '185', '592'] # these are spambots or other blocked users                               

today = Date.today
# see documentation of time objects for exact timing
one_month_ago_day = today - 30
one_month_ago = Time.mktime(one_month_ago_day.year, one_month_ago_day.month, one_month_ago_day.day)
two_months_ago_day = today - 60 
two_months_ago = Time.mktime(two_months_ago_day.year, two_months_ago_day.month, two_months_ago_day.day)
four_months_ago_day = today - 120 
four_months_ago = Time.mktime(four_months_ago_day.year, four_months_ago_day.month, four_months_ago_day.day)

puts "------------------------"
puts "Loading and parsing"

dataset = EdgerydersDataset.new :json_users => File.read('json/users.json'), 
                                :json_nodes => File.read('json/nodes.json'), 
                                :json_comments => File.read('json/comments.json')
                                 
puts "------------------------"

dataset.build_member_to_member_thread_network!(:excluded_users=>EXCLUDED_USERS)

puts ""
puts "Member to member network up to now"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Connected members count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-until_now-ANON", :member_node_field=>:code, :exclude_isolated=>false
dataset.export_pajek "export/#{ts}/edgeryders-until_now-NAMES", :member_node_field=>:name, :exclude_isolated=>false

puts "------------------------"
dataset.build_member_to_member_thread_network!(:excluded_users=>EXCLUDED_USERS, :until=>one_month_ago)

puts ""
puts "Member to member network up to #{one_month_ago}"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Connected members count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-until_#{one_month_ago.strftime("%Y%m%d_%H%M")}-ANON", :member_node_field=>:code, :exclude_isolated=>false
dataset.export_pajek "export/#{ts}/edgeryders-until_#{one_month_ago.strftime("%Y%m%d_%H%M")}-NAMES", :member_node_field=>:name, :exclude_isolated=>false

puts "------------------------"
dataset.build_member_to_member_thread_network!(:excluded_users=>EXCLUDED_USERS, :until=>two_months_ago)

puts ""
puts "Member to member network up to #{two_months_ago}"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Connected members count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-until_#{two_months_ago.strftime("%Y%m%d_%H%M")}-ANON", :member_node_field=>:code, :exclude_isolated=>false
dataset.export_pajek "export/#{ts}/edgeryders-until_#{two_months_ago.strftime("%Y%m%d_%H%M")}-NAMES", :member_node_field=>:name, :exclude_isolated=>false

puts "------------------------"

dataset.build_member_to_member_thread_network!(:excluded_users=>EXCLUDED_USERS, :until=>four_months_ago)

puts ""
puts "Member to member network up to #{four_months_ago}"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Connected members count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-until_#{four_months_ago.strftime("%Y%m%d_%H%M")}-ANON", :member_node_field=>:code, :exclude_isolated=>false
dataset.export_pajek "export/#{ts}/edgeryders-until_#{four_months_ago.strftime("%Y%m%d_%H%M")}-NAMES", :member_node_field=>:name, :exclude_isolated=>false

puts "------------------------"

dataset.build_member_to_post_network!(:excluded_users=>EXCLUDED_USERS)

puts ""
puts "Member to post network up to now"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Posts count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-until_now-ANON", :member_node_field=>:code, :exclude_isolated=>true
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-until_now-NAMES", :member_node_field=>:name, :exclude_isolated=>true

puts "------------------------"

dataset.build_member_to_post_network!(:excluded_users=>EXCLUDED_USERS, :until=>two_months_ago)

puts ""
puts "Member to post network up to #{two_months_ago}"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Posts count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-until_#{two_months_ago.strftime("%Y%m%d_%H%M")}-ANON", :member_node_field=>:code, :exclude_isolated=>true
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-until_#{two_months_ago.strftime("%Y%m%d_%H%M")}-NAMES", :member_node_field=>:name, :exclude_isolated=>true

puts "------------------------"

dataset.build_member_to_post_network!(:excluded_users=>EXCLUDED_USERS, :until=>four_months_ago)

puts ""
puts "Member to post network up to #{four_months_ago}"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Posts count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-until_#{four_months_ago.strftime("%Y%m%d_%H%M")}-ANON", :member_node_field=>:code, :exclude_isolated=>true
dataset.export_pajek "export/#{ts}/edgeryders-members-to-post-until_#{four_months_ago.strftime("%Y%m%d_%H%M")}-NAMES", :member_node_field=>:name, :exclude_isolated=>true

puts "------------------------"

dataset.build_member_to_post_detailed_network!(:excluded_users=>EXCLUDED_USERS)

puts ""
puts "Member to post detailed network"
puts "Members count: #{dataset.detailed_network.members.size}"
puts "Posts count: #{dataset.detailed_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.detailed_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_member_artifact_csv "export/#{ts}/edgeryders-members-to-post-detailed-ANON", :member_node_field=>:code
dataset.export_member_artifact_csv "export/#{ts}/edgeryders-members-to-post-detailed-NAMES", :member_node_field=>:name

dataset.export_member_artifact_csv "export/#{ts}/edgeryders-members-to-post-detailed-withepochtimestamp-ANON", :member_node_field=>:code, :timestamp_method=>:epoch_timestamp
dataset.export_member_artifact_csv "export/#{ts}/edgeryders-members-to-post-detailed-withepochtimestamp-NAMES", :member_node_field=>:name, :timestamp_method=>:epoch_timestamp

puts "------------------------"

dataset.build_member_to_member_thread_network_detailed!(:excluded_users=>EXCLUDED_USERS)

puts ""
puts "Member to mamber detailed network"
puts "Members count: #{dataset.detailed_network.members.size}"
puts "Edges count: #{dataset.detailed_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_member_member_csv "export/#{ts}/edgeryders-members-to-member-detailed-withepochtimestamp-ANON", :member_node_field=>:code, :timestamp_method=>:epoch_timestamp
dataset.export_member_member_csv "export/#{ts}/edgeryders-members-to-member-detailed-withepochtimestamp-NAMES", :member_node_field=>:name, :timestamp_method=>:epoch_timestamp
