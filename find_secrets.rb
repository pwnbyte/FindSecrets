require 'net/http'
require 'uri'
require 'optparse'

AUTHOR = "Gh0sTNiL"
VERSION= "v0.1(Beta)"

def banner()
    
puts %Q(

    88888888b oo                dP    .d88888b                                        dP            
    88                          88    88.    "'                                       88            
   a88aaaa    dP 88d888b. .d888b88    `Y88888b. .d8888b. .d8888b. 88d888b. .d8888b. d8888P .d8888b. 
    88        88 88'  `88 88'  `88          `8b 88ooood8 88'  `"" 88'  `88 88ooood8   88   Y8ooooo. 
    88        88 88    88 88.  .88    d8'   .8P 88.  ... 88.  ... 88       88.  ...   88         88 
    dP        dP dP    dP `88888P8     Y88888P  `88888P' `88888P' dP       `88888P'   dP   `88888P' 
   ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    => Author: #{AUTHOR}
    => Version: #{VERSION}

)   
end


## RegeX patterns
@match_data = {"Api" => "/api", 
    "ApiKey" => 'X-Api-(\w*)","(\w*)"',
    "AmazonEndPoint" => "https?:\/\/(.*).amazonaws.com", 
    "AcessKeyAws" => "ACCESS_KEY_ID", 
    "SecretKeyAws" => "SECRET_KEY"}


options = {}

OptionParser.new do |opt|
    opt.banner = banner()
    opt.on("-u=s", "--url", "[*] Required target URL") do |i|
        options[:url] = i
    end
end.parse!

if options[:url].nil?
    puts "[*] target is required"
end

url = options[:url]

if !url.start_with?('http://') and !url.start_with?('https://')
    puts "[+] provide a schema https://#{url}"
    exit!
end

def parse_response_string(string_response)
    string_response = string_response.strip()
    if /#{@match_data["AmazonEndPoint"]}/.match(string_response).to_s != ""
        p /#{@match_data["AmazonEndPoint"]}/.match(string_response).to_s
    end

    if /#{@match_data["Api"]}/.match(string_response).to_s != ""
        p /#{@match_data["Api"]}/.match(string_response).to_s
    end

    if /#{@match_data["ApiKey"]}/.match(string_response).to_s != "" 
        p /#{@match_data["ApiKey"]}/.match(string_response).to_s
    end

    if /#{@match_data["AcessKeyAws"]}/.match(string_response).to_s != ""
        p /#{@match_data["AcessKeyAws"]}/.match(string_response).to_s
    end

    if /#{@match_data["SecretKeyAws"]}/.match(string_response).to_s != ""
        p /#{@match_data["SecretKeyAws"]}/.match(string_response).to_s
    end
end



def manipulate_requests(url)

    uri = URI.parse(url)
    #uri.scheme # http or https
    #uri.host # url 
    #uri.request_uri # path requested
    begin
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        request = Net::HTTP::Get.new(uri.request_uri)
        request["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36"
        response = http.request(request)
        string_response = response.body
        parse_response_string(string_response)

    rescue Errno::ECONNRESET => e
        puts e
    end

end

manipulate_requests(url)
