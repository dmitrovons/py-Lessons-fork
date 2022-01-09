from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def Parse(self, aPath: str) -> dict:
        Query = urlparse(aPath).query
        if (Query == ''):
            Res = {}
        else:
            Pairs = Query.split('&')
            Res = dict(P.split('=') for P in Pairs)
        return Res

    def GetDigitStr(self, aNum: str) -> str:
        Digits = ['Null', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        if (len(aNum) == 1):
            Msg = Digits[int(aNum)]
        else:
            Msg = 'Unknown'
        return Msg

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        Query = self.Parse(self.path)
        DigitStr = self.GetDigitStr(Query.get('num', '0'))
        BgColor = Query.get('color', 'white')
        RevStr = Query.get('rev', 'reverse')

        Page = """
        <html>
            </head>
                <style>
                    body {
                        background-color: %s;
                    }
                </style>
                <meta charset='utf-8'>
                <title>Python HTTP server</title>
            </head>
            <body>
                <h1>Color: %s</h1><br>
                <h1>Digit: %s</h1><br>
                <h1>Reverse: %s</h1><br>
            </body>
        </html>""" % (BgColor, BgColor, DigitStr, RevStr[::-1])

        self.wfile.write(Page.encode())


httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
