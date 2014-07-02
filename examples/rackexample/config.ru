app = proc do |env|
    [200, { "Content-Type" => "text/html" }, ["hello <b>world</b> (from rack)"]]
end
run ap
