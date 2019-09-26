title: A Network Engineer's Guide to the Linux CLI 1st Edition
category:
- Route/Switch
author: Brandon James
summary: 


I am a huge fan of Linux[^1]. In the office, most of my real work happens on my Red Hat jumpbox. At home, my personal machines run Fedora and this website is hosted on Ubuntu. One of my favorite things about working with Cisco devices is the great CLI, Linux provides an even better experience for general purpose computing. 

This is meant to be a living document with regular updates. You are reading the first edition of the document, which contains what I believe to be essential knowledge for effective Linux CLI use. 

# Index

* [The Unix Philosophy](#the-unix-philosophy)
* [Man Pages](#man-pages)
* [Navigation](#navigation)
* [Pagers](#pagers)
* [Searching with grep, locate and which](#searching-with-grep-find-locate-and-which)
	- [grep](#grep)
	- [locate](#locate)  
	- [which](#which)
* [SSH](#openssh)
* [Vim](#vim)
* [.bashrc and .profilerc](#.bashrc-and-.profilerc)
* [Change Log](#change-log)
* [Queue](#queue)

## The Unix Philosophy

Linux falls under the "Unix-like" class of operating systems, all of these operating systems roughly follow something known as the Unix Philosophy. The Unix Philosophy has a long and somewhat storied history that you can read about in the first Chapter of [*The Art of Unix Programming* by Eric Steven Raymond](http://www.catb.org/~esr/writings/taoup/html/ch01s06.html). While the book is geared towards programmers, understanding the Unix philosophy is sure to make you a better user of Linux as well. The Unix Philosophy isn't meant to be a set of strict rules and instead should be thought of as a list of best practices.

I think of the following quote[^2] from Doug McIlroy when I think of the Unix Philosophy:

i) Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new features.

ii) Expect the output of every program to become the input to another, as yet unknown, program. Don't clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don't insist on interactive input.

iii) Design and build software, even operating systems, to be tried early, ideally within weeks. Don't hesitate to throw away the clumsy parts and rebuild them.

iv) Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them.

From the perspective of a Linux user, I think it's important to keep the first two in mind. Realizing that the Linux CLI consists of not just commands, but a collection of small programs that can act as input to each other is the first step to Linux mastery.

## Man Pages

All the commands that you run on the Linux CLI are separate programs[^3], most of these commands have listings in the system manual. To view a man page, simply type `man <utility>` where utility is the name of the command or tool you want to know more about. The `man` program itself even has a man page, type `man man` to try it out. If for some reason you can't find the `man` page you are looking for you can use `man -k <keyword>` to get a list of `man` pages containing a specific keyword. To search within a man page, you can pipe `man` into [`grep`](#grep) such as `man man | grep -n EXAMPLES` to find the line number where the examples section begins. 

In addition to being a quick way to view manual entries, the `man` program belongs to a class of CLI programs called [pagers](#pagers). Pagers give you a way to view the entire contents of a file without the need for a scrollbar. With `man` you can move up and down with `j` and `k`, skip forward a screenful with the spacebar, jump to a specific line number by typing it and pressing enter or search for a string with `/<string>`. 

As you read this guide, I encourage you to skim the man pages for the utilities I mention. 

## Navigation

* A few general notes on the Linux directory layout.

	i) The root of the Linux filesystem is `/` or the root directory (not to be confused with the root user). This is not quite the same as being in the root of the C:\\ drive on a Windows machine. In Linux, all drives are mounted under the root filesystem. 

	ii) All users have a home directory, it traditionally resides under `/home/<username>`. The `~` symbol refers to the current users home directory.

	iii) Files and folders can be referenced by either absolute or relative paths. 

	 	 * An absolute path is when you refer to the file or folder by it's full path starting at the root directory. As an example, if you have a folder called 'scripts' in your home directory the absolute path to a script within that directory is `/home/bjames/scripts/update_files.sh`. 
	 
	 	 * There a couple ways to refer to a file or folder by relative paths
	 
	 		1) Referencing the file or folder without a preceding `/` uses your current working directory as the base directory. Using the script above, the relative path from your home directory would be `scripts/update_files.sh`

     		2) Linux provides two useful shortcuts for relative paths 
     	
     			* When within a folder, you can refer to the folder as `.`. Again, from our home folder `./scripts/update_files.sh` or from the scripts folder `./update_files.sh` are both relative paths to the update_files.sh script.

	 			* `..` refers to the parent directory. As an example, let's say the absolute path of your working directory is the scripts folder from above, `/home/bjames/scripts/`. If you needed to access notes.txt stored in your home directory, you could do so with the following relative path: `../notes.txt`. Note that you can use `..` multiple times in a single path. For instance `../../` refers to `/home/`.

* `ls` Lists the contents of the current directory. It can be combined with arguments like `ls -l` to format the output as a list, `ls -a` to include hidden files in the output or `ls -h` to print the file size in a human readable format. Arguments can also be stacked, for example `ls -lah` formats the output as a list, includes hidden files and uses human readable file sizes. Many Linux flavors alias `ls -lah` to `ll`, which means running the command `ll` actually runs `ls -lah`. 
```
[bjames@lwks1 Documents]$ ls -lah
total 183M
drwxr-xr-x.  8 bjames bjames 4.0K Sep  8 17:24  .
drwx------. 36 bjames bjames 4.0K Sep  8 17:23  ..
drwxrwxr-x.  2 bjames bjames 4.0K Jul 12 13:51  ACI
-rw-------.  1 bjames bjames 230K Sep  7 00:10 'LISP - edit.aup'
drwxrwxr-x.  3 bjames bjames 4.0K Sep  4 21:20 'LISP - edit_data'
-rw-rw-r--.  1 bjames bjames  12M Sep  4 23:42  LISP.mp3
drwxrwxr-x. 12 bjames bjames 4.0K Aug 18 16:27  notes
-rw-rw-r--.  1 bjames bjames  53M Sep  5 15:45  output2.mkv
-rw-rw-r--.  1 bjames bjames 118M Sep  5 15:41  output.mkv
-rw-rw-r--.  1 bjames bjames 108K Jul 12 16:36  UA_TRAILRUN_50K_TRAINING_PLAN_2018.pdf
drwxrwxr-x.  6 bjames bjames 4.0K Jul 12 10:57  Zoom
```

* `pwd` Prints the path of the current working directory
```
[bjames@lwks1 Documents]$ pwd
/home/bjames/Documents
```

* `cd` Changes the working directory. `cd ~` or just `cd` by itself takes you to your home directory. You can `cd` using absolute paths `cd /var/log/`. You can also `cd` using relative paths `cd scripts` takes you to scripts or `cd ../notes` takes you to the sibling folder `notes`. 

That covers the basics of navigating on the Linux CLI. Here's an example putting it all together. 

i) We start out in my home directory, which contains 12 folders and no files.
```
[bjames@lwks1 ~]$ pwd
/home/bjames  
[bjames@lwks1 ~]$ ls
Desktop    Downloads  Pictures  Public  Templates  Videos
Documents  Music      Projects  snap    tmp
```

ii) From there we `cd` to my Projects folder using a relative path 
```
[bjames@lwks1 ~]$ cd Projects/
[bjames@lwks1 Projects]$ ls
neverthenetwork
```

iii) If we want to go to my Videos folder, we can do so in a few ways. Three are shown below:

	 1) Returning to the parent folder and then navigating to the Video folder, both using relative paths.
```
[bjames@lwks1 Projects]$ pwd
/home/bjames/Projects
[bjames@lwks1 Projects]$ cd ..
[bjames@lwks1 ~]$ cd Videos/
[bjames@lwks1 Videos]$ pwd
/home/bjames/Videos
``` 
	 2) The absolute path
```
[bjames@lwks1 Projects]$ cd /home/bjames/Videos/
[bjames@lwks1 Videos]$ pwd
/home/bjames/Videos 
```
	 3) A single relative path
```
[bjames@lwks1 Projects]$ cd ../Videos/
[bjames@lwks1 Videos]$ pwd
/home/bjames/Videos
```

## Pagers

If you've read many linux guides, you've probably seen someone use `cat file.txt` to print the content of a file to the screen. This does work, but there is a much better solution. `more` and `less` both belong to a class of programs known as pagers. Pagers work by breaking files into pages or screenfuls of data so you don't need to scroll back up to see the rest of your file. The two programs operate similarly, but do have a few differences. 

* `less` - Operates similarly to `vi` and allows forward and backward movement through the file. The output of the file is not copied to your scrollback buffer[^5]. 
	* Basic navigation `[space]` - Move forward one screenful, `j` move forward one line, `k` move backward one line, `q` quit
	* The pager used by `man` operates similarly to less
	* `less file.txt`
* `more` - Much simpler than `less`
	* Basic navigation [space] - Move forward one screenful
	* `more file.txt`
	
Read the man pages (`man less` and `man more`) for *more* on both of these. 

## Searching with grep, locate and which

### grep

`grep` is used to find strings matching a pattern within a file. In the most basic case, you might use `grep` to search for a specific string within a file:

```
[bjames@lwks1 pages]$ grep "specific string" linux_intro.md
Grep is used to find strings matching a pattern within a file. In the most basic case, you might use grep to search for a specific string within a file:
```

However, the real power of `grep` lies in regular expressions. Current versions of `grep` support three *flavors* of regex. They are standard `grep` regex, extended `grep` regex and perl regex. I find myself using extended `grep` for most things. In the below example, we use extended regular expressions to find IP addresses within this markdown file. 

```
[bjames@lwks1 pages]$ grep -nE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' linux_intro.md
175:[bjames@lwks1 ~]$ ssh 172.16.12.1
176:172.16.12.127  172.16.12.130  172.16.12.132  172.16.12.137  
177:[bjames@lwks1 ~]$ ssh 172.16.12.127 | tee logfile.log
<redacted for brevity>
262:RSA host key for 192.168.88.1 has changed and you have requested strict checking.
267:[bjames@lwks1 ~]$ ssh-keygen -R 192.168.88.1
268:# Host 192.168.88.1 found: line 10
```

__Note:__ in the above output, I also included the `-n` argument, this tells `grep` to print the line number the match was found on. Also note the regex above won't only find valid IPs, for instance 999.999.999.999 is not a valid IP, but would be considered a match. The regex to only match valid IPs is significantly more complicated. When using `grep` it's generally best to use regex that's good enough to find what you are looking for.

In addition to searching a single file, `grep` can be used to search multiple files using either a wildcard such as `grep <pattern> *.log`, a single directory `grep <pattern> ~/logs/` or a directory and it's subdirectories `grep -r <pattern> ~/logs/` (here the `-r` argument stands for recursive). 

```
[bjames@t470s pages]$ grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' *.md
automation_concurrency.md:192.168.1.100
automation_concurrency.md:192.168.10.0
<redacted for brevity>
wlc_cli.md:192.168.0.20
wlc_cli.md:192.168.1.20
```

__Note:__ Above we found every IP address, subnet mask or wildcard mask used in any NTN article. In addition to the `-E` argument, I used `-o` which tells `grep` that we want the matching part of the line only.

`grep` can also be used with pipes to search the output of another file `<command> | grep <pattern>`

```
[bjames@t470s pages]$ ls -lah | grep linux
-rw-rw-r--.  1 bjames bjames  23K Sep 24 23:46 linux_intro.md
```

#### My most used `grep` arguments

`-E` use extended regular expressions.

`-v` inverse matching, prints all lines that don't match the pattern

`-o` only output the matching string

`-r` recursively search sub-directories

`-n` print the line number the match occurred on

`-i` case insensitive search

`-I` ignore binary files

`grep` has tons of options and can be used for finding just about anything you'd need to find so I *highly* recommend reading `man grep` as the need arises. 

### locate

`locate` is used to find files based on their names. It can be used with either basic wildcards or regular expressions. 

```
[bjames@t470s pages]$ locate -i *mac*.pdf
/var/lib/snapd/snap/pycharm-community/147/help/ReferenceCardForMac.pdf
/var/lib/snapd/snap/pycharm-community/150/help/ReferenceCardForMac.pdf
```

This is useful if I remember all or part of the name of a file, but don't remember where it was saved. 

### which

`which` returns the path of a shell command. This is especially useful for user installed programs and aliases. 

```
[bjames@t470s pages]$ which ll
alias ll='ls -l --color=auto'
	/usr/bin/ls
```

## SSH

Linux has a built in SSH client, called OpenSSH[^4]. Basic usage is very simple.
```
[bjames@lwks1 ~]$ ssh labtoolbox
bjames@labtoolbox's password: 
bjames@labtoolbox:~$ 
```
You can also specify a username
```
[bjames@lwks1 ~]$ ssh root@labtoolbox
root@labtoolbox's password: 
root@labtoolbox:~$ 
```
__Usability Tip__ most Linux distributions ship with a program called bash-completion installed. If it's installed you can use tab-completion to fill in the hostname based on your known-hosts and ssh-config files. If there are multiple matches it will print out a list of matching hosts. This can be useful if you are having trouble remembering an IP or hostname. 

```
[bjames@lwks1 ~]$ ssh 172.16.12.1
172.16.12.127  172.16.12.130  172.16.12.132  172.16.12.137  
```
### Logging SSH Sessions

As network engineers we often need to log our ssh sessions to a file. This can be done using the `tee` program as follows.

```
[bjames@lwks1 ~]$ ssh 172.16.12.127 | tee logfile.log
```

This is a good time to introduce the concept of `|` or pipes. `ssh` and `tee` are two seperate programs. Linux CLI programs such as `ssh` often read from standard input (commonly called stdin) write to standard output (commonly called stdout). When using a terminal emulator, stdout is printed on the terminal and stdin is input to the terminal. `|` is one of the redirection operators in Linux. In this case, we are redirecting the output of `ssh` to the input of `tee` which in turn writes to logfile.log.

`ssh`, `tee` and output redirection are examples of the first two points of the Unix Philosophy at the top of this page. `ssh` and `tee` are both small programs that do one thing well.  In addition, we've made the output of `ssh` the input of `tee`. Redirection is an important part of effective CLI use.

### The Known Hosts File
The first time you log into a device you'll be prompted to add it's RSA key to the known hosts file. If this key ever changes, you'll be presented with an error message.
```
[bjames@lwks1 ~]$ ssh 192.168.88.1
The authenticity of host '192.168.88.1 (192.168.88.1)' can't be established.
RSA key fingerprint is SHA256:tXxQqN842Uoe/35JLTOOllo5liFu3qOERiid54iIW1Y.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.88.1' (RSA) to the list of known hosts.
bjames@192.168.88.1's password: 
```
If the key ever changes, you'll be presented with an error message.
```
[bjames@lwks1 ~]$ ssh 192.168.88.1
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
SHA256:HrknWcZ9j3/gt8TY7iqtsOXgJgEypFzuDD8Mydi5y1o.
Please contact your system administrator.
Add correct host key in /home/bjames/.ssh/known_hosts to get rid of this message.
Offending RSA key in /home/bjames/.ssh/known_hosts:10
RSA host key for 192.168.88.1 has changed and you have requested strict checking.
Host key verification failed.
```
This can be fixed by manually deleting the key from the known_hosts file or you can use `ssh-keygen -R <hostname>` to remove the key from the file.
```
[bjames@lwks1 ~]$ ssh-keygen -R 192.168.88.1
# Host 192.168.88.1 found: line 10
/home/bjames/.ssh/known_hosts updated.
Original contents retained as /home/bjames/.ssh/known_hosts.old
```
### SSH Configuration File

The SSH configuration file is used to control how your system connects to other systems via SSH. There are actually multiple SSH configuration files on most systems. Commonly, `/etc/ssh/ssh_config` will contain some basic system-wide configuration as well as example configuration that has been commented out. On more modern systems, your system-wide SSH configuration will include any `.conf` file in `/etc/ssh/ssh_config.d/`. In addition to the system-wide configuration files, each user can have a configuration file under `~/.ssh/config`. In general I've found it best to edit user configuration files first and system-wide configuration files only when necessary.

The SSH Configuration file has a simple syntax. 

```
# This is a line comment

Host <hostname, IP or pattern>
	# any number of options can be listed here
	Ciphers aes128-ctr
# Use ssh-keys for all other hosts
Host *
	IdentityFile ~/.ssh/id_rsa
```

__Note:__ The SSH Configuration file has it's own man page, you can read it with `man ssh_config`

### SSH Arguments

Many of the options you configure in the SSH Configuration file may also have equivalent arguments. The one I use most frequently is `ssh -c <cipher> <hostname>` when connecting to older devices that don't use modern SSH ciphers.

```
[bjames@lwks1 ~]$ ssh oldhost1
Unable to negotiate with oldhost1 port 22: no matching cipher found. Their offer: aes128-cbc,3des-cbc,aes192-cbc,aes256-cbc
[bjames@lwks1 ~]$ ssh -c aes256-cbc oldhost1
```

For more SSH arguments read `man ssh`

### SSH Keys

SSH can use public key authentication instead of password authentication. As long as your keys are managed correctly, this is both more convenient and secure than password authentication. To use key based authentication, you must first generate a private key. 

```
[bjames@lwks1 ~]$ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/bjames/.ssh/id_rsa): test_key
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Passphrases do not match.  Try again.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in test_key.
Your public key has been saved in test_key.pub.
The key fingerprint is:
SHA256:F/hmGkdfO1F+S1fm8cVtJAKHiI7sOQFpAEONwvZjZ5Y bjames@lwks1
The key's randomart image is:
+---[RSA 3072]----+
|Boo.   . ..oo .+B|
|.=+.  . .... . *O|
|o..o o. . o   oo*|
|   ++E.  o o ..o+|
|  ..=o  S * . o. |
|    +    B     . |
|     .  .        |
|                 |
|                 |
+----[SHA256]-----+
```

I strongly recommend setting a passphrase, especially in a shared environment. If you can't be bothered to type your passphrase more than once per session, you can use `ssh-agent` to store the passphrase. This command generates two files `<key_name>` and `<key_name>.pub`. Once you've generated an SSH key pair, you need to copy the public key, `<key_name>.pub` to the systems you need to authenticate against. 

__Note:__ In practice, it's likely that you'll just want to use default of `~/.ssh/id_rsa`

```
[bjames@lwks1 ~]$ ssh-copy-id -i test_key.pub goaccess.neverthenetwork.com
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "test_key.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
bjames@goaccess.neverthenetwork.com's password: 

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'goaccess.neverthenetwork.com'"
and check to make sure that only the key(s) you wanted were added.
```

This program works by copying your `<key_name>.pub` to `~/.ssh/authorized_keys`. Which can be done manually from systems that don't have `ssh-copy-id` installed. In addition, this might not work on non-unix-like systems. In which case you'll need to copy the contents of `<key_name>.pub` to the authorized key store manually. 

Once the key has been copied, you can log in to the remote system by specifying the identity file using `ssh -i` or by modifying your ssh configuration to always use a specific identity file for one or every host. 

```
[bjames@lwks1 ~]$ ssh -i test_key goaccess.neverthenetwork.com 
Enter passphrase for key 'test_key': 
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-55-generic x86_64)

bjames@goaccess:~$ 
```

__Note:__ There are several methods to maintain a list of authorized SSH keys across all your systems. One common method is to include users `authorized_keys` key files in configuration management. There are also centralized methods such as storing the keys in LDAP. 

#### SSH Agent

I'm only going to cover the absolute basic use of `ssh-agent` for more information consult `man ssh-agent`. `ssh-agent` can be used to store ssh keys and is especially useful in the case of ssh keys using passphrases. To use `ssh-agent`, it first needs to be started. 

```
[bjames@lwks1 ~]$ eval `ssh-agent`
Agent pid 21285
```

You probably noticed the use of the `eval` command. `eval` takes input from a file or stdin and evaluates it as if it was entered on the CLI. In this case, calling `ssh-agent` by itself would've resulted in the following output to stdout. 

```
[bjames@lwks1 ~]$ ssh-agent
SSH_AUTH_SOCK=/tmp/ssh-k4tysoOInoQM/agent.21285; export SSH_AUTH_SOCK;
SSH_AGENT_PID=21285; export SSH_AGENT_PID;
echo Agent pid 21285;
```

These are bash commands that create new [environment variables](#environment-variables) called `SSH_AUTH_SOCK` and `SSH_AGENT_PID` and then prints them to the screen. `eval` causes these bash commands to be run in the current shell.

Once our `ssh-agent` is running, we can use `ssh-add` to add keys to the `ssh-agent`. By default it tries to add `~./ssh/id_rsa`, but you can specify a key using `ssh-add <key_name>`. Once that's been done you can use the identity file without being prompted for the passphrase.

```
[bjames@lwks1 ~]$ ssh-add test_key
Enter passphrase for test_key: 
Identity added: test_key (bjames@lwks1)
[bjames@lwks1 ~]$ ssh -i test_key goaccess.neverthenetwork.com 
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-55-generic x86_64)

bjames@goaccess:~$ 
```

__Note:__ This also works with identity files that have been specified using the ssh configuration file

## Vim

`vim` is commonly the default CLI text editor on linux distributions. Once you've got the basics down, `vim` is a joy to use. `vim` has a few different modes, but here I'm just going to cover __normal__ and __insert__. 

This is just a cheatsheet of sorts, for more information I recommend `man vim` or `vimtutor`, which launches a fantastic interactive guide to `vim`.

### Normal Mode Commands
`j` move the cursor down

`k` move the cursor up

`l` move the cursor right

`h` move the cursor left

`.` repeat the last insert

`i` switch to insert mode at the current cursor location

`I` switch to insert mode at the beginning of the current line

`a` switch to insert mode in the position following the cursor

`A` switch to insert mode at the end of the line

`:w` save the file

`:wq` or `:x`save the file and quit

`:q` quit

`:q!` quit ignoring prompts about the file not being saved

### Insert Mode
`ESC` switch to Normal Mode

## .bashrc

.bashrc is described by `man bash` as your personal initialization file. Mine typically contains a group of environment variables, command aliases and functions. .bashrc is actually a list of commands that are ran when you first start a terminal session. For instance, if you want to alias

```
[bjames4@plaalanwan1 ~]$ more .bashrc
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# Source sec account tools
if [ -f ~/.secacctbash ]; then
    . ~/.secacctbash
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# delete ssh logs more than 1 week old
find ~/sshlogs/ -mindepth 1 -mtime +7 -delete

# User specific aliases and functions

alias isotime="date +"%Y-%m-%dT%H%M%S""
alias ll="ls -lah"
alias setproxy="source ~/scripts/set_proxy.sh"

# oui lookup using nmap ouilist and grep
function ouilookup()
{
    grep -i "$1" ~/oui.txt;
}

# log ssh sessions
function logssh()
{

    currtime=$(isotime);
    ssh $1 2>&1 | tee -a ~/sshlogs/$1-$currtime.log;

}

# unset the proxy environment variables
function unset_proxy() {
    unset HTTP_PROXY
    unset HTTPS_PROXY
}
```

SSH Agent

## Queue

Things I plan on adding as time allows

* Network Utilities
	- tcpdump
	- dig
	- netcat
	- whois
	- traceroute and tracepath
	- ping
* IO Redirection
* File Transfer
	- Clients: SCP, SFTP, FTP
	- Servers: Python Simple HTTP Server
* Text Manipulation: awk, sed and cat


[^1]: My apologies to Richard Stallman, [GNU+Linux](https://www.gnu.org/gnu/linux-and-gnu.en.html) just doesn't roll of the tongue quite as well.
[^2]: https://archive.org/details/bstj57-6-1899/page/n3
[^3]: As the Free Software Foundation suggests, many, but not all of these are part of the GNU Core Utilities. 
[^4]: OpenSSH is a widely used product of the OpenBSD Project, another Unix-like operating system. 
[^5]: This is due to a feature called alternate screen. I generally don't mind altscreen, but there are ways to [effectively disable it](https://www.shallowsky.com/linux/noaltscreen.html). 