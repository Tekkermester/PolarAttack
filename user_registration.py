import base64
import threading
import webbrowser
import requests
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from paths import APP_DIR, sep
from utils import load_yml, dump_yaml, calculate_token_expire_time, generate_member_id


# CONFIG
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

CLIENT_ID = config.get('CLIENT_ID')
CLIENT_SECRET = config.get('CLIENT_SECRET')

REDIRECT_URI = config.get('REDIRECT_URL')

AUTH_URL = (
    "https://flow.polar.com/oauth2/authorization"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=accesslink.read_all"
)

TOKEN_URL = "https://polarremote.com/v2/oauth2/token"

auth_code = None
token_data = None



# LOCAL CALLBACK SERVER

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/callback" and "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<html><head><title>PolarAttack</title></head><body style='color:black;'><h1 style='color:orange;'>Siker! Bezarhatod ezt az ablakot!</h1><p>Visszaterhetsz az alkalmazasba.</p></body></html>")
        else:
            self.send_response(400)
            self.end_headers()


def run_server():
    HTTPServer(("localhost", 8080), OAuthHandler).handle_request()



# TOKEN EXCHANGE

def exchange_code_for_token(code: str) -> str:
    basic = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    auth_header = base64.b64encode(basic).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    r = requests.post(TOKEN_URL, headers=headers, data=data)
    r.raise_for_status()
    return r.json()



# REGISTER USER

def register_user(access_token: str, member_id: str) -> str:
    xml_body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f"<register><member-id>{member_id}</member-id></register>"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/xml",
        "Accept": "application/json",
    }

    r = requests.post(
        "https://www.polaraccesslink.com/v3/users",headers=headers, data=xml_body)

    r.raise_for_status()
    return r.json()



# MAIN

def main():
    threading.Thread(target=run_server, daemon=True).start()
    webbrowser.open(AUTH_URL)

    while auth_code is None:
        pass

    token_data = exchange_code_for_token(auth_code)

    access_token = token_data["access_token"]
    polar_user_id = token_data["x_user_id"]
    expires_in = token_data["expires_in"]

    tokens_yaml = load_yml(f"{APP_DIR}{sep()}tokens.yml")

    tokens_yaml["accestoken"] = access_token
    tokens_yaml["polar_user_id"] = polar_user_id
    tokens_yaml["expires_in"] = calculate_token_expire_time(expires_in)


    member_id = generate_member_id()
    tokens_yaml["member_id"] = member_id

    result = register_user(access_token, member_id=member_id)

    dump_yaml(f"{APP_DIR}{sep()}tokens.yml",tokens_yaml)

    config_yaml = load_yml(f"{APP_DIR}{sep()}config.yml")
    config_yaml["name"] = f"{result['last-name']} {result['first-name']}"
    dump_yaml(f"{APP_DIR}{sep()}config.yml", config_yaml)
