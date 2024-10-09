---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Neighbour 
# DESCRIPTION       . Check out our new cloud service, Authentication Anywhere. Can you find other user's secrets?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/neighbour
```

- The login page is suggesting that we can use a `guest account` and indicates us to use CTRL + U

- By doing so, we end up in the source code where the following is revealed

```
<!-- use guest:guest credentials until registration is fixed. "admin" user account is off limits!!!!! -->
```

- After logging in as user, we see the URL looking like this

```
http://10.10.206.181/profile.php?user=guest
```

- This is a very basic IDOR vulnerability and the admin flag can be revealed by using the following URL

```
http://10.10.206.181/profile.php?user=admin
```

