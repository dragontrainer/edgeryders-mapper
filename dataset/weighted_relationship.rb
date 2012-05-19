require 'dataset/relationship'

class WeightedRelationship < Relationship
  attr_accessor :weight
  
  def initialize( from, to, weight=1 )
    super(from, to)
    @weight = weight||1
  end
  
end