- Download the image attached. It's a survey about the most used weak passwords / credentials.

- This might be a sublime hint that we might need to guess one of the most 'used' passwords.

- I ran `steghide --extract -sf ` against the file and it asked for a passphase, which I didn't had.

- Running `stegcracker file /usr/share/wordlists/rockyou.txt` reveals the passphase used and extracts the data to `filename.out`. 

- This file holds the flag.

