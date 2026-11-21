# Chapter 2: Text Manipulation in Linux
Text manipulation is a crucial skill in Linux, as most of the system's configuration files and logs are plain text. This chapter introduces various commands and techniques to efficiently view, edit, and manage text files.

## Viewing Files
`cat` (Concatenate)
Usage: Displays the entire content of a file.
Example: `cat /etc/passwd`
Output: Displays the full content of the /etc/passwd file.

`head`
Usage: Shows the first 10 lines of a file by default.
Example: head /etc/passwd
Output: Displays the first 10 lines of the /etc/passwd file.
Customization: To show the first 20 lines: head -n 20 /etc/passwd

`tail`
Usage: Shows the last 10 lines of a file by default.
Example: tail /var/log/syslog
Output: Displays the last 10 lines of the /var/log/syslog file.
Customization: To show the last 20 lines: tail -n 20 /var/log/syslog

`nl` (Number Lines)
Usage: Displays the content of a file with line numbers.
Example: nl /etc/passwd
Output: Displays the content of the /etc/passwd file with line numbers.

## Filtering Text
`grep`
Usage: Searches for specific text within a file.
Example: `grep 'root' /etc/passwd`
Output: Displays all lines containing the word root in the /etc/passwd file.

`sed` (Stream Editor)
Usage: Finds and replaces text within a file.
Example: `sed 's/oldtext/newtext/g' filename`
Output: Replaces all occurrences of oldtext with newtext in the file filename.

`awk`
Usage: A powerful text-processing language for pattern scanning and processing.
Example: `awk '{print $1}' /etc/passwd`
Output: Prints the first column of each line in the /etc/passwd file.

## Combining Commands
`pipe` (|)
Usage: Sends the output of one command as input to another command.
Example: `cat /etc/passwd | grep 'root'`
Output: Filters the content of /etc/passwd to show only lines containing root.

`tee`
Usage: Reads from standard input and writes to standard output and files.
Example: `cat /etc/passwd | tee outputfile`
Output: Displays the content of /etc/passwd and saves it to outputfile.

## Editing Files
`nano`
Usage: A simple text editor.
Example: `nano filename`
Output: Opens the file filename in the nano text editor.

`vim`
Usage: A more advanced text editor.
Example: `vim filename`
Output: Opens the file filename in the vim text editor.

## Case Scenarios with Examples

### Viewing Log Files
Scenario: You need to check the last 50 lines of the system log to troubleshoot an issue.
Command: `tail -n 50 /var/log/syslog`
Explanation: This command displays the last 50 lines of the /var/log/syslog file, helping you quickly review recent system events.

### Searching for Errors
Scenario: You suspect there are errors in the Apache web server logs.
Command: `grep 'error' /var/log/apache2/error.log`
Explanation: This command searches for the keyword error in the Apache error log, allowing you to identify and address issues.

### Replacing Text in Configuration Files
Scenario: You need to update the hostname in a configuration file.
Command: `sed 's/oldhostname/newhostname/g' /etc/hostname`
Explanation: This command replaces all instances of oldhostname with newhostname in the /etc/hostname file.

### Extracting Usernames
Scenario: You want to list all usernames from the /etc/passwd file.
Command: `awk -F: '{print $1}' /etc/passwd`
Explanation: This command uses awk to extract and print the first field (username) from each line of the /etc/passwd file.

### Combining Commands for Detailed Search
Scenario: You need to find lines containing the word fail in a log file and display them with line numbers.
Command: `grep 'fail' /var/log/syslog | nl`
Explanation: This command first searches for lines containing fail and then numbers each line of the output.

By mastering these commands and techniques, you'll be able to efficiently view, edit, and manage text files in Linux, which is essential for system administration, programming, and security tasks.
