import re
import random
import os
import string
import time
from tls_client import Session
from terminut import log
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

init(autoreset=True)

class LiveLogin:
    def __init__(self):
        self.base_headers = self._initialize_headers()
        self.session = Session(client_identifier="chrome_120", random_tls_extension_order=True)
        self._flow_token = None
        self._uaid = None
        self._get_initial_cookies()

    def _initialize_headers(self):
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "login.live.com",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def _get_initial_cookies(self):
        response = self.session.get("https://login.live.com/", headers=self.base_headers)
        self._extract_tokens(response.text)

    def _extract_tokens(self, response_text):
        ppft_match = re.search(r'name="PPFT".*?value="([^"]*)"', response_text)
        if ppft_match:
            self._flow_token = ppft_match.group(1)

        uaid_match = response_text.split("uaid=")
        if len(uaid_match) > 1:
            self._uaid = uaid_match[1].split('"')[0]

    def check_email(self, email):
        headers = self._initialize_check_headers()
        payload = self._create_payload(email)

        response = self.session.post("https://login.live.com/GetCredentialType.srf", json=payload, headers=headers)
        return response.json()

    def _initialize_check_headers(self):
        headers = self.base_headers.copy()
        headers["Accept"] = "application/json"
        headers["Content-type"] = "application/json; charset=utf-8"
        return headers

    def _create_payload(self, email):
        return {
            "checkPhones": True,
            "country": "",
            "federationFlags": 3,
            "flowToken": self._flow_token,
            "forceotclogin": False,
            "isCookieBannerShown": False,
            "isExternalFederationDisallowed": False,
            "isFederationDisabled": False,
            "isFidoSupported": True,
            "isOtherIdpSupported": False,
            "isRemoteConnectSupported": False,
            "isRemoteNGCSupported": True,
            "isSignup": False,
            "originalRequest": "",
            "otclogindisallowed": False,
            "uaid": self._uaid,
            "username": email,
        }

def process_email(email):
    live_login = LiveLogin()
    result = live_login.check_email(email)

    if result.get("IfExistsResult") == 0:
        log.info(f"{Fore.GREEN}Valid - {email} - {'has phone' if result.get('HasPhone') == 1 else 'no phone'}{Style.RESET_ALL}")
    else:
        log.error(f"{Fore.RED}Invalid - {email}{Style.RESET_ALL}")

    time.sleep(1)  # Delay of 1 second between email checks

def generate_random_title(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def set_random_title():
    random_title = generate_random_title()
    os.system(f'title {random_title}')

def main():
    set_random_title()
    
    while True:
        with open("emails.txt", "r") as file:
            emails = [line.strip() for line in file.readlines()]

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(process_email, emails)

        recheck = input("\nWould you like to recheck the list of emails? (yes/no): ").strip().lower()
        if recheck != 'yes':
            break

if __name__ == "__main__":
    main()