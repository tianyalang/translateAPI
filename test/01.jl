using HTTP
r = HTTP.request("GET", "http://httpbin.org/ip")
println(r.status)
println(String(r.body))