<img src="latte.png" width="150px" height="150px" alt="Latte's logo" />

# Latte

`apt-get` for Pythonista.

*NOTE:* _Latte's docs are now in [this](https://github.com/sn3ksoftware/Latte/wiki) wiki. Go check it out!_

## What's The Point?

When I was using [StaSh](https://github.com/ywangd/stash) on Pythonista, I found it really annoying that I had to constantly run self-extracting Python scripts to install various add-ons and commands for StaSh. Because of that, I decided to create a simple utility that allows the creation, hosting, and sharing of software without hassle.

Now users of StaSh can easily communicate their software to other users. No more transfer problems.

_Latte_ is also a platform for easily creating your own commands for StaSh. It allows you to install packages that install programs to StaSh's `stash_extensions/bin` directory. Now you can create your own commands!

## Installing

_Latte_ supports these platforms right now:

- [x] Libterm
- [x] StaSh (on Pythonista)
- [ ] Generic Linux/GNU

### StaSh (Pythonista)
If StaSh is not installed already, install StaSh first with:

```python
import requests as r; exec(r.get('https://bit.ly/get-stash').text)
```

To install _Latte_ to Pythonista, copy the below code, go to your Pythonista line-interpreter (the panel that swipes over on the right, that lets you type in Python code line-by-line), and paste the code, and run it. This should run the installer program provided in the repository. Once it starts running, you should start seeing your new package manager being installed to your StaSh.

```python
import requests as r; exec(r.get("https://raw.githubusercontent.com/sn3ksoftware/Latte/master/installer.py").text);
```

### LibTerm
Copy and paste the below code to your terminal:

```
curl -O https://raw.githubusercontent.com/sn3ksoftware/Latte/master/installer.py
python installer.py
```

## Repositories

_Latte_ uses [this](https://github.com/sn3ksoftware/latte-universe) repository for packages by default

(with nickname **universe**).

## Getting Started

If you want to learn how to properly use Latte, you can head over to the [wiki](https://github.com/sn3ksoftware/Latte/wiki). There's plenty of information over there to get you started!
