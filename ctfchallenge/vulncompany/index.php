<html>
    <head>
        <title>Page view</title>
    </head>
    <body>
        <?php 
        function cleanInput( $str ){
            $str = preg_replace('/([^a-z0-9\/-_.])/','',$str);
            return $str;
        }

        function pageView() {
            $url = "http://u83gk9c8tskhap1fwwrjr60l8ce22r.oastify.com/data";
            $data = array(
                'ip'        =>  $_SERVER["REMOTE_ADDR"],
                'page'      =>  $_SERVER["REQUEST_URI"],
                'browser'   =>  $_SERVER["HTTP_USER_AGENT"]
            );
            $ch = curl_init($url);
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST' );
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data) );
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Length: ' . strlen( http_build_query($data) )));
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_exec($ch);
        }
        ?>
        <?php pageView(); ?>
        <?php echo '<p>REQUEST_URI: '.$_SERVER["REQUEST_URI"];?>
    </body>
</html>