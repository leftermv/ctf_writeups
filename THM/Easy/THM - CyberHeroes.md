---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . CyberHeroes
# DESCRIPTION       . Want to be a part of the elite club of CyberHeroes? Prove your merit by finding a way to log in!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/cyberheroes
```

- I've started the CTF by checking webpage running on the server. Here I found the following goala

```
find the vuln on our login page and login to join us. :D
```

- On the login page's sourcec code the following function was found

```javascript
<script>
    function authenticate() {
      a = document.getElementById('uname')
      b = document.getElementById('pass')
      const RevereString = str => [...str].reverse().join('');
      if (a.value=="h3ck3rBoi" & b.value==RevereString("{REDACTED}")) { 
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            document.getElementById("flag").innerHTML = this.responseText ;
            document.getElementById("todel").innerHTML = "";
            document.getElementById("rm").remove() ;
          }
        };
        xhttp.open("GET", "RandomLo0o0o0o0o0o0o0o0o0o0gpath12345_Flag_"+a.value+"_"+b.value+".txt", true);
        xhttp.send();
      }
      else {
        alert("Incorrect Password, try again.. you got this hacker !")
      }
    }
  </script>
```

- the credentials are hardcoded in the if statement

- The flag can be retrieved by logging in as `h3ck3rBoi` and the reverse of the value found as argument for the RevereString function.

P.S: can also be accessed by going to `http://10.10.71.165/RandomLo0o0o0o0o0o0o0o0o0o0gpath12345_Flag_h3ck3rBoi_S{REDACTED}5.txt`

```
Congrats Hacker, you made it !! Go ahead and nail other challenges as well :D flag{{REDACTED}} 
```