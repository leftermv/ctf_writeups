- On the website we find a simple "ticketing" system.

- it asks for `name` and a `message`. once the `submit` button is pressed, there's a modification to the URL

```
http://ip/?name=asda&content=dsa
```

- By inspecting the source code of the page, we're able to identify a MD5 hash.

```
<!-- Our first bug was: d63af914bd1b6210c358e145d61a8abc. Please fix now! -->
```

- After being cracked, `d63af914bd1b6210c358e145d61a8abc` translates to `1628168161` in decimal.

- And here my brain decided to take a pause. I was stuck trying to isnert this number or hash in every way possible in the message and name forms, hoping that I can access that ticket and see the body.

- However, after a while, I decided to change the method used in the request using burpsuite

```
GET /?name=abc&content=de HTTP/1.1
```

to 

```
POST /?name=abc&content=de HTTP/1.1
```

- This has caused the internal server to throw an exception

```
# werkzeug.exceptions.BadRequestKeyError

werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand. KeyError: 'code'

## Traceback
```

- By taking a look in the `Traceback`, I found an interesting entry

```
File "/home/ctf/app.py", line _16_, in `index`
```

```
@app.route('/', methods=['GET', 'POST', 'PUT'])
    def index():
        if request.method == 'POST':
            code = request.form['code']
            if len(code) < 0:
                return "You should provide the code!"
                
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                rows = cur.execute("SELECT name, content FROM tickets WHERE code = ?", (code,)).fetchall()
```

- From this source code, I assumed I must use the `POST`method to send the `code`. Which I assumed was  the number I found in the source code.

- I wrote a python script to do this

```
#!/usr/bin/python
import requests
import hashlib

target = "http://IP"

code = 1628168161

while True:
    md5_code = hashlib.md5(str(code).encode()).hexdigest()
    req = requests.post(target, data={"code": md5_code})
    answer = req.text

    if("ctf" in answer):
        print(answer)
        break

    code += 1
```

- And ... it doesn't work as expected. But it does something.

```
<div class="row">
    <hr>
	    <p>Name: Nice one</p>
	    <p>Message: ctf{Try harder!}</p>
    <hr>
</div>
```

- That's what I found in the answer. Unfortunately, I had no idea what to do now. I assumed it had something to do with the value used, but I didn't knew what.

- So I was stuck here for a while. 

- Then, I found another writeup in which `162` was added to the initial value, `1628168161`. Why? No idea. But it works.

- If we modify this line 

```
code = 1628168161
```

to 

```
code = 1628168161 + 162
```

```
<div class="row">
    <hr>
        <p>Name: Nice one</p>
        <p>Message: ctf{{redacted}}</p>
    <hr>
</div>
```

- it works and i'm confused. to be updated once i find the explanation :) 
