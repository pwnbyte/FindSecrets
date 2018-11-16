require 'net/http'
require 'uri'
require 'optparse'
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'colorize'


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
    "ApiKey" => 'X-Api-(\w*)',
    "AmazonEndPoint" => "https?:\/\/(.*).amazonaws.com", 
    "AcessKeyAws" => "ACCESS_KEY_ID", 
    "SecretKeyAws" => "SECRET_KEY",
    "Authorization" => "Authorization",
    "appToken" => "appToken",
    "appKey" => "appKey"}

$urls_array = []    

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

def url_crawler(url)
    page = Nokogiri::HTML(open(url)).search('script').each do |link|
        hash_link = link.to_h
        hash_link.each_value do |v|
            if v.end_with?('.js')
                $urls_array.append(v)
                puts "JAVSCRIPT FOUND => #{v}".colorize(:magenta)
            end
        end
    end
end




def parse_response_string(string_response)
    string_response = string_response.strip()
    if /#{@match_data["AmazonEndPoint"]}/.match(string_response).to_s != ""
        puts "[+] Found AMAZON-ENDPOINT => \n ---+---+---\n#{/#{@match_data["AmazonEndPoint"]}/.match(string_response).to_s}\n ---+---+---".colorize(:light_blue)
    end

    if /#{@match_data["Api"]}/.match(string_response).to_s != ""
        puts "[+] Found API-ENDPOINT => \n ---+---+--- \n#{/#{@match_data["Api"]}/.match(string_response).to_s}\n ---+---+---".colorize(:light_blue)
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

    if /#{@match_data["Authorization"]}/.match(string_response).to_s != ""
        puts /#{@match_data["Authorization"]}/.match(string_response).to_s
    end
end

def init_array_requests(array_urls)
    array_urls.each do |url|
        if !url.start_with("https://") and !url.start_with("http://")
            url = 'http://'+url
        end
    return url
    end
end

def manipulate_requests(uri)
    #uri.scheme # http or https
    #uri.host # url 
    #uri.request_uri # path requested
    begin
        puts "[+] REQUEST TO #{uri}".colorize(:yellow)
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        request = Net::HTTP::Get.new(uri.request_uri)
        request["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36"
        response = http.request(request)
        string_response = response.body
        parse_response_string(string_response)

    rescue Errno::ECONNRESET => e
        puts e
    rescue Net::OpenTimeout => e
        puts "[-] Timeout for: #{url}"
    rescue Net::ReadTimeout => e
        puts "[-] Timeout for: #{url}"
    end
end


url_crawler(url)
$urls_array.each do |u|

    if u.start_with?("//")
        u = u.gsub(/\/\//, "https://")
    end

    # extract domains from .js 
    uri_js = URI.parse(u)
    uri_domain = URI.parse(url)

    # verify if .js domains are diferente from output
    if uri_js.host != uri_domain.host
        if uri_js.host.nil?
            uri_js = uri_domain + uri_js
        end

        manipulate_requests(uri_js)

    elsif !u.start_with?(uri_domain)
            u = uri_domain + u
            manipulate_requests(u)
    else
        manipulate_requests(u)
    end
end
