import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64

ADDRESS = "0.0.0.0"
PORT = 8080

def getEstates():
    conn = psycopg2.connect(database="my_db",
                        host="database",
                        user="root",
                        password="pass",
                        port="5432")

    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM estates")
    estates = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return estates

class EstatesRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        html = """
            <html>
                <head>
                    <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
                    <meta content="utf-8" http-equiv="encoding">
                </head>
                <body>"""
        for estate in estates:
            memView = estate[2]
            imageBinary = bytes(memView)
            encodedString = base64.b64encode(imageBinary).decode('utf-8')

            html += "<h3>" + estate[1] + "</h3>"
            html += f'<img src="data:image/jpeg;base64,{encodedString}">'
        html += "</body></html>"
        
        self.wfile.write( bytes(html, "utf-8") )


if __name__ == "__main__":
    estates = getEstates()

    server = HTTPServer((ADDRESS, PORT), EstatesRequestHandler)
    server.estates = estates
    server.serve_forever()

    print("server is running")