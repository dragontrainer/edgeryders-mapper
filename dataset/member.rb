require 'dataset/element'

# the member is a person producing artifacts on a site
class Member < Element
  attr_accessor :code

  def initialize(raw_data)
    @data = raw_data
    @code = "#{raw_data["uid"]}"
  end
  
  def to_s
    "#{@code}"
  end
end