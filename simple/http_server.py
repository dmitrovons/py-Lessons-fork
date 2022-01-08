from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def Parse(self, aPath: str) -> str:
        Query = urlparse(aPath).query
        if (Query == ''):
            return 'Empty'

        Pairs = Query.split('&')
        PairsDict = dict(P.split('=') for P in Pairs)

        Digits = ['Null', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        Num = PairsDict.get('num', '')
        if (Num) and (len(Num) == 1):
            Msg = Digits[int(Num)]
        else:
            Msg = 'Unknown'
        return Msg

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        Msg = self.Parse(self.path)
        Body = "Query: %s, Digit: %s" % (self.path, Msg)
        Page = """
        <html>
            </head>
                <meta charset='utf-8'>
                <title>Python HTTP server</title>
                </head>
            <body>
                %s
            </body>
        </html>""" % (Body)

        self.wfile.write(Page.encode())


httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
