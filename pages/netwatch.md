title: Practical Automation - Netwatch
published: 2019-09-12
category:
- Automation
- Programming
author: Brandon James
summary: One of the more practical ways to get started with automation is by writing small data gathering utilities. In this article I walk through my scripting process using a practical example. 


One practical way to get started with automation is by writing small data gathering utilities. They provide immediate value and have no risk of failure. In this article we are going to explore automating an issue I've faced in the past. You're working a TAC case and they want you to run a command on _n_ devices once every _x_ minutes over the course of _y_ hours. 

This project was inspired by a [post on Reddit](https://www.reddit.com/r/Cisco/comments/d2ndqq/dump_switch_commands_to_a_file_on_a_schedule/) and I hope it will be useful to Network Engineers everywhere.

## Problem Meet Solution

It's important to have a clear definition of the problem you are solving. This problem is relatively simple. We need to periodically run a set of commands against multiple network devices. 
