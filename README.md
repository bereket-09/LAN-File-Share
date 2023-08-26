
# LAN File Transfer App

This is a Python application that allows you to send and receive files between two computers over a network. You can select a folder to send on the sender side, and the entire folder including all subfolders and files will be sent to the receiver. On the receiver side, the files and subfolders are stored in the appropriate locations. The application provides a simple GUI that makes it easy to use.

## Installation

### Prerequisites

To use this application, you need to have Python 3.x installed on your computer. You can download it from the official website [here](https://www.python.org/downloads/).

You also need to install the following external libraries:

- tkinter
- ttk
- socket

You can install these libraries using pip, the package installer for Python.

```bash
pip install tkinter ttk socket
```

### Clone

Clone this repository to your local machine.

```bash
git clone https://github.com/bereket-09/LAN-File-Share.git
```

## Usage

1. Open the `file_transfer_app.py` file using Python IDLE or your preferred Python editor.
2. Modify the variables in the code as needed. For example, you can change the default hostname and port numbers.
3. Run the code to start the application.

```bash
python file_transfer_app.py
```

4. Select a folder to send on the sender side, and click "Send Files". The folder will be sent to the receiver.
5. On the receiver side, select a folder to store the received files, and click "Receive Files". The files and subfolders will be stored in the appropriate locations.

## Contributing

This project was created by **Bereket Zelalem**. Contributions are welcome! If you have any ideas or suggestions to improve the application, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

- This application was inspired by [this project](https://github.com/Soumi7/Simple-File-Transfer).
- Some parts of the code were adapted from [this tutorial](https://www.thepythoncode.com/article/send-receive-files-using-sockets-python).
