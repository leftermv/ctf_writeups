---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Confidential
# DESCRIPTION       . We got our hands on a confidential case file from some self-declared "black hat hackers"... it looks like they have a secret invite code.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/confidential
```

- The PDF contains a QR code that is overlapped by another image, so we can't scan it.

- The CTF is booting on THM's attack box and I don't like working there ; plus, I don't have the tools required installed.

- I've transfered the file to my host using netcat

```bash
# my host
nc -l -p 3131 > pdf.pdf

# attackbox
nc -N my_IP 3131 < pdfname.pdf 
```

- I treid using the common tools like `exiftool`, `binwalk`, `strings`, `pdfinfo` but with no luck.

- I came across `pdfimages` while googling for tools that might help and the syntax is as follows

```
pdfimages -all pdf.pdf extracted
```

```bash
ls
extracted-000.png  extracted-001.png  extracted-002.png
```

- `extracted-000.png` contains the QR code and can be scanned to get the value.