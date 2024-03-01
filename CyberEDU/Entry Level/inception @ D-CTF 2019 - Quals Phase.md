- the `chall.jpeg.zip` can be unzipped using `unzip chall.jpeg.zip`

- the result is a `jpeg` image that contains a `png` image

- this can be seen by running `binwalk -e chall.jpeg`.

- to extract the data, I've used `binwalk --dd '.*' chall.jpeg` 

- the resulted image is a QR code that I've found easy to read with `zbarimg 1B16B` (1B16B = filename)

**NOTE**: the tool can be installed on Debian based distros with `apt install zbar-tools`

- After reading the QR data, we're given the flag.

```
zbarimg 1B16B 

QR-Code:DCTF{394a6{REDACTED}b07f0}
scanned 1 barcode symbols from 1 images in 0.03 seconds
```