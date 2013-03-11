# This file exports only .net  files. There are 9 time slices, 30 days apart from each other, counting backwards from the date the file is run. 
#To change the number of slices change the integer at the beginning of line 24; to change the interval between slices change the integer at the
# end of line 45

$LOAD_PATH.unshift(File.dirname(__FILE__))
require 'edgeryders_dataset'
require 'fileutils'
require 'date'

ts = Time.new.strftime("%Y%m%d-%H%M")
EXCLUDED_USERS = ['229', '624', '353', '595', '426', '462', '185', '592'] # these are spambots or other blocked users                               

extractionday = Date.new(2012, 12, 10)
# see documentation of time objects for exact timing

puts "------------------------"
puts "Loading and parsing"

dataset = EdgerydersDataset.new :json_users => File.read('json/users.json'), 
                                :json_nodes => File.read('json/nodes.json'), 
                                :json_comments => File.read('json/comments.json')
                                 
puts "------------------------"

15.times do

extractiontime = Time.mktime(extractionday.year, extractionday.month, extractionday.day)

dataset.build_member_to_member_thread_network!(:excluded_users=>EXCLUDED_USERS)

dataset.build_member_to_member_thread_network!(:excluded_users=>EXCLUDED_USERS, :until=>extractiontime)

puts ""
puts "Member to member network up to #{extractionday}"
puts "Members count: #{dataset.weighted_network.members.size}"
puts "Connected members count: #{dataset.weighted_network.relationships.map{|r| [r.a, r.b]}.flatten.uniq.size}"
puts "Edges count: #{dataset.weighted_network.relationships.size}"
puts ""
puts "Exporting ..."

FileUtils.mkdir_p "export/#{ts}"
dataset.export_pajek "export/#{ts}/edgeryders-until_#{extractiontime.strftime("%Y%m%d_%H%M")}-ANON", :member_node_field=>:code, :exclude_isolated=>false
dataset.export_pajek "export/#{ts}/edgeryders-until_#{extractiontime.strftime("%Y%m%d_%H%M")}-NAMES", :member_node_field=>:name, :exclude_isolated=>false

extractionday -=28

end