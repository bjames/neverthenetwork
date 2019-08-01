title: How I Automate - Concurrency
published: 2019-08-02
category:
- Automation
author: Brandon James
summary: If you need to push configuration changes to more than one device at a time, you need concurrency.

Interacting with Network Devices can often be I/O limited. A function runs, waits for a response from the device, then another function runs so on and so forth. This is made worse by the fact that scripts are often run against multiple devices, after all the purpose of scripting is to speed up repetitive tasks. 

As an example, one of the scripts I maintain is used to test the POTS lines my enterprise uses for out-of-band connectivity at our branches and call centers. Dial-up modems are slow, you make a call, the line rings, remote end picks up, the modems eventually train up and then you finally get a connection. With some of our international locations I've seen this process take nearly a full minute. Before I added multiprocessing, this script could take over 2 hours to complete. Now it finishes in roughly 20 minutes.

As a little bit of background on my process; I typically write scripts without concurrency first using my little 3560-CX as a test device. Once the script is complete, I write a bit of logic to execute the script against multiple devices simultaneously. That logic is discussed below.

### Using the Multiprocessing Library

Python provides two easy ways to add concurrency to your scripts. The first is [threading](https://docs.python.org/3/library/threading.html) and the second is [multiprocessing](https://docs.python.org/3/library/multiprocessing.html). I use the latter

 

