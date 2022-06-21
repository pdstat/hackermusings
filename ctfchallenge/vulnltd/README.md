# VulnLtd

http://www.vulnltd.co.uk/ - 7 flags to find

![alt](./images/vulnltd-01.png)

So this is the front page, not a lot, no custom js just jQuery and Bootstrap and a link to a contact page.

Which has a form

![alt](./images/vulnltd-02.png)

Which when you submit the form we get a message back saying

```
Your slack token has expired
```

Note there's nothing in the request that looks like a token

```
POST /contact HTTP/1.1
Host: www.vulnltd.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
Origin: http://www.vulnltd.co.uk
Connection: close
Referer: http://www.vulnltd.co.uk/contact
Cookie: ctfchallenge=xxx
Upgrade-Insecure-Requests: 1

name=sss&email=sss&message=ssss
```

OK fine lets start the usual enumeration starting with any subdomains we might find.

Nothing with assetfinder

```
└─$ assetfinder -subs-only vulnltd.co.uk
vulnltd.co.uk
vulnltd.co.uk
vulnltd.co.uk
```

So lets use the subdomain wordlist. And..... I get a hit with support.vulnltd.co.uk

Which gives me some support ticket search form

![alt](./images/vulnltd-03.png)

Which just tells me could not find ticket when it's submitted, this is the request which gets sent

```
POST / HTTP/1.1
Host: support.vulnltd.co.uk
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 14
Origin: http://support.vulnltd.co.uk
Connection: close
Referer: http://support.vulnltd.co.uk/
Cookie: ctfchallenge=xxx
Upgrade-Insecure-Requests: 1

ticket_ref=sss
```

OK I'm going to leave this for now and come back to it. Time to do some content discovery with fuzzing on www.vulnltd.co.uk/FUZZ

And yup get a hit with robots.txt

```
User-agent: *
Disallow: /secr3t_l0g1n/


# [^FLAG^XXX^FLAG^]
```

Flag 1 :). The secret path takes me through to this login form

![alt](./images/vulnltd-04.png)

The docs give me some info to look at

![alt](./images/vulnltd-05.png)

OK so lets login to the CMS as guest with a password which is probably monday-sunday :D

And yes, tuesday gets me in

![alt](./images/vulnltd-06.png)

Clicking on one of the links which takes the format /page/x (where x is a number) just tells me

```
Guest users cannot edit pages
```

I have a similar issue if I click on the new page link

```
Guest users cannot create pages
```

And trying to sign in to the slack workspace with my own account just tells me no

![alt](./images/vulnltd-07.png)

However... look at this cookie!

![alt](./images/vulnltd-08.png)

Change it to true and I get another flag (no. 2) when I refresh the page :)

![alt](./images/vulnltd-09.png)

I can now edit and create pages, having a look at the draft contact page I can spot some PHP code at the top which is interesting

```php
<?php
/**
 * We've dropped slack for receiving contact messages for the website and we're only going to use it for company communications only.
 * This will now send an to email start-ticket@vulnltd.co.uk which will create a support ticket which links in with our support desk app.
 */
$sent_message = false;
$message_error = false;
if( isset($_POST["name"],$_POST["email"],$_POST["message"]) ){
    $sent_message = true;
    try{
        $message = \Model\Email::send('start-ticket@vulnltd.co.uk',$_POST["email"], 'Support Message', 'Name: '.$_POST["name"].' Message: '.$_POST["message"]  );
    }catch (Exception $e ){
        $message_error = 'Error sending Email';
    }
}
?>
```