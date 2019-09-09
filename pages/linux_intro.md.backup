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

A few general notes on the Linux directory layout.

i) The root of the Linux filesystem is `/` or the root directory (not to be confused with the root user). This is not quite the same as being in the root of the C:\\ drive on a Windows machine. In Linux, all drives are mounted under the root filesystem. 

ii) All users have a home directory, it traditionally resides under `/home/<username>`. The `~` symbol refers to the home directory.

iii) When within a folder, you can refer to the folder as `.`. As an example, if you have a file called notes.txt within your home directory, when you are on the CLI and you are in your home directory, you can refer to the file as `./notes.txt`.

iv) All folders except the root directory have a subfolder called `..`. It refers to the parent directory. As an example `~/..` refers to `/home` and `~/../..` refers to `/`. This can be useful for navigation.

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

* `cd` Changes the working directory. `cd` by itself takes you back to your home directory.  


[^1]: My apologies to Richard Stallman, [GNU+Linux](https://www.gnu.org/gnu/linux-and-gnu.en.html) just doesn't roll of the tongue quite as well.
[^2]: https://archive.org/details/bstj57-6-1899/page/n3
[^3]: As the Free Software Foundation suggests, many, but not all of these are part of the GNU Core Utilities. 