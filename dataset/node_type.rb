module NodeType
   
   MAPPING = {
     :user => "User profile",
     :mission_report => "Mission report",
     :mission_brief => "Mission brief",
     :campaign => "Campaign"
   }
   
   class << self
     def [](key)
       MAPPING[key.to_sym]
     end

     def method_missing name, *args
       if /^(#{MAPPING.keys.join("|")})\?$/ =~ name.to_s
         is?($1.to_sym, *args)
       end
     end
     
     def is?(what, node)
       MAPPING[what] == node["type"]
     end
   end
   
end