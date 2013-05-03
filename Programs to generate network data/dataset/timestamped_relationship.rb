require 'dataset/relationship'

class TimestampedRelationship < Relationship
  attr_accessor :timestamp
  
  def initialize( from, to, timestamp, data=nil )
    super(from, to, data)
    @timestamp = timestamp
  end
end