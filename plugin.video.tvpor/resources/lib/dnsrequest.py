import urllib2
import httplib
import socket
import dns.resolver

user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2049.0 Safari/537.36'

class MyHTTPConnection (httplib.HTTPConnection):
    def connect (self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8']
        answer = resolver.query(self.host,'A')
        self.host = answer.rrset.items[0].address
        self.sock = socket.create_connection ((self.host, self.port))#

class MyHTTPHandler (urllib2.HTTPHandler):
    def http_open (self, req):
        return self.do_open (MyHTTPConnection, req)

def request(url):
    opener = urllib2.build_opener(MyHTTPHandler)
    opener.addheaders = [('User-Agent', user_agent)]
    urllib2.install_opener (opener)
    f = urllib2.urlopen (url)
    data = f.read ()
    return data
