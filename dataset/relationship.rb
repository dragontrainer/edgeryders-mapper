class Relationship
  attr_accessor :a, :b
  
  def initialize( from, to )
    @a = from
    @b = to
  end
  
  def signature
    %{#{a.to_s}_#{b.to_s}}
  end
  
  def to_s
    %{#{a.to_s} --> #{b.to_s}}
  end
end