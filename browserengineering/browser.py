import socket
import ssl

class URL:
    def __init__(self, url: str):
        self.scheme, url = url.split('://', 1)
        assert self.scheme in ['http', 'https', 'file']
        if '/' not in url:
            url = url + '/'
        self.host, url = url.split('/', 1)
        self.path = '/' + url
        self.port = 80 if self.scheme == 'http' else 443
        if ':' in self.host:
            self.host, port = self.host.split(':', 1)
            self.port = int(port)
        
    def request(self):
        if self.scheme == 'file':
            with open(self.path, 'r') as file:
                content = file.read()
                print(content)
            return
        
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        
        if self.scheme == 'https':
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
            
        s.connect((self.host, self.port))
        request = self.setup_headers()
        s.send(request.encode('utf8')) # this encoding makes sure we're sending type bytes
        response = s.makefile('r', encoding='utf8', newline='\r\n')
        statusline = response.readline()
        version, status, explanation = statusline.split(' ', 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == '\r\n': break
            header, value = line.split(':', 1)
            response_headers[header.casefold()] = value.strip()
        assert 'transfer-encoding' not in response_headers
        assert 'content-encoding' not in response_headers
        content = response.read()
        s.close()
        return content
    
    def setup_headers(self) -> str:
        request = 'GET {} HTTP/1.0\r\n'.format(self.path)
        request += 'Host: {}\r\n'.format(self.host)
        request += 'Connection: close\r\n'
        request += 'User-Agent: CustomUserAgent/1.1\r\n'
        request += '\r\n'
        return request
    
def show(body: str):
    in_tag = False
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            print(c, end="")
            
def load(url):
    body = url.request()
    if not url.scheme == 'file':
        show(body)

if __name__ == '__main__':
    import sys
    load(URL(sys.argv[1]))