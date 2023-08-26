import os
import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Separator, Treeview


class Progress:
    def __init__(self, filename, filesize):
        self.filename = filename
        self.filesize = filesize
        self.status = "Pending"


class FileTransferApp:
    def __init__(self, master):
        self.master = master
        master.title("File Transfer App")
        master.geometry("1300x600")
        master.resizable(False, False)

        self.directory_name = None
        self.progresses = {}
        self.received_files = {}

        # Set up GUI for sender
        sender_frame = tk.Frame(master, width=480)
        sender_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        sender_label = tk.Label(
            sender_frame, text="Sender", font=("Helvetica", 16, "bold")
        )
        sender_label.pack(pady=(0, 10))

        hostname_label = tk.Label(sender_frame, text="Hostname:")
        hostname_label.pack(pady=(10, 0), anchor=tk.W)

        hostname = socket.gethostname()
        self.sender_hostname = tk.StringVar(value=hostname)
        self.sender_hostname_entry = tk.Entry(
            sender_frame, textvariable=self.sender_hostname, state="readonly"
        )
        self.sender_hostname_entry.pack(pady=(0, 10), padx=10, fill=tk.X)

        port_label = tk.Label(sender_frame, text="Port:")
        port_label.pack(pady=(10, 0), anchor=tk.W)

        self.port_entry = tk.Entry(sender_frame)
        self.port_entry.pack(pady=(0, 10), padx=10, fill=tk.X)

        select_folder_button = tk.Button(
            sender_frame, text="Select Folder", command=self.select_folder
        )
        select_folder_button.pack(pady=(10, 20), fill=tk.X)

        self.send_files_button = tk.Button(
            sender_frame, text="Send Files", command=self.send_files
        )
        self.send_files_button.pack(fill=tk.X)

        self.status_message = tk.StringVar(value="")
        self.status_label = tk.Label(sender_frame, textvariable=self.status_message)
        self.status_label.pack(pady=(20, 10), fill=tk.X)

        self.file_table = Treeview(
            sender_frame,
            columns=("ID", "Filename", "Status", "Progress"),
            show="headings",
        )
        self.file_table.heading("ID", text="ID")
        self.file_table.heading("Filename", text="Filename")
        self.file_table.heading("Status", text="Status")
        self.file_table.heading("Progress", text="Progress")

        self.file_table.column("ID", width=50)
        self.file_table.column("Filename", width=300)
        self.file_table.column("Status", width=100)
        self.file_table.column("Progress", width=200)

        self.file_table["displaycolumns"] = ("ID", "Filename", "Status", "Progress")

        self.file_table.pack(padx=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            sender_frame, orient="vertical", command=self.file_table.yview
        )
        self.file_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        Separator(sender_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # Set up GUI for receiver
        receiver_frame = tk.Frame(master, width=480)
        receiver_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        receiver_label = tk.Label(
            receiver_frame, text="Receiver", font=("Helvetica", 16, "bold")
        )
        receiver_label.pack(pady=(0, 10))

        hostname_label2 = tk.Label(receiver_frame, text="Hostname:")
        hostname_label2.pack(pady=(10, 0), anchor=tk.W)

        hostname = socket.gethostname()
        self.receiver_hostname = tk.StringVar(value=hostname)
        self.receiver_hostname_entry = tk.Entry(
            receiver_frame, textvariable=self.receiver_hostname, state="readonly"
        )
        self.receiver_hostname_entry.pack(pady=(0, 10), padx=10, fill=tk.X)

        port_label2 = tk.Label(receiver_frame, text="Port:")
        port_label2.pack(pady=(10, 0), anchor=tk.W)

        self.port_entry2 = tk.Entry(receiver_frame)
        self.port_entry2.pack(pady=(0, 10), padx=10, fill=tk.X)

        self.receive_files_button = tk.Button(
            receiver_frame, text="Receive Files", command=self.receive_files
        )
        self.receive_files_button.pack(fill=tk.X)

        self.status_message2 = tk.StringVar(value="")
        self.status_label2 = tk.Label(receiver_frame, textvariable=self.status_message2)
        self.status_label2.pack(pady=(20, 10), fill=tk.X)

        self.file_table2 = Treeview(
            receiver_frame, columns=("Filename", "Progress"), show="headings"
        )
        self.file_table2.heading("Filename", text="Filename")
        self.file_table2.heading("Progress", text="Progress")

        self.file_table2.column("Filename", width=300)
        self.file_table2.column("Progress", width=200)

        self.file_table2["displaycolumns"] = ("Filename", "Progress")

        self.file_table2.pack(padx=10, fill=tk.BOTH, expand=True)

        scrollbar2 = tk.Scrollbar(
            receiver_frame, orient="vertical", command=self.file_table2.yview
        )
        self.file_table2.configure(yscroll=scrollbar2.set)
        scrollbar2.pack(side="right", fill="y")

        # Stretch the last row to fill the window
        master.rowconfigure(1, weight=1)

    def select_folder(self):
        self.directory_name = filedialog.askdirectory(
            initialdir=".", title="Select Folder to Send"
        )
        if self.directory_name:
            self.status_message.set(f"Selected folder: {self.directory_name}")

    def send_files(self):
        self.status_message.set("")
        hostname = self.sender_hostname.get()
        port = self.port_entry.get()
        if not port.isdigit():
            messagebox.showwarning(
                "Invalid Port Number", "Please enter a valid port number"
            )
            self.port_entry.delete(0, tk.END)
            self.port_entry.focus()
            return

        if not self.directory_name:
            messagebox.showwarning(
                "No Folder Selected", "Please select folder to send files"
            )
            return

        self.file_table.delete(*self.file_table.get_children())
        self.progresses = {}
        self.file_table_id = 1

        for root, dirs, files in os.walk(self.directory_name):
            for file_path in files:
                file_full_path = os.path.join(root, file_path)
                file_rel_path = os.path.relpath(file_full_path, self.directory_name)
                progress = Progress(file_rel_path, os.path.getsize(file_full_path))
                self.progresses[self.file_table_id] = progress

                self.file_table.insert(
                    "",
                    "end",
                    text="",
                    iid=self.file_table_id,
                    values=(self.file_table_id, progress.filename, progress.status, ""),
                )
                self.file_table_id += 1

                self.master.update()

        thread = threading.Thread(
            target=self.send_files_thread,
            args=(hostname, int(port), self.directory_name),
            daemon=True,
        )
        thread.start()

    def send_files_thread(self, hostname, port, directory):
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to a hostname and port number
            s.connect((hostname, port))

            # Send the directory name so receiver can create the folder
            s.sendall(os.path.basename(directory).encode())

            # Send the files
            for root, dirs, files in os.walk(directory):
                for file_path in files:
                    file_full_path = os.path.join(root, file_path)
                    file_rel_path = os.path.relpath(file_full_path, directory)
                    with open(file_full_path, "rb") as f:
                        file_contents = f.read()
                        s.sendall(file_rel_path.encode())
                        s.sendall(file_contents)

                    self.progresses[self.file_table_id - 1].status = "Completed"
                    self.file_table.item(
                        self.file_table_id - 1,
                        values=(
                            self.file_table_id - 1,
                            file_rel_path,
                            self.progresses[self.file_table_id - 1].status,
                            "Completed",
                        ),
                    )
                    self.file_table.item(self.file_table_id - 1, open=True)
                    self.master.update()

                    self.file_table_id += 1

            # Close the connection
            s.close()

            messagebox.showinfo("Files Sent", "The files have been successfully sent")

        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while sending the files: {e}"
            )

    def receive_files(self):
        self.status_message2.set("")
        hostname = self.receiver_hostname.get()
        port = self.port_entry2.get()
        if not port.isdigit():
            messagebox.showwarning(
                "Invalid Port Number", "Please enter a valid port number"
            )
            self.port_entry2.delete(0, tk.END)
            self.port_entry2.focus()
            return

        self.received_folder_path = filedialog.askdirectory(
            initialdir=".", title="Select Folder to Save Received Files"
        )

        if not self.received_folder_path:
            messagebox.showwarning(
                "No Folder Selected", "Please select folder to save received files"
            )
            return

        self.file_table2.delete(*self.file_table2.get_children())
        self.received_files = {}
        self.file_table_id = 1

        thread = threading.Thread(
            target=self.receive_files_thread, args=(hostname, int(port)), daemon=True
        )
        thread.start()

    def receive_files_thread(self, hostname, port):
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind the socket to the hostname and port number
            s.bind((hostname, port))

            # Listen for incoming connections
            s.listen(5)

            self.status_message2.set("Listening for incoming connections...")
            self.master.update()

            while True:
                # Accept incoming connection
                conn, address = s.accept()
                self.status_message2.set(f"Connected to {address[0]}:{address[1]}")
                self.master.update()

                # Receive the directory name
                directory_name = conn.recv(1024).decode()
                self.status_message2.set(f"Receiving files from {directory_name}")
                self.master.update()

                # Create the folder to store the received files
                receive_folder = os.path.join(self.received_folder_path, directory_name)
                os.makedirs(receive_folder, exist_ok=True)

                # Receive the files
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    if not self.received_files:
                        self.file_table2.delete(*self.file_table2.get_children())

                    file_rel_path = data.decode()
                    file_path = os.path.join(receive_folder, file_rel_path)
                    with open(file_path, "ab") as f:
                        f.write(conn.recv(1024))

                    if not os.path.isdir(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))

                    if file_rel_path not in self.received_files:
                        self.received_files[file_rel_path] = "Pending"
                        self.file_table2.insert(
                            "",
                            "end",
                            text="",
                            iid=self.file_table_id,
                            values=(file_rel_path, self.received_files[file_rel_path]),
                        )
                        self.file_table_id += 1
                        self.master.update()

                    file_size = os.path.getsize(file_path)
                    bytes_received = os.stat(file_path).st_size
                    progress = int(bytes_received / file_size * 100)

                    self.received_files[file_rel_path] = f"{progress}%"
                    self.file_table2.item(
                        file_rel_path,
                        values=(file_rel_path, self.received_files[file_rel_path]),
                    )
                    self.master.update()

                self.status_message2.set(
                    f"All files received successfully from {directory_name}"
                )
                self.master.update()

                # Close the connection
                conn.close()

        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while receiving the files: {e}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferApp(root)
    root.mainloop()
