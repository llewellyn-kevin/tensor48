from tkinter.filedialog import askopenfilename
import http.server
import socketserver 
import os 
import shutil

# Get replay file
filename = askopenfilename()
print("Copying...")
print(filename)
print("to web/js/replay_file.js")
shutil.copyfile(filename, './web/js/replay_file.js')

# Set up the simple server 
PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'web')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler

# Serve
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    print("Visit http://127.0.0.1:8000/replay.html to view selected replay")
    try:
        httpd.serve_forever() 
    except KeyboardInterrupt: 
        pass 
    print("\r\nClosing the server and freeing port {}".format(PORT))
    httpd.server_close()
