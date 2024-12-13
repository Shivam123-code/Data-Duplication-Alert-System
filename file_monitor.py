
import os
import time
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
from concurrent.futures import ThreadPoolExecutor

# Function to generate hash of a file
def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):  # Read in chunks
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

# Function to convert bytes to MB
def bytes_to_mb(bytes_size):
    return bytes_size / (1024 * 1024)  # Convert bytes to MB

# Function to show duplicate file notification
def show_duplicate_notification(file_path, file_size, count, total_size):
    file_name = os.path.basename(file_path)
    file_location = os.path.dirname(file_path)
    message = (f"Duplicate File Detected:\n\n"
               f"Name: {file_name}\n"
               f"Location: {file_location}\n"
               f"Individual Size: {file_size} Bytes\n"
               f"Total Size of Duplicates: {bytes_to_mb(total_size):.2f} MB\n"
               f"Count: {count}")

    # Create a Tkinter window for the notification
    notification_window = tk.Tk()
    notification_window.title("Duplicate File Detected")
    notification_window.geometry("350x220")
    notification_window.configure(bg="#f0f0f0")
    notification_window.eval('tk::PlaceWindow %s center' % notification_window.winfo_toplevel())

    # Add a frame for better layout
    frame = tk.Frame(notification_window, bg="#f0f0f0")
    frame.pack(pady=10)

    # Display the message with better styling
    message_label = tk.Label(frame, text=message, justify=tk.LEFT, bg="#f0f0f0", font=("Arial", 10))
    message_label.pack(pady=10)

    # Close button with styling
    close_button = tk.Button(frame, text="Close", command=notification_window.destroy, 
                             bg="#4CAF50", fg="white", font=("Arial", 10), relief=tk.RAISED)
    close_button.pack(pady=10)

    # Make the window stay on top
    notification_window.attributes("-topmost", True)

    notification_window.mainloop()

# Class to handle file system events
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_hashes, file_counts, file_sizes):
        self.file_hashes = file_hashes
        self.file_counts = file_counts
        self.file_sizes = file_sizes

    def on_created(self, event):
        if not event.is_directory and not event.src_path.endswith(('.part', '.tmp')):
            time.sleep(1)  # Small delay to ensure file is fully written
            file_hash = get_file_hash(event.src_path)
            file_size = os.path.getsize(event.src_path) if os.path.exists(event.src_path) else 0
            
            if file_hash:
                # Increment the count and total size for the existing file hash
                self.file_counts[file_hash] = self.file_counts.get(file_hash, 0) + 1
                count = self.file_counts[file_hash]
                self.file_sizes[file_hash] = self.file_sizes.get(file_hash, 0) + file_size
                total_size = self.file_sizes[file_hash]

                if count > 1:
                    show_duplicate_notification(event.src_path, file_size, count, total_size)

# Function to process a single file (used for multithreading)
def process_file(file_path, file_hashes, file_counts, file_sizes):
    file_hash = get_file_hash(file_path)
    if file_hash:
        file_hashes.add(file_hash)
        file_counts[file_hash] = file_counts.get(file_hash, 0) + 1  # Initialize count for existing files
        file_sizes[file_hash] = file_sizes.get(file_hash, 0) + os.path.getsize(file_path)  # Initialize size for existing files

# Function to scan existing files and add their hashes using multithreading
def scan_existing_files(path, file_hashes, file_counts, file_sizes):
    print(f"Scanning existing files in {path}...")
    
    with ThreadPoolExecutor() as executor:
        for root_dir, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                executor.submit(process_file, file_path, file_hashes, file_counts, file_sizes)

# Function to monitor folder
def monitor_folder(folder_path, file_hashes, file_counts, file_sizes):
    event_handler = FileEventHandler(file_hashes, file_counts, file_sizes)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
    print(f"Monitoring folder: {folder_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Function to select folder
def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory()  # Open folder selection dialog
    if folder_path:
        print(f"Selected folder: {folder_path}")
        file_hashes = set()
        file_counts = {}  # Dictionary to keep track of file counts
        file_sizes = {}  # Dictionary to keep track of file sizes
        scan_existing_files(folder_path, file_hashes, file_counts, file_sizes)  # Scan existing files
        print("Initial scan completed. Monitoring for new duplicates...")
        monitor_folder(folder_path, file_hashes, file_counts, file_sizes)  # Start monitoring for new files

# Main function
if __name__ == "__main__":
    select_folder()  # Allow user to select a folder


