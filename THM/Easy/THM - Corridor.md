```bash
# PLATFORM          . THM
# CTF NAME          . Corridor
# DESCRIPTION       . Can you escape the Corridor?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/corridor
```

- The doors on the main page are all clickable. 

- When clicked, the URL address of each page displays a hash-like format, so I decided to grab one and crack it.

- It was the MD5 hash of "1". 

- I made a list of all the hashes 
	- grab them by clicking on each door
	- or by inspecting the source code of the page

- After cracking, they're the hashes of numbers `1`, `2`, `3` and so on until `13`.

- So I have hashed the number `14` and went to that directory, but I got a `Not Found` message. Then, I tried with `0` and I found the flag.

```bash
echo -n "0" | md5sum
```

```bash
curl http://ip/hash_from_above | grep flag
```

