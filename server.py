import os
import http.server
import socketserver
import threading
import time
from datetime import datetime

from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        msg = 'Hello! you requested %s' % (self.path)
        self.wfile.write(msg.encode())


port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))


def continuous_logger(port):
    """Log server status every LOG_INTERVAL seconds"""
    start_time = time.time()
    while True:
        elapsed = int(time.time() - start_time)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{timestamp}] Server running on port {port} - Uptime: {elapsed}s')
        t = os.environ.get('LOG_INTERVAL', '5')
        time.sleep(int(t))


# Start logging thread as daemon
logger_thread = threading.Thread(target=continuous_logger, args=(port,), daemon=True)
logger_thread.start()

httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
