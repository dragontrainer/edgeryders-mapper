
class DetailedNetwork
  attr_accessor :members, :relationships
  
  
  def initialize
    @relationships = Array.new
    @members = Array.new
  end

  def <<(relationship)
    @relationships << relationship
  end
  
end