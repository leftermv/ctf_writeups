---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          . THM
# CTF NAME          . Capture!
# DESCRIPTION       . Can you bypass the login form?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/r/room/capture
```

- When inputting any credentials in the login form, we get the following message

```
**Error:** The user 'a' does not exist
```

- Assuming this flaw, I assume that if the username would've been correct, the message would be something like 'the password is incorrect'.

- We can enumerate using the usernames.txt first (provided by the room) to discover the username.

- Then, we could enumerate using that username to find out the password.

