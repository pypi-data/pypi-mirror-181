import mysql.connector
import socket
import datetime
import threading
import pickle

FORMAT = "utf-8"

def handle(client):
    query = client.recv(2048).decode(FORMAT)
    my_cursor.execute(query)
    my_conn.commit()
    data = my_cursor.fetchall()
    data=pickle.dumps(data)
    client.send(data)

class Server:
    def __init__(self, server_host, server_port, db_host, db_user, db_pswd, db_name):
        self.server_host = server_host
        self.server_port = server_port
        self.db_host = db_host
        self.db_user = db_user
        self.db_pswd = db_pswd
        self.db_name = db_name
    
    def startServer(self):
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_host, self.server_port))
        t = datetime.datetime.now()
        print(f"SERVER started at {t}")
        server.listen()
        
        global my_conn, my_cursor
        my_conn = mysql.connector.connect(host=self.db_host, user=self.db_user, passwd=self.db_pswd, database=self.db_name)
        my_cursor = my_conn.cursor()

        while True:
            client, addr = server.accept()
            t = datetime.datetime.now()
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    def stopServer(self):
        server.close()
        my_conn.close()

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connectClient(self):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))
        
    def askQuery(self, query):
        self.query = query
        client.send(self.query.encode(FORMAT))
        data = client.recv(2048)
        data = pickle.loads(data)
        return data

    def closeClient(self):
        client.close()