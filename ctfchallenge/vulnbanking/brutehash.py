import hashlib
from datetime import date, timedelta

hash = '5e6f59f4f4150be8e61eaa20bec51a75'
pwd_wordlist = '/usr/share/wordlists/ctfchallenge/passwords-large.txt'

def generateDateStrings():
    startdate = date(1970, 1, 1)
    dates = [startdate]
    for i in range(365*73):
        startdate = startdate + timedelta(days=1)
        dates.append(startdate)
    return [s.strftime('%d%m%Y') for s in dates]

def generateHashCombo(custno, password):
    combined = custno + password
    m = hashlib.md5()
    m.update(combined.encode('UTF-8'))
    return m.hexdigest()

def bruteForceHash():
    datestrings = generateDateStrings()
    digits = [str(s).zfill(2) for s in range(100)]
    passwords = [password.strip() for password in open(pwd_wordlist, 'r')]
    for datestring in datestrings:
        for digit in digits:
            for password in passwords:
                password =  password.strip()
                hashcombo = generateHashCombo(datestring + digit, password)
                if hashcombo == hash:
                    print(f'Found cust number {datestring+digit} and password {password} for hash {hash}')
                    return

bruteForceHash()