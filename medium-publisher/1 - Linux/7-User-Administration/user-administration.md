# User Administration

![image](./img/linux-101.png)

**What the Tutorial is About:**

This lesson teaches you how to manage users on an Ubuntu 20.04 Linux system.  It covers the basic commands to add new users, delete existing users, and modify user privileges.  Think of it as learning how to control who has access to your computer and what they're allowed to do.

**Why it's important:**

*   **Security:**  Each user having their own account keeps their files private and prevents accidental damage to the system.
*   **Organization:** Different people can use the same computer without messing up each other's work.
*   **Permissions:**  You can control what each user is allowed to do on the system.

**Key Concepts (Simplified):**

*   **Users:**  Each person (or process) that needs to interact with the computer needs a user account. This allows the system to track who is doing what and assign permissions appropriately.

*   **Root User:**  This is the super-powerful administrator account.  It can do *anything* on the system. You should generally *avoid* using the root user directly for everyday tasks, as mistakes can have serious consequences.  This tutorial doesn't focus on the root user directly, but understands that you'll often use `sudo` to act like the root user.

*   **`sudo`:**  This is a command that allows you to temporarily run commands as the root user.  It's like saying, "I need to do something that requires administrator privileges." You'll need `sudo` for most of the commands in this tutorial.

*   **Groups:** Users can be organized into groups.  This makes it easier to manage permissions for multiple users at once.  For example, you might have a "developers" group.

**The Main Commands Explained (For Beginners):**

1.  **`adduser username` (Adding a User):**
    *   **What it does:**  Creates a new user account with the specified `username`.
    *   **How it works:**  The `adduser` command is a helpful script that does a few things:
        *   Asks you for information about the user (full name, etc.).  You can usually just press Enter to skip these.
        *   Creates a home directory for the user (e.g., `/home/username`). This is where the user's files and settings will be stored.
        *   Creates a password for the user. *You need to set a strong password!*
    *   **Example:** `sudo adduser newuser`  (Adds a user named "newuser").

2.  **`userdel username` (Deleting a User):**
    *   **What it does:**  Deletes the user account with the specified `username`.
    *   **Important:**  This *does not* delete the user's files in their home directory by default.
    *   **Example:** `sudo userdel olduser` (Deletes the user "olduser").

3.  **`userdel -r username` (Deleting a User and Their Home Directory):**
    *   **What it does:**  Deletes the user account *and* removes their home directory and all its contents.  *Be careful with this command!*  It's permanent.
    *   **Example:** `sudo userdel -r olduser`

4.  **`usermod -aG groupname username` (Adding a User to a Group):**
    *   **What it does:** Adds an existing user to a specific group.
    *   **`-aG`:**  `-a` means append (add to the group) and `-G` specifies the group.
    *   **Example:** `sudo usermod -aG sudo newuser` (Adds the user "newuser" to the "sudo" group. The "sudo" group allows users to run commands with administrator privileges using `sudo`.)

5.  **`gpasswd -d username groupname` (Removing a User from a Group):**
    *   **What it does:** Removes a user from a group.
    *   **Example:** `sudo gpasswd -d newuser sudo` (Removes the user "newuser" from the "sudo" group).

6.  **Creating a New User:**
    *   The command `sudo adduser newusername` is used to create a new user account.  Replace `newusername` with the actual name you want for the user.
    *   The system will then prompt you for a password for the new user, and some optional information like their full name. *Make sure the password is strong and you remember it!*

7.  **Adding a User to the `sudo` Group (Giving Administrative Privileges):**
    *   By default, new users can't use `sudo`. To grant a user administrative privileges, you need to add them to the `sudo` group.
    *   The command `sudo usermod -aG sudo newusername` does this. Again, replace `newusername` with the actual username.

**Key Takeaways for Beginners:**

*   Managing users is essential for security and organization on a Linux system.
*   Use the `adduser` command to create new accounts.
*   Be very careful when deleting users, especially when using the `-r` option.
*   The `sudo` command is your friend for running commands that require administrative privileges.
*   Groups make it easier to manage permissions for multiple users.
*   Always use strong passwords!

**What to do next:**

1.  **Practice:**  Try the commands in a safe environment, like a virtual machine. Don't experiment on a system that you rely on.
2.  **Read the documentation:**  Use the `man adduser`, `man userdel`, `man usermod`, and `man gpasswd` commands to learn more about each command and its options.  The `man` command brings up the manual page for a command.
3.  **Experiment:** Once you understand the basics, try adding, deleting, and modifying users and groups to see how it all works.
4.  **Be Careful:** Always double-check your commands before you run them, especially when using `sudo` or the `-r` option with `userdel`.  A mistake can break your system.

**Important Tips from the Tutorial:**

*   **Root Account:**  The root account is the most powerful account on the system.  It's often disabled for security reasons. You'll use `sudo` instead.
*   **Think before you type:** When using commands that make system changes, double-check what you are typing to avoid mistakes.
*   **Practice in a safe environment:** If you're unsure, try these commands on a test system or virtual machine before using them on your primary computer.
*   **Read the output:** The commands you run will often give you feedback. Pay attention to this output, as it can help you understand what's happening and identify errors.
*   **Consult the manual:** If you need more information about a command, you can use the `man` command. For example, `man adduser` will display the manual page for the `adduser` command.

This tutorial is a great starting point for learning about user management in Linux.