# Bash Scripting

## Mastering Bash Scripting: A Gateway to Linux Automation

Bash scripting is a powerful tool that allows Linux users to automate tasks, streamline workflows, and enhance productivity. Whether you're a beginner dipping your toes into the world of Linux or a seasoned professional, mastering bash scripting is an essential skill. In this post, we'll delve into the fundamentals of bash scripting, exploring how to create scripts, utilize variables, and interact with the user. We'll also provide code snippets and examples to help you start writing your own scripts.

### Why Bash Scripting?

Bash scripting is not just for hackers or system administrators; it's for anyone looking to automate repetitive tasks, simplify complex processes, or create customized solutions on Linux. Scripts can range from simple commands to complex programs that perform a variety of tasks, such as file management, network monitoring, or even penetration testing. By learning bash scripting, you gain the ability to control your Linux environment more efficiently and effectively.

### Your First Bash Script

Let's start with a simple bash script. We'll create a script that prints "Hello, Hackers-Arise!" to the terminal.

```bash
#!/bin/bash
# This is a simple script to print a message
echo "Hello, Hackers-Arise!"
```

In this script:

- **`#!/bin/bash`** - is known as the shebang. It tells the system that this script should be run using the bash shell.

- **`echo`** - is a command that prints text to the terminal.

To run this script, save it to a file called `hellohackers.sh`, and make it executable:

```bash
chmod +x hellohackers.sh
./hellohackers.sh
```

This will output:

```bash
Hello, Hackers-Arise!
```

### Adding Variables and User Input

Variables in bash scripting allow you to store and manipulate data. Let's enhance our script by adding variables and user input.

```bash
#!/bin/bash
# Script to greet a user
echo "Enter your name:"
read name
echo "Hello, $name! Welcome to Hackers-Arise!"
```

Here:

- **`read name`** - prompts the user to enter their name and stores it in the variable `name`.

- **`$name`** is used to access the value stored in the `name` variable.

Running this script will interact with the user:

```bash
Enter your name:
John
Hello, John! Welcome to Hackers-Arise!
```

### Creating a Simple Port Scanner

Now that we understand variables and user input, let's create a simple port scanner script. This script will check if a specific port on a given host is open.

```bash
#!/bin/bash
# Simple Port Scanner

echo "Enter the host:"
read host
echo "Enter the port:"
read port

echo "Scanning $host on port $port..."
timeout 1 bash -c "</dev/tcp/$host/$port" && echo "Port $port is open on $host" || echo "Port $port is closed on $host"
```

Explanation:

- **`timeout 1`** limits the scan time to 1 second.
- **`</dev/tcp/$host/$port`** attempts to connect to the specified port on the host.
- The script prints whether the port is open or closed.

### Improving the Script: Looping Through Multiple Ports

What if you want to scan multiple ports? We can modify the script to scan a range of ports using a loop.

```bash
#!/bin/bash
# Port Scanner for Multiple Ports

echo "Enter the host:"
read host
echo "Enter the starting port:"
read start_port
echo "Enter the ending port:"
read end_port

for (( port=$start_port; port<=$end_port; port++ ))
do
    echo "Scanning $host on port $port..."
    timeout 1 bash -c "</dev/tcp/$host/$port" && echo "Port $port is open" || echo "Port $port is closed"
done
```

This script scans all ports between the specified `start_port` and `end_port`. The loop iterates over each port, scanning it and printing the result.

### Common Bash Commands for Scripting

As you begin to write more complex scripts, you'll frequently use certain bash commands. Here are a few you should know:

- `if` statements: Used for conditional execution.
- `for` and `while` loops: For iterating over a series of items.
- `case`: A multi-branch decision-making tool, similar to `switch` in other programming languages.
- `functions`: Group commands into reusable blocks of code.

### Example: Automating Backups

Let's combine some of these elements into a more practical script. Here's an example of a backup script that compresses and archives a directory.

```bash
#!/bin/bash
# Simple Backup Script

backup_dir="/home/user/backup"
source_dir="/home/user/data"
timestamp=$(date +"%Y%m%d%H%M")

echo "Creating backup..."
tar -czf "$backup_dir/backup_$timestamp.tar.gz" -C "$source_dir" .

echo "Backup created at $backup_dir/backup_$timestamp.tar.gz"
```

This script:

- Sets the `backup_dir` and `source_dir` variables.
- Uses `date` to create a timestamp.
- Compresses the contents of `source_dir` into a `.tar.gz` file named with the current timestamp.
- Saves the backup file in `backup_dir`.

### Conclusion

Bash scripting is a skill that can significantly improve your productivity and capability on Linux. By mastering the basics and gradually tackling more complex scripts, you can automate tasks, manage systems more efficiently, and even create your own tools. Whether you're just starting out or are an experienced Linux user, bash scripting opens up a world of possibilities.

Dive in, experiment with scripts, and soon you'll find that bash scripting becomes an indispensable part of your Linux toolkit. Happy scripting!

Scenario: You want to automate a task to scan for open ports on your network.

Commands:

Create a Bash Script
Explanation: This command sequence creates a basic bash script.

Example:

```bash
nano scan_ports.sh

#!/bin/bash
echo "Scanning for open ports..."
nmap -sT localhost
chmod +x scan_ports.sh
./scan_ports.sh
Output: Creates and runs a script that scans for open ports on the local machine.
