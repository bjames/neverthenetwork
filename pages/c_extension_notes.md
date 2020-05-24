title: Extending C with Python - Preliminaries
published: 
category:
- Programming
author: Brandon James
summary: 


I've been meaning to revist C for a while now. I think having a compiled language in my toolbox is important. As someone who mostly programs in Python, C makes a lot of sense because you can write Python modules using C. This is something you might need to do if you are doing anything computationally intensive and only if it's absolutely necessary. Python is generally fast enough and premature optimization often leads to bugs and difficult to maintain code.  

I haven't touched C since college, but I remember enough of it that most of the online tutorials are overly basic. So I decided an appropriate way to relearn C would be to write a Python Module in C. I started working through the [Python Doc on Extending Python with C](https://docs.python.org/3/extending/extending.html) and I found that it assumes either a whole lot of background on C and the Python/C API or it assumes the reader is willing to spend a significant time doing research as they read through the doc. In this article, I share my notes from working through the example module assuming the reader has little or no background in C. There will be a follow up article where I write a Python module in C that is more applicable to network engineers. In that article I will also compare the running time of the C module and an equivelent native Python module. 

# `spam module`
In the Extending Python doc, we create a simple module that binds to the C system function, which is provided by [`stdlib.h`](https://en.wikibooks.org/wiki/C_Programming/Standard_libraries#ANSI_Standard) C library. C libraries are roughly equivelent to Python modules, but they behave quite differently. Let's consider the following simple example:

```
#include <stdio.h>

void main(){

    printf("Hello, World!\n");

}
```

Unlike Python, C doesn't provide a print function by default. So in order to write to the terminal we need to import `stdio.h`. Just like the name implies, `stdio` is the portion of the standard library that provides IO functions. If you have access to a linux machine, it's very likely you have `stdio.h` sitting in a folder somewhere. You can find it with `locate stdio.h` and peek at the code if you are curious[^1]. 

In C, any statement begining with `#` is a preprocessor directive[^2]. `#include` tells the preprocessor to inject the code mentioned in the `#include` statement into the file. It should be noted that you won't actually see a printf function instead the header file, instead you'll find a function prototype:

```
extern int printf (const char *__restrict __format, ...);
```

These prototypes exist only to help the compiler verify your use of the function. In the case of C standard library functions, your compiler already has precompiled copies of the code. After your code has been compiled, it is linked to the precompiled library[^3]. _______________WHERE IS THE OBJ FILE??__________

[^1]: Alternatively, you can view it on the [web](https://sourceware.org/git/?p=glibc.git;a=blob;f=include/stdio.h;h=9df98b283353e3d5610b8036876833e86a8eeab0;hb=HEAD).
[^2]: You can read more about preprocessor directives [here](https://en.wikibooks.org/wiki/C_Programming/Preprocessor_directives_and_macros). 
[^3]: The printf function is found in printf.c in the stdlib, you can view it [here](https://sourceware.org/git/?p=glibc.git;a=blob;f=stdio-common/printf.c;h=15f71c1feddf9e8324ab38afb351c7840af5a8fc;hb=9ea3686266dca3f004ba874745a4087a89682617)