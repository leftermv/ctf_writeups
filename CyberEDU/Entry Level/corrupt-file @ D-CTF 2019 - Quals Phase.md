- we given `flag.docx.zip` ; 

- `unzip flag.docx.zip` will result in `flag.docx`.

- However, look at the results of `file flag.docx`

```
flag.docx: XZ compressed data, checksum CRC64
```

- I've renamed the file to `flag.docx.xz` and used `xz -d flag.docx.xz` to decompress it.

- This time, `file flag.docx` returns `POSIX tar achive`

- Rename the file to `flag.tar` and decompress using `tar xf flag.tar`.

- We're given a `flag.txt` containing the flag.
