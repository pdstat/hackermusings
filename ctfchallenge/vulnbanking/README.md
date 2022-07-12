# VulnBanking

http://www.vulnbanking.co.uk - 4 flags to find

![alt](./images/vulnbanking-01.png)

OK let's check subdomains first

```
└─$ assetfinder -subs-only vulnbanking.co.uk
vulnbanking.co.uk
hostmaster.vulnbanking.co.uk
```

OK so just the one, let's check that out later. For now just some content discovery

So doing a content fuzz on http://www.vulnbanking.co.uk/FUZZ gives the following

- /css/
- /js/
- /logout/

So not much. Just checking out the resources and links on the page however leads another couple of potential paths to check out.

First off there is inline javascript included 

```javascript
$('input.auth').click( function(){
    $.post('/api/login',{
        customer_number :   $('input[name="customer_number"]').val(),
        password        :   $('input[name="password"]').val()
    },function(resp){
        alert('Login Successful');
        window.location = '/session/' + resp.token;
    }).fail(function(){
        alert('Customer Number / Password combination invalid');
    })
});
```

And the login help link. So now I have a few extra things to check out

- /api/login - perhaps additional api endpoints to discover?
- /session/token - where token is some token received from a successful login
- /template-manager - the main style.css is loaded from this location. 
- /login-help - link on the login page

The template manager has another login form associated with it and its own app.js file

```javascript
templateManager = function (t) {
  for (ApiFire = function (t, e) {
    xhttp = new XMLHttpRequest,
    xhttp.open('POST', t, !0),
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'),
    xhttp.send('value=' + e)
  }, ApiCall = function (t) {
    console.log(t),
    url = '/template-manager/api/set-' + t,
    v = document.getElementById('val').value,
    ApiFire(url, v)
  }, i = 0; i < t.length; i++) try {
    document.getElementById(t[i]).addEventListener('click', function (t) {
      ApiCall(t.srcElement.id.replace('btn-', ''))
    })
  } catch (t) {
  }
}(['btn-background-color',
'btn-font-type',
'btn-font-color',
'btn-font-size']);
```

OK so template manager has another API.

The login help has another form associated with it

![alt](./images/vulnbanking-02.png)

So starting at the top of the last set of content I found and doing a fuzz on http://www.vulnbanking.co.uk/api/FUZZ, I get one additional result back

- logs

Which gives me a json array of logs

```json
[{"date":"Tue, 12 Jul 2022 14:36:40 +0000","endpoint":"\/api\/login",...,"result":"success","flag":"[^FLAG^xxx^FLAG^]"},...,"auth_hash":"597b45bd3e7f72c74d9b93435037eae7","result":"fail"}]
```

Flag no.2 found