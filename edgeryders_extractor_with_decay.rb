# this script extracts the edgeryders member to member network using 
# the new CSV exporter with 'decay' which means it lets the edges 
# disappear after a given amount of days
# The CSV file obtained has the time series
$LOAD_PATH.unshift(File.dirname(__FILE__))
require 'edgeryders_dataset'
require 'fileutils'
require 'date'

ts = Time.new.strftime("%Y%m%d-%H%M")
EXCLUDED_USERS = ['229', '624', '353', '595', '426', '462', '185', '592'] # these are spambots or other blocked users                               

extractionday = Date.today
decay = 30

puts "------------------------"
puts "Loading and parsing"

dataset = EdgerydersDataset.new :json_users => File.read('json/users.json'), 
                                :json_nodes => File.read('json/nodes.json'), 
                                :json_comments => File.read('json/comments.json')

extractiontime = Time.mktime(extractionday.year, extractionday.month, extractionday.day, 23, 59, 59)

dataset.build_member_to_member_thread_network_detailed!(:excluded_users=>EXCLUDED_USERS, :until=>extractiontime)

puts "------------------------"
puts ""
puts "Member to mamber detailed network"
puts "Members count: #{dataset.detailed_network.members.size}"
puts "Edges (raw) count: #{dataset.detailed_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_member_member_csv "export/#{ts}/edgeryders-member-member-with-decay-ANON", :member_node_field=>:code, :exclude_isolated=>false, :decay=>decay
dataset.export_member_member_csv "export/#{ts}/edgeryders-member-member-with-decay-NAMES", :member_node_field=>:name, :exclude_isolated=>false, :decay=>decay

