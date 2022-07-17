# VulnCorp

http://www.vulncorp.co.uk - 9 flags to find

![alt](./images/vulncorp-01.png)

OK usual trick of checking subs first

```
└─$ assetfinder -subs-only vulncorp.co.uk
www.vulncorp.co.uk
vulncorp.co.uk
vulncorp.co.uk
vulncorp.co.uk
```

So nothing with assetfinder, a fuzz with the subdomain word list did however bring back 3

- chat.vulncorp.co.uk
- prueba.vulncorp.co.uk
- webmail.vulncorp.co.uk

All of which redirect to their own login screens. OK so lets focus on the main domain for now. Quick content discovery reveals

- /meet-the-team
- /contact
- /admin
- /phpmyadmin

OK lets go through those 1 by 1

## Meet the team

![alt](./images/vulncorp-02.png)

First thing that pops out to me here is that the images are of the form /images/staff_photo_x where x is 1-10. So are there more hidden images in that directory? Quick test and no a range of 0-100 still only brings back 200 OK responses for 1-10

## Contact

![alt](./images/vulncorp-03.png)

Submitting the form gives the message

```
Error posting to message server, subscription expired
```

## Admin

![alt](./images/vulncorp-04.png)

The link points at the github repo https://github.com/template-manager/template-manager. Here's the readme contents of that

```
template-manager

Template manager is a basic system built in PHP which can be used to build your website and translate URL's to templates.

It also comes with an admin interface to control plugins

When installing this product it will need write access to the project root directory to save config file with database settings.
```

So a few interesting findings straight away in here

## sql-setup.php

```php
<?php

$sql_cmd = array();
$sql_cmd[] = "CREATE TABLE page ( id int(11) NOT NULL, url varchar(250) NOT NULL, template varchar(250) NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=latin1;";
$sql_cmd[] = "ALTER TABLE page ADD PRIMARY KEY (id);";
$sql_cmd[] = "ALTER TABLE page MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;";
$sql_cmd[] = "INSERT INTO page (url, template) VALUES ('/', 'home')";
$sql_cmd[] = "CREATE TABLE user (id int(11) NOT NULL,username varchar(50) NOT NULL,password varchar(32) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;";
$sql_cmd[] = "ALTER TABLE user ADD PRIMARY KEY (id);";
$sql_cmd[] = "ALTER TABLE user MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;";
```

So we know the DB tables

## /admin_template/admin.php

```php
function adminLogin( $username, $password ){
    $resp = false;
    $d = Db::get()->prepare('select * from user where username = ? and password = ? LIMIT 1 ');
    $d->execute( array( $username, md5( $password ) ) );
    if( $d->rowCount() == 1 ){
        $resp = true;
    }
    return $resp;
}

if( isset($_POST["username"],$_POST["password"]) ){
    $login_error = true;
    if( $login = adminLogin($_POST["username"],$_POST["password"]) ){
        $challenge = md5(rand().date("U").print_r( $_SERVER, true ).print_r( $_POST, true ).rand());
        $auth = md5( $challenge.'s4cre4log1nStinG4T3mpl4tem4Ngaer' );
        $str = json_encode( array(
            'challenge'  =>  $challenge,
            'auth'       =>  $auth
        ));
        $hash = base64_encode(urlencode($str));
        setcookie('token',$hash,time()+3600,'/');
        header("Location: /admin/dashboard");
        exit();
    }
}
```

So the adminLogin function just returns a boolean response on username/password match, this is a prepared statement so no SQLi here. It then creates a token cookie which is based upon an encoded JSON array with a challenge md5 hash (made up of a random int, the linux epoch date, server info and post request info) and an auth string which an md5 hash of the challenge plus the string 's4cre4log1nStinG4T3mpl4tem4Ngaer'. After that it does a redirect to /admin/dashboard.

## /admin_template/dashboard.php

```php
if( isset( $_COOKIE["token"] ) ){
    $json = json_decode( urldecode(base64_decode($_COOKIE["token"])), true );
    if( gettype($json) == 'array' ){
        if( isset($json["challenge"],$json["auth"]) ){
            if( $json["auth"] ==  md5( $json["challenge"].'s4cre4log1nStinG4T3mpl4tem4Ngaer' ) ){
                $logged_in = true;
                setcookie('token',$_COOKIE["token"],time()+3600,'/');
            }
        }
    }
}
if( !$logged_in ){
    header("Location: /admin");
    exit();
}
```

The dashboard page checks for the presence of this token cookie and that its value is correct before we are allowed to proceed. If not it redirects back to the login admin page.

## /admin_template/install.php

```php
function createConfigFile( $db_host, $db, $db_user, $db_pass ){
    $myfile = fopen(getcwd()."/../".date("YmdH").".cfg", "w");
    fwrite( $myfile,"DB_HOST=".$db_host.PHP_EOL."DB_DB=".$db.PHP_EOL."DB_USER=".$db_user.PHP_EOL."DB_PASS=".$db_pass);
    fclose($myfile);
}
if( isset( $_POST["db_server"],$_POST["db_db"],$_POST["db_user"],$_POST["db_pass"],$_POST["username"],$_POST["password"] ) ){
    if( $pdo = Db::checkDb( $_POST["db_server"],$_POST["db_db"],$_POST["db_user"],$_POST["db_pass"] ) ){
        Db::setup( $pdo, $_POST["username"], $_POST["password"] );
        createConfigFile(  $_POST["db_server"],$_POST["db_db"],$_POST["db_user"],$_POST["db_pass"] );
        header("Location: /admin");
    }
}
```

So this seems to be writing a config file with the DB details in it, the name of the config file takes a date format eg. '2022071706.cfg'. Perhaps this config file still exists?

And yes it does :) (2019100213.cfg) - here's flag 1

```
DB_HOST=localhost
DB_DB=vulncorp_www
DB_USER=vulncorp_www
DB_PASS=sezk87mjd3u7wp0p

[^FLAG^xxx^FLAG^]
```

This allows me in to phpmyadmin

![db](./images/vulncorp-05.png)