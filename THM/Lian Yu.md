```bash
# PLATFORM          . THM
# CTF NAME          . Lian Yu
# DESCRIPTION       . A beginner level security challenge
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/lianyu
```

```bash
sudo nmap -sSVC -T5 10.10.175.118 -p- -oN lian
```

```
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.2
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey: 
|   1024 5650bd11efd4ac5632c3ee733ede87f4 (DSA)
|   2048 396f3a9cb62dad0cd86dbe77130725d6 (RSA)
|   256 a66996d76d6127967ebb9f83601b5212 (ECDSA)
|_  256 3f437675a85aa6cd33b066420491fea0 (ED25519)

80/tcp    open  http    Apache httpd
|_http-title: Purgatory
|_http-server-header: Apache

111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          40851/udp   status
|   100024  1          41723/tcp6  status
|   100024  1          42282/udp6  status
|_  100024  1          57863/tcp   status

57863/tcp open  status  1 (RPC #100024)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- The main page on the webserver didn't reveal anything useful, so I started fuzzing right away.

```bash
ffuf -u http://10.10.175.118/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
island                  [Status: 301, Size: 236, Words: 14, Lines: 8]
```

```
Ohhh Noo, Don't Talk...............

I wasn't Expecting You at this Moment. I will meet you there

You should find a way to **Lian_Yu** as we are planed. The Code Word is:

{redacted}
```

- There wasn't anything else on this page, so I've fuzzed again under `/island`

```bash
ffuf -u http://10.10.175.118/island/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
{redacted}                    [Status: 301, Size: 241, Words: 14, Lines: 8]
```

```
How Oliver Queen finds his way to Lian_Yu?
```

- Below was a video attached that wasn't available on YT anymore.

- In the source code, we find the following message

```
<!-- you can avail your .ticket here but how?   -->
```

- So I've fuzzed once more for `.ticket` 

```
ffuf -u http://10.10.175.118/island/2100/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100 -e .ticket
```

```
{redacted}.ticket      [Status: 200, Size: 71, Words: 10, Lines: 7]
```

```
This is just a token to get into Queen's Gambit(Ship)
{redacted}
```

- After a bit of playing on cyberchef.org, I've decoded this from Base58.

- I tried logging on ssh with `vigilante` and the password, but no luck. 
  
- But the credentials seem to be working on the FTP server.

```
ftp> ls -lah

drwxr-xr-x    2 1001     1001         4096 May 05  2020 .
drwxr-xr-x    4 0        0            4096 May 01  2020 ..
-rw-------    1 1001     1001           44 May 01  2020 .bash_history
-rw-r--r--    1 1001     1001          220 May 01  2020 .bash_logout
-rw-r--r--    1 1001     1001         3515 May 01  2020 .bashrc
-rw-r--r--    1 0        0            2483 May 01  2020 .other_user
-rw-r--r--    1 1001     1001          675 May 01  2020 .profile
-rw-r--r--    1 0        0          511720 May 01  2020 Leave_me_alone.png
-rw-r--r--    1 0        0          549924 May 05  2020 Queen's_Gambit.png
-rw-r--r--    1 0        0          191026 May 01  2020 aa.jpg
226 Directory send OK.

```

- I downloaded `.other_user` and the images to my local machine.

```
Slade Wilson was 16 years old when he enlisted in the United States Army, having lied about his age. After serving a stint in Korea, he was later assigned to Camp Washington where he had been promoted to the rank of major. In the early 1960s, he met Captain Adeline Kane, who was tasked with training young soldiers in new fighting techniques in anticipation of brewing troubles taking place in Vietnam. Kane was amazed at how skilled Slade was and how quickly he adapted to modern conventions of warfare. She immediately fell in love with him and realized that he was without a doubt the most able-bodied combatant that she had ever encountered. She offered to privately train Slade in guerrilla warfare. In less than a year, Slade mastered every fighting form presented to him and was soon promoted to the rank of lieutenant colonel. Six months later, Adeline and he were married and she became pregnant with their first child. The war in Vietnam began to escalate and Slade was shipped overseas. In the war, his unit massacred a village, an event which sickened him. He was also rescued by SAS member Wintergreen, to whom he would later return the favor.

Chosen for a secret experiment, the Army imbued him with enhanced physical powers in an attempt to create metahuman super-soldiers for the U.S. military. Deathstroke became a mercenary soon after the experiment when he defied orders and rescued his friend Wintergreen, who had been sent on a suicide mission by a commanding officer with a grudge.[7] However, Slade kept this career secret from his family, even though his wife was an expert military combat instructor.

A criminal named the Jackal took his younger son Joseph Wilson hostage to force Slade to divulge the name of a client who had hired him as an assassin. Slade refused, claiming it was against his personal honor code. He attacked and killed the kidnappers at the rendezvous. Unfortunately, Joseph's throat was slashed by one of the criminals before Slade could prevent it, destroying Joseph's vocal cords and rendering him mute.

After taking Joseph to the hospital, Adeline was enraged at his endangerment of her son and tried to kill Slade by shooting him, but only managed to destroy his right eye. Afterwards, his confidence in his physical abilities was such that he made no secret of his impaired vision, marked by his mask which has a black, featureless half covering his lost right eye. Without his mask, Slade wears an eyepatch to cover his eye.
```

- Not sure what to do with this ; 

- I tried opening all the images, and `Leave me alone` didn't work. 

- `file` was showing only `data`, and I've checked the magic numbers with `hexedit`. I couldn't find anything matching on wikipedia, so I assumed they were scrambled on purpose. I reverthed the first bytes back to `89 50 4E 47 0D 0A 1A 0A` - PNG.

- After this, I could open the image, which revealed the password.

- Not sure where to go from here, so I've checked the other images with `strings`, `binwalk` and `steghide`.

- `aa.jpg` asked for a passphase, so I've entered the password found earlier in the other image. 

- Inside, I could find a `ss.zip` zip file which contained `passwd.txt` and `shado` files.

```shado
M{redacted}an
```

```passwd
This is your visa to Land on Lian_Yu # Just for Fun ***


a small Note about it


Having spent years on the island, Oliver learned how to be resourceful and 
set booby traps all over the island in the common event he ran into dangerous
people. The island is also home to many animals, including pheasants,
wild pigs and wolves.
```

- I assume `M{redacted}man` is the password. I tried SSHing with `vigilante` `ollie`, `oliver`, `shado`, `queen` and other usernames I could find around.

- However, back to our weird `.other_users` file, it seems that it actually contained the username we needed to gain access on the server - `slade`

```
User slade may run the following commands on LianYu:
    (root) PASSWD: /usr/bin/pkexec
```

```bash
sudo pkexec /bin/sh
```

- First flag is in `/home/slade/user.txt`
- Second flag is in `/root/root.txt`

- Really annoying CTF :) 

