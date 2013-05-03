require 'dataset/element'
require 'time'

# An artifact of the site produced by a member
# it is connected to many other artifacts 
# through the connection to other artifcats
# the author and other artifacts authors collaborate
class Artifact < Element
  attr_accessor :code, :author, :children, :timestamp, :additional_data
  
  def initialize(code, author, raw_data)
    @code = code
    @author = author
    @children = Array.new
    @data = raw_data
    ts = @data["timestamp"]||@data["created"]
    @timestamp = Time.at( ts.to_i ) if ts

    dt = @data["date"]
    @timestamp ||= Time.parse( dt ) rescue nil
    
    @additional_data = {}
  end
  
  def pretty(depth=0)
    puts %{#{" "*depth}- #{@code}}
    @children.each do |c|
      c.pretty(depth+1)
    end
  end
  
  def name
    @data["title"]||code
  end
  
  def dump_data
    @data.to_json
  end
end