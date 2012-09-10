class Relationship
  attr_accessor :a, :b, :additional_data
  
  def initialize( from, to, data=nil )
    @a = from
    @b = to
    @additional_data = data
  end
  
  def signature
    %{#{a.to_s}_#{b.to_s}}
  end
  
  def to_s
    %{#{a.to_s} --> #{b.to_s}}
  end
end