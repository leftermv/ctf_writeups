- we're given a .zip file containing a .jpg image.  

- the file can't be opened, but we're lucky : we are given a hint.  

```
BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB
BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB 
BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB BBBBBBBBBB
```

Let's try replacing the `BBBBBBBBBB` in the file binary data.  

To do that, I've chosen to use python.

```bash
#!/usr/bin/env python3

with open('chall.jpg', 'rb') as img:                        # open the .jpg file in 'read binary' mode
  binary_data = img.read()                                  # read the data and save it into a variable
  
data = binary_data.replace(b'BBBBBBBBBB', b'')              # replace the 10-B's sequence with nothing. 

with open('ihopethisworks.jpg', 'wb') as img:               # open (and create, in this case) a new .jpg file
  img.write(data)                                           # write the resulted data into this file.
```

We're able to open this image and obtain the flag.  

FLAG: TFCCTF{the_{REDACTED}w4y}


