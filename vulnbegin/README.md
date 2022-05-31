# VulnBegin

http://www.vulnbegin.co.uk/ - 9 flags to find

OK so we're greeted with well not a lot really....

![Not much here](./images/vulnbegin-01.png)

Dev tools reveal there are no particularly interesting javascript for this page just jquery and bootstrap

![Javascript](./images/vulnbegin-02.png)

Ok lets check if there's a robots.txt

```
User-agent: *
Disallow: /secret_d1rect0y/
```

Woo yup, this reveals a flag (no. 4)

```
[^FLAG^XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX^FLAG^]
```

Ok let's try some directory fuzzing. So first things first I have to work out how to set a cookie with my fuzzing tool of choice ffuf. Because....

```
If using automation tools you need to make sure you are setting the ctfchallenge cookie with every request or it will NOT work
```

Quick check of the help

```
ffuf -h                                                                                                                                     
Fuzz Faster U Fool - v1.3.1 Kali Exclusive <3

HTTP OPTIONS:
  -H                  Header `"Name: Value"`, separated by colon. Multiple -H flags are accepted.
```

Also need to limit the number of requests

```
Important Information

To avoid overloading the challenges please limit your requests to 10 per second

If you receive a HTTP status code 429 this is because you are requesting too much information from the challenges
```

Another check of the help reveals we can limit the threads with the -t and set the delay between requests with -p so we have a command similar to the below

```
ffuf -u 'https://www.vulnbegin.co.uk/FUZZ' -w /usr/share/wordlists/ctfchallenge/content.txt -H "Cookie: ctfchallenge=xxxxx" -t 1 -p 0.1
```

I don't know why but requests made with ffuf to this domain timeout every time, no matter what setting I put for the thread count/delay between requests. So instead I switched over to using Burp Intruder and sniper mode on the directory. Using the provided content.txt as my payload list

![position](./images/vulnbegin-03.png)

Again making sure to limit our requests as per our scope

![resource pool](./images/vulnbegin-04.png)

Plenty of 404 not found responses, except one

![cpadmin](./images/vulnbegin-05.png)

OK using the path in the browser redirects me to /cpadmin/login, a login page! Let's try a quick basic SQLi check

![alt](./images/vulnbegin-06.png)

OK that didn't work, BUT it does give a specific message about an invalid username. Let's try admin before fuzzing the usernames save some time.

![admin worked](./images/vulnbegin-07.png)

Success. OK time to fuzz passwords, again in Burp similar to the previous fuzz but with a POST request for login

And we get another 302 redirect with this payload

![password](./images/vulnbegin-08.png)

Yay got flag no.5

![flag](./images/vulnbegin-09.png)

As I'm logged in it looks like I have a new 'token' cookie, quick fuzz test at /cpadmin see if I get any results.....

Whilst that runs, I'm wondering if I need to find any subdomains of vulnbegin.co.uk, let's use tomnomnom's assetfinder

```
assetfinder -subs-only vulnbegin.co.uk
www.vulnbegin.co.uk
vulnbegin.co.uk
v64hss83.vulnbegin.co.uk
vulnbegin.co.uk
vulnbegin.co.uk
```

Look at that a hidden subdomain, quick visit reveals flag no. 2

```
[^FLAG^XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX^FLAG^] 
```

OK the fuzz results came back, another directory

![env](./images/vulnbegin-10.png)

Yay another flag (no. 6), and an API token

![api key](./images/vulnbegin-11.png)