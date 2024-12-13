Duplicate File Detection and Notification System
This Python project detects duplicate files in a specified folder and notifies the user using a graphical interface. It calculates file hashes and tracks duplicates based on the hash and file size. It also monitors the folder in real-time using the watchdog library.

Features:
File Hashing: Uses MD5 to hash files and compare them to detect duplicates.
Real-time Monitoring: Monitors a folder for newly downloaded or created files and detects duplicates.
Tkinter Notifications: When a duplicate file is detected, a notification window is shown with details such as file name, location, size, and count of duplicates.
Supports Browser Downloads: Excludes incomplete browser files (such as .crdownload and .part).
Multithreading: Utilizes ThreadPoolExecutor to scan existing files and detect duplicates without blocking the application.
Technologies Used:
Python 3.x
hashlib (for generating file hashes)
tkinter (for the GUI-based notifications)
watchdog (for monitoring file system events)
concurrent.futures (for multithreading support)
Requirements:
Python 3.x
watchdog
tkinter (usually comes pre-installed with Python)
Install Dependencies:
Ensure you have Python 3.x installed on your machine.
Install the necessary dependencies by running:
bash
Copy code
pip install watchdog
How It Works:
Scan Existing Files: When you select a folder, the program scans all existing files in that folder and computes their hashes.

Monitor Folder for New Files: The program continuously monitors the selected folder for any new files. If a new file is detected:

It calculates the hash of the file.
It checks if the hash matches any previously scanned files.
Duplicate Detection: If a duplicate file (same hash) is detected:

A Tkinter notification window pops up displaying the file name, location, size, and the total size of all duplicates.
The program tracks the number of duplicates and the total size of all files with the same hash.
Notifications:

The program shows a popup message with details about the duplicate.
The popup contains a Close button to dismiss the notification.
Excluding Temporary Files: The program automatically ignores browser download files (such as .crdownload or .part files), as these are incomplete files that might not be relevant for duplication checks.

Usage:
Run the Program:

Start the program by executing the script:
bash
Copy code
python duplicate_file_detector.py
Select Folder:

A file dialog will open, allowing you to select a folder to monitor for duplicate files.
View Notifications:

If a duplicate file is detected, a Tkinter window will appear, showing the details of the duplicate file.
Stop Monitoring:

To stop monitoring, simply close the program.
Example Output:
When a duplicate file is detected, you’ll see a pop-up message like this:

yaml
Copy code
Duplicate File Detected:

Name: example_video.mp4
Location: C:/Downloads
Individual Size: 12345678 Bytes
Total Size of Duplicates: 45.23 MB
Count: 3
Notes:
The program uses the MD5 hash of files to detect duplicates. This method is fast, but it’s not the most collision-resistant. For more sensitive applications, consider using a stronger hash like SHA-256.
The program does not track files that are still being downloaded (files ending in .part or .crdownload).
The program uses multithreading to scan existing files efficiently, preventing the UI from freezing while it works.

![image](https://github.com/user-attachments/assets/7bbbc509-9d9f-4212-aed7-82af49c2f9ec)
