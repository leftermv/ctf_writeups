- We're given a `.pyc` file, which is `compiled python`.

- After a bit of research, I've found out that we can use the `uncompyle6` module to decompile the file.

**NOTE**: I encountered some compatibility problems which I will explain below, after I walk through the steps needed to get the flag.

- Create a python3.7 (earlier versions of python works too) environment: `python3.7 -m venv /path/to/venv`

- install `uncompyle6` module: `pip install uncompyle6`

- `uncompyle6 -o . chall.pyc` will create a `chall.py` file with the decompiled code.

**TIP:**
- `uncompyle6 chall.pyc` will print the decompiled code to the terminal ; no `.py` file created.

**NOTE**: if you're using python 3.x, modify the print syntax by adding `()` and `input()` has to be used instead of `raw_input()`. 

- The source code reveals the password needed to retrieve the flag, as well as the strings that the flag is made of.

![[Pasted image 20231212220137.png]]

**TIP**: `strings` can be used also to reveal the bits of the flags, but they're not in the correct order. 

- Password can be seen in strings output too.

___

**COMPATIBILITY PROBLEMS**

- `uncompyle6` requires max `python 3.7.16` or earlier.

- I had to compile `python3.7.16` from the source code.

- A summary of the steps are below

```bash
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev -y

wget https://www.python.org/ftp/python/3.7.16/Python-3.7.16.tar.xz

tar -xf Python-3.7.16.tar.xz

# assuming the Python-3.7.16 folder has been moved to /usr/local/share/python3.7

cd /usr/local/share/python3.7
./configure --enable-optimizations --enable-shared

make 
# or make -j <threads_number> for faster compilation.

sudo make altinstall 
# don't overwrite default python binary on the system

sudo ldconfig /usr/local/share/python3.7

python3.7 --version
# should output Python 3.7.16

#create python3 venv
python3.7 -m venv /path/to/venv
```
