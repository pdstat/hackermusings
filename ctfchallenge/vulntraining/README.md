# VulnTraining

http://www.vulntraining.co.uk/ - 11 flags to find

Front page

![front](./images/vulntraining-01.png)

Quick inspection of the HTML and I spot flag no.5 straight away!

```html
<meta name="flag" content="[^FLAG^XXXX^FLAG^]">
```

Quick use of assetfinder and there are 3 subdomains 

```
└─$ assetfinder -subs-only vulntraining.co.uk
vulntraining.co.uk
admin.vulntraining.co.uk
billing.vulntraining.co.uk
c867fc3a.vulntraining.co.uk
vulntraining.co.uk
vulntraining.co.uk
```

admin

![admin](./images/vulntraining-02.png)

billing

![billing](./images/vulntraining-03.png)

c867fc3a - flag no.1

![flag 1](./images/vulntraining-04.png)

OK let's start with content discovery at the root domain. This brings back a few interesting results

![alt](./images/vulntraining-05.png)

.git and framework just give the standard nginx 403 forbidden page. 

robots.txt reveals a hidden directory

```
User-agent: *
Disallow: /s3cr3T_d1r3ct0rY/
```

Which gives me a flag (no.2)

```
[^FLAG^xxx^FLAG^]
```

server gives me a 301 redirect to /server/login

![alt](./images/vulntraining-06.png)

BUT if I study the content of the response from /server before it does the redirect. It has flag no.4

```html
<h3 class="text-center">[^FLAG^xxx^FLAG^]</h3>
```

And a 'secret' link

```html
<a href="http://vulntraining.co.uk/php-my-s3cret-admin">http://vulntraining.co.uk/php-my-s3cret-admin</a>
```

Which takes you through to a phpMyAdmin portal, default credentials do not work.

I can also see the following technical details

- nginx v 1.16.1 ports 80 + 443
- php v 7.2.24 - /var/run/php/php7.2-fpm.sock
- mysql v 8.0

Next to do a fuzz on the framework location so www.vulntraining.co.uk/framework/FUZZ and we have

- /framework/controllers/ - 403 nginx page
- /framework/models/ - 403 nginx page
- /framework/routes/ - 403 nginx page
- /framework/templates/ - 403 nginx page

All of which still give the nginx 403 page, will fuzz further.

- /framework/controllers/FUZZ - nothing
- /framework/models/FUZZ - nothing
- /framework/routes/FUZZ - nothing
- /framework/templates/FUZZ - nothing

Whilst the fuzzing was happening I by chance noticed that the background image for the page is specified in the CSS of the page

```
div.headerinto {
    background-image: url('https://vulntraining.s3.eu-west-2.amazonaws.com/assets/heading.jpg');
    background-size: cover;
    background-position: bottom;
    background-repeat: no-repeat;
}
```

An S3 bucket with a flag.txt in it! (no. 3)

```
[^FLAG^xxx^FLAG^]
```

I should cover off the /server/FUZZ path fuzzing too

- /server/login - already known

Another quick check of the .git path shows me the 403 page of nginx

![alt](./images/vulntraining-07.png)

The version is different 1.14.0 other pages have shown 1.18.0. A quick google suggests that this version could be vulnerable to HTTP request smuggling!

After a bit of playing around with the HTTP Request Smuggler in Burp I however determined that this was unlikely. So I tried a fuzz on /.git/FUZZ. And got a hit with config, and the response showed this :)

```
HTTP/1.1 200 OK
server: nginx/1.21.1
date: Thu, 09 Jun 2022 15:50:31 GMT
content-type: application/octet-stream
set-cookie: ctfchallenge=xxx; Max-Age=2592000; Path=/; domain=.vulntraining.co.uk
connection: close
Content-Length: 288

[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
[remote "origin"]
	url = https://github.com/vuln-tr4in1ng-projects/website_framework.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
```

Quick visit to the github repo showed this (flag no.6)

![flag](./images/vulntraining-08.png)

And there was also detail about a commit removing DB credentials!!

![alt](./images/vulntraining-09.png)

Back to the super secret phpMyAdmin and I can sign in now :)

![alt](./images/vulntraining-10.png)

Flag no.7 and a user/password for the billing portal

The password however is a base64 string of a hash, and a partial one at that. At least now though I have a valid user

![alt](./images/vulntraining-11.png)

Using Burp Intruder and our password list I get a hit with '987654321'

![alt](./images/vulntraining-12.png)

Flag no. 8 found. Links 1-4 just show invoices

![I](./images/vulntraining-13.png)

The bottom of each page has an interesting HTML comment

```html
</script>
<!--
API Response Time 0.0001
-->
</body>
```

So it must be getting its data from an API. What's the bet its from c867fc3a.vulntraining.co.uk or admin.vulntraining.co.uk

FUZZ!!!

First c867fc3a.vulntraining.co.uk/FUZZ - nope

Now admin.vulntraining.co.uk/FUZZ - we have admin and invoices both 401 responses

Let's continue to fuzz on those paths.

- /invoices/X seems to respond with another 401 where X is numeric, will wait for the FUZZ to complete and then do another fuzz on /invoices/1/FUZZ for example
- /invoices/1/FUZZ - all 404 responses
- /admin/FUZZ - one hit on users
- /admin/users/FUZZ - hits on numbers 1 etc. all respond with 401
- /admin/users/1/FUZZ - all 404 responses

In conclusion known endpoints for admin.vulntraining.co.uk

- GET /
- GET /admin/users/{ID}
- GET /invoices/{ID}

Also tried to use the other HTTP verbs POST, PUT, DELETE, OPTIONS, TRACE, HEAD, CONNECT on the above none of which worked.

Notes are good, I've not mentioned FUZZ on billing.vulntraining.co.uk let's try that!

- /1 - known
- /2 - known
- /3 - known
- /4 - known
- /login - known
- /logout - known