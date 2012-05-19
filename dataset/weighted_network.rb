require 'dataset/weighted_relationship'

class WeightedNetwork
  
  def initialize
    @relations_map = Hash.new
  end
  
  def <<(relationship)
    if rel = @relations_map[relationship.signature]
      rel.weight += 1
    else 
       @relations_map[relationship.signature] = WeightedRelationship.new relationship.a, relationship.b
    end
  end
  
  def relationships 
    @relations_map.values
  end
end