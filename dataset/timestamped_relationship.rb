require 'dataset/relationship'

class TimestampedRelationship < Relationship
  attr_accessor :timestamp
  
  def initialize( from, to, timestamp )
    super(from, to)
    @timestamp = timestamp
  end
end