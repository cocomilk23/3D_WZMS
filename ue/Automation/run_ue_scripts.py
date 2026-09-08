"""Run editor bridge scripts sequentially and stop at the first failed job."""
import argparse
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
parser=argparse.ArgumentParser();parser.add_argument('scripts',nargs='+');args=parser.parse_args()
client=UnrealMcpClient();client.connect()
try:
    for script in args.scripts:
        print('START',script,flush=True);run_job(client,script);print('COMPLETE',script,flush=True)
finally:client.close()
