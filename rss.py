import config
import PyRSS2Gen
import http.server
import socketserver
import core
from datetime import datetime
from threading import Thread

# Our rss generator
rss = PyRSS2Gen.RSS2(
    title="Satellite station images",
    link="",
    description="Images from the station",
    lastBuildDate=datetime.now(),
    items=[]
    )

# Http server
httpd = 0
server_thread = 0

# We need to set out directory
class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=config.output_dir, **kwargs)

# Function for adding passes
def addRSSPass(satellite, filename, date):

    # Generate item content, here being images
    image = ""
    if satellite.downlink == "APT":
        image = "Visible + Infrared : <\p>" + "<img src=\"" + filename + ".png\">"
    elif satellite.downlink == "LRPT":
        image = "Visible : <\p>" + "<img src=\"" + filename + " - Visible.bmp\">" + "<\p>" + "Infrared : <\p>" + "<img src=\"" + filename + " - Infrared.bmp\">"

    # Add it to the feed
    rss.items.append(PyRSS2Gen.RSSItem(
        title = satellite.name + " on " + date.strftime('%H:%-M %d, %b %Y'),
        link = "",
        description = image,
        guid = PyRSS2Gen.Guid(""),
        pubDate = date)
    )

    # Write the file to push the update
    rss.write_xml(open(config.output_dir + "/rss.xml", "w"))

# Used for the startup procedure
def startServer():
    global rss, httpd, server_thread

    # Configure the http server
    httpd = socketserver.TCPServer(("", config.rss_port), HTTPHandler)
    print("Starting http server at " + str(config.rss_port))
    print("\n")

    # Start it in a thread
    server_thread = Thread(target = httpd.serve_forever)
    server_thread.start()

    # Write the file to make the feed readable
    rss.write_xml(open(config.output_dir + "/rss.xml", "w"))
