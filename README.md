# Exploit HTTP Host Header
This just is a simple script to check what server response when get infected HTTP-header.

[More about HTTP Host header attacks](https://portswigger.net/web-security/host-header)

Note: **It's just an alpha version, so bugs will be :)** 

## Install

```bash
git clone https://github.com/run-byte-run/ehhh.git
cd ./ehhh
pip install -r requirements.txt
```

## Usage
So let's try to solve [this lab.](https://portswigger.net/web-security/host-header/exploiting/lab-host-header-authentication-bypass) 
```bash
python ehhh.py --url https://31fda3e5180d68.web-security-academy.net/admin
```
Console output will be like:
```console
Ehhh just run...
Module "lib.attacks.add_line generate task.
Module "lib.attacks.bruteforce generate task.
Module "lib.attacks.flawed generate task.
Module "lib.attacks.x_header generate task.
Task "BruteForceEhhhAttackTask" with "host: localhost" may be vulnerability!
```
So that means if we replace Host-header to `Host: localhost` response will change. Try it out ;)   