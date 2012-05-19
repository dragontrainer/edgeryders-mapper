# base element class
class Element

  # THIS SHOULD BE OVERRIDDEN IF USING THE VALIDATIONS
  def legal_attributes
    [ ] 
  end

  def method_missing name, *args
    @data[name.to_s]
  end  

  def existed_at? date_as_string
    self.createdDate[0..date_as_string.size-1] < date_as_string
  end

private
  def default_values! hash, attribs
    attribs.keys.each do |k|
      default_value! hash, k, attribs[k]
    end
  end

  def default_value! hash, key, def_val
    hash[key] = def_val if not hash.include? key
  end

  def verify_well_formedness! hash
    verify_all_keys_are_legal! hash
    verify_all_attributes_are_present! hash
  end

  def verify_all_keys_are_legal! hash
    hash.keys.each do |k|
      if not legal_attributes.include? k
        raise "#{self.class.name} PARSE ERROR: Wrong key >>#{k}<< in data: #{hash.inspect}"
      end
    end    
  end

  def verify_all_attributes_are_present! hash
    legal_attributes.each do |att|
      if not hash.keys.include? att
        raise "#{self.class.name} PARSE ERROR: Missing key >>#{att}<< in data: #{hash.inspect}"
      end
    end
  end


end