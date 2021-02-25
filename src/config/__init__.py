import argparse
import os
from os.path import expanduser

SPLIT_CLI_BACKEND_URI = "https://split-cli-backend.herokuapp.com"
SPLIT_CLI_BACKEND_API_URI = "/api/v1"
SPLIT_CLI_BACKEND_BASE_URL = f"{SPLIT_CLI_BACKEND_URI}{SPLIT_CLI_BACKEND_API_URI}"

home = expanduser("~")
config_path=f"{home}/.split"
if not os.path.isdir(config_path):
    os.mkdir(config_path)
config_file = f"{config_path}/splitcli.json"

parser = argparse.ArgumentParser(description='optional baseUrl')
parser.add_argument('--baseUrl', help='optional base url')
args = parser.parse_args()
if args.baseUrl is not None:
    SPLIT_CLI_BACKEND_URI = args.baseUrl
    SPLIT_CLI_BACKEND_BASE_URL = f"{SPLIT_CLI_BACKEND_URI}{SPLIT_CLI_BACKEND_API_URI}"
    print(f"Working with base url: {SPLIT_CLI_BACKEND_URI}")