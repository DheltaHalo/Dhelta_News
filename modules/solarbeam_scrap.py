import urllib.request as urllib2
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "http://solarbeam.io/exchange/swap"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'

# header variable
headers = { 'User-Agent' : user_agent }

# creating request
req = urllib2.Request(url, None, headers)

# getting html
html = urllib2.urlopen(req).read()
print(html)