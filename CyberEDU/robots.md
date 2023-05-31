# Robots


This task is very trivial and the most important hint is given in the CTF's name : robots.   
All we have to do is to navigate to /robots.txt to reveal the flag.  

```
User-agent: *
Disallow: /g00d_old_mus1c.php
```

We see that the `g00d_old_mus1c.php` is not crawlable, but we have access to that page.  

The flag is CTF{Kr4{REDACTED}0ts}
