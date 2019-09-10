title: A Brief Introduction to the Linux CLI for Network Engineers
category:
- Route/Switch
author: Brandon James
summary: 


I am a huge fan of Linux[^1]. In the office, most of my real work happens on my Red Hat jumpbox. At home, all my personal machines run Fedora. One of my favorite things about working with Cisco devices is the great CLI, Linux provides a similar experience for general purpose computing. 

# Linux CLI Basics

## The Unix Philosophy

Linux falls under the "Unix-like" class of operating systems, all of these operating systems roughly follow something known as the Unix Philosophy. The Unix Philosophy has a long and somewhat storied history that you can read about in the first Chapter of [*The Art of Unix Programming* by Eric Steven Raymond](http://www.catb.org/~esr/writings/taoup/html/ch01s06.html). While the book is geared towards programmers, understanding the Unix philosophy is sure to make you a better user of Linux as well. The Unix Philosophy isn't meant to be a set of strict rules and instead should be thought of as a list of best practices.

I think of the following quote[^2] from Doug McIlroy when I think of the Unix Philosophy:

i) Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new features.

ii) Expect the output of every program to become the input to another, as yet unknown, program. Don't clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don't insist on interactive input.

iii) Design and build software, even operating systems, to be tried early, ideally within weeks. Don't hesitate to throw away the clumsy parts and rebuild them.

iv) Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them.

From the perspective of a Linux user, I think it's important to keep the first two in mind. 

## Man pages

All the commands that you run on the Linux CLI are separate programs[^3], most of these commands have listings in the system manual. To view a man page, simply type `man <utility>` where utility is the name of the command or tool you want to know more about. The `man` program itself even has a man page, type `man man` to try it out.

In addition to being a quick way to view manual entries, the `man` program belongs to a class of CLI programs called pagers. Pagers give you a way to view the entire contents of a file without the need for a scrollbar. Try `man less` or `man more` to learn about two other pagers. I'll cover both of these in more detail later.

As you read this article, I encourage you to skim the man pages for the utilities I mention. 

## File Navigation

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

* `ls` Lists the contents of the current directory. It can be combined with arguments like `ls -l` to format the output as a list, `ls -a` to print include hidden files in the output or `ls -h` to print the file size in a human readable format. Arguments can also be stacked, for example `ls -lah` formats the output as a list, includes hidden files and uses human readable file sizes. Many Linux flavors alias `ls -lah` to `ll`, which means running the command `ll` actually runs `ls -lah`. 
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

* `cd` Changes the working directory. `cd ~` or just `cd` by itself takes you to your home directory. You can `cd` using absolute paths `cd /var/log/`. You can also `cd` using relative paths `cd scripts` takes you to scripts or `cd ../notes`. 

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

iii) If we want to go to my Videos folder, we can do so in three different ways.  3) Just using a relative path. All three are show in order below:

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

## OpenSSH

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

### SSH Keys


[^1]: My apologies to Richard Stallman, [GNU+Linux](https://www.gnu.org/gnu/linux-and-gnu.en.html) just doesn't roll of the tongue quite as well.
[^2]: https://archive.org/details/bstj57-6-1899/page/n3
[^3]: As the Free Software Foundation suggests, many, but not all of these are part of the GNU Core Utilities. 
[^4]: OpenSSH is a very widely used product of the OpenBSD Project, another maker of a FOSS Unix-like operating system. 
 