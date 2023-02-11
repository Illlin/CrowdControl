from http.server import BaseHTTPRequestHandler, HTTPServer
import json

passord = "FishBiscuitsAreFish"

inps = {"names":["Up","Down","Left","Right"], "background":"background.png"}

# HTTPRequestHandler class
class HTTPServerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(self.path[1:])
        content_length = int(self.headers.get("Content-Length", 0))
        request_body = self.rfile.read(content_length).decode()
        try:
            request_data = json.loads(request_body)
            if request_data["password"] == password:
                if "names" in request_data:
                    global inps
                    inps = request_data
                    print("UPDATES INPS ----------------------")
                print(request_data)
                self.send_response(200, {"message": "Success"})
        except json.JSONDecodeError as e:
            self.send_response(400, {"error": "Invalid JSON"})

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Set Buttons")

    # GET
    def do_GET(self):
        print(self.path)
        location = self.path[1:]  # get Image Request Location
        print(location)

        if location == "":
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("Server/main.html", "rb") as b:
                self.wfile.write(b.read())

        elif location == "get-inputs":
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            a = json.dumps(inps)
            print(a)
            self.wfile.write(a.encode("utf-8"))

        elif "button/" in location:
            button = location[7:]
            print(f"GOT BUTTON --- {button}")
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Yeppers you pressed button!")

        elif "images/" in location:
            img = location[7:]
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open(f"Images/{img}", "rb") as b:
                self.wfile.write(b.read())

        else:
            print(f"ERROR --- {location}")
            self.send_response(404)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Error 404")


        print("Done Get")


def run():
    print('starting server...')

    # Server settings
    server_address = ('0.0.0.0', 5000)
    httpd = HTTPServer(server_address, HTTPServerRequestHandler)
    print('running server...')
    httpd.serve_forever()


run()