## Chapter 1: Getting Started with the Basics
**Linux** is the operating system of choice for hackers due to its powerful command line interface and extensive customization capabilities. In this chapter, we'll explore the essentials to get you started with Linux using Kali, a popular distribution for penetration testing and security research.

## Introductory Terms and Concepts
Before diving into Linux, it's important to understand a few key terms:

**Binaries**: Executable files, similar to applications in Windows, found in directories like /usr/bin or /usr/sbin.
**Case Sensitivity**: Linux distinguishes between file.txt and File.txt. This can be a common pitfall for new users.
**Directory**: Equivalent to a folder in Windows, used to organize files hierarchically.
**Home Directory**: Each user has a personal directory (/home/username) where files are stored by default.
**Root**: The superuser with full control over the system. Many hacking tools require root access to function properly.
**Shell**: The command line interface for interacting with the operating system. The most common shell is bash.
**Terminal**: The application that provides access to the shell.

## A Tour of Linux OS

### Basic Commands in Linux
Let's start with some basic commands to navigate and manipulate the filesystem:

`pwd` (Print Working Directory)
Usage: Displays the current directory.
Example: pwd
Output: /home/user

`cd` (Change Directory)
Usage: Changes the current directory.
Example: cd /etc
Output: Changes the directory to /etc.

`ls` (List Directory Contents)
Usage: Lists files and directories within the current directory.
Example: ls
Output: Lists files and directories.

`whoami` (Display current user)
Usage: Displays the current user's name.
Example: whoami
Output: root

### Modifying Files and Directories
Working with files and directories is a common task in Linux:

#### Creating a File
Usage: `touch filename`
Example: touch testfile.txt
Output: Creates an empty file named testfile.txt.

#### Creating a Directory
Usage: `mkdir directoryname`
Example: mkdir testdir
Output: Creates a directory named testdir.

#### Copying a File
Usage: `cp source destination`
Example: cp testfile.txt testfile_backup.txt
Output: Copies testfile.txt to testfile_backup.txt.

#### Renaming a File
Usage: `mv oldname newname`
Example: mv testfile.txt newfile.txt
Output: Renames testfile.txt to newfile.txt.

#### Removing a File
Usage: `rm filename`
Example: rm newfile.txt
Output: Deletes newfile.txt.

#### Removing a Directory
Usage: `rmdir directoryname`
Example: rmdir testdir
Output: Deletes the testdir directory (only if it's empty).

### Finding Stuff
Linux provides powerful tools for searching files and directories:

`locate`
Usage: Quickly finds files by name.
Example: locate testfile.txt
Output: Lists all files named testfile.txt in the system.

`find`
Usage: Searches for files in a directory hierarchy.
Example: find /home -name "testfile.txt"
Output: Searches for testfile.txt starting from /home.

`grep`
Usage: Searches for specific text within files.
Example: grep "text" filename
Output: Displays lines in filename that contain "text".

`whereis`
Usage: Locates the binary, source, and manual page files for a command.
Example: whereis ls
Output: ls: /bin/ls /usr/share/man/man1/ls.1.gz

`which`
Usage: Shows the full path of shell commands.
Example: which ls
Output: /bin/ls

## Linux Directory Structure
This tree structure shows the top-level directories and a few examples of files and subdirectories in each.

/
├── bin
├── boot
├── dev
├── etc
├── home
│   └── username
├── lib
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── sbin
├── srv
├── sys
├── tmp
├── usr
│   ├── bin
│   ├── lib
│   ├── local
│   └── share
└── var
    ├── log
    └── spool

## Test your knowledge of Linux
Now that you have the basics, try these commands out on your Ubuntu or Kali system. Experiment with creating, modifying, and deleting files and directories. Use the search commands to locate files and understand their usage. The best way to learn Linux is by doing, so don't be afraid to explore and make mistakes.
