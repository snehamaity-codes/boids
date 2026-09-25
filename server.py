"""
Simple HTTP server to run the Boids simulation locally.
Usage: python server.py
Then open http://localhost:8000 in your browser.
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8000

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPServer = http.server.SimpleHTTPRequestHandler

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print(f"\n  Boids Simulation Server")
print(f"  -------------------------")
print(f"  Running at -> http://localhost:{PORT}")
print(f"  Press Ctrl+C to stop\n")

webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        httpd.server_close()
