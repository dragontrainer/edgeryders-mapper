require 'dataset/element'

# the member is a person producing artifacts on a site
class Member < Element
  attr_accessor :code, :timestamp

  def initialize(raw_data)
    @data = raw_data
    @code = "#{raw_data["uid"]}"
    
    ts = @data["timestamp"]||@data["created"]
    @timestamp = Time.at( ts.to_i ) if ts

    dt = @data["date"]
    @timestamp ||= Time.parse( dt ) rescue nil
  end
  
  def to_s
    "#{@code}"
  end
   
end