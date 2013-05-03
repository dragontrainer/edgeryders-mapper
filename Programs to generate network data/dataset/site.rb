# a site where members interact on artifacts
# it has a list of artifacts and a list of members
class Site 
  attr_accessor :artifacts, :members
  
  def initialize
    @artifacts = Array.new
    @members = Hash.new
  end
end