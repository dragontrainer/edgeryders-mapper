require 'dataset/relationship'

class WeightedRelationship < Relationship
  attr_accessor :weight
  
  def initialize( from, to, weight=1, data=nil )
    super(from, to, data=nil)
    @weight = weight||1
  end
  
end