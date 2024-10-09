---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Commited
# DESCRIPTION       . One of our developers accidentally committed some sensitive code to our GitHub repository. Well, at least, that is what they told us...
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/commited
```

- We can check the different changes in the previous commits by using 

```
git log --stat -p
```

- However, we couldn't find anything useful for us.

- Then, I've decided to check if there are other branches in the repository 

```
git branch

  dbint
* master
```

- I switched to the `dbint` branch and reused the log command

```
git checkout dbint
git log --stat -p

Commit c56c470a2a9dfb5cfbd54cd614a9fdb1644412b5
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:46:39 2022 -0800

    Oops

diff --git a/main.py b/main.py
index 54d0271..0e1d395 100644
--- a/main.py
+++ b/main.py
@@ -4,7 +4,7 @@ def create_db():
     mydb = mysql.connector.connect(
     host="localhost",
     user="root", # Username Goes Here
-    password="flag{REDACTED}" # Password Goes Here
+    password="" # Password Goes Here

```

