"""Local-only static preview server; defaults to port 8766."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse

p=argparse.ArgumentParser()
p.add_argument('--port',type=int,default=8766)
args=p.parse_args()
root=Path(__file__).resolve().parents[1]/'web-preview'
handler=partial(SimpleHTTPRequestHandler,directory=str(root))
server=ThreadingHTTPServer(('127.0.0.1',args.port),handler)
print(f'WZMS preview: http://127.0.0.1:{args.port}/',flush=True)
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close()
