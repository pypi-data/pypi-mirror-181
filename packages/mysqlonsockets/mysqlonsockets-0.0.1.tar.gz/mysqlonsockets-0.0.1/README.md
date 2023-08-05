# mysqlonsockets


```cmd
pip install mysqlonsockets
```

Developed by Vedant Barhate (c) 2022

You need basic knowledge of Python And MySQL to use this package.

This package is useful when you want to use your MySQL database from one device on another devices.


## Example

### Creating A Server
```python
from mysqlonsockets import Server
server = Server(server_host='<IPv4 addr>', server_port=9999, db_host='localhost', db_user='root', db_pswd='<user-pswd>', db_name='<database name>')
server.startServer()
# When You Are Done
server.stopServer()
```

### Creating A Client
```python
from mysqlonsockets import Client
client = Client(host='<IPv4 addr of device to join>', port=9999)
client.connectClient()
data = askQuery('<SQL-Query>')
print(data)
# When You Are Done
client.closeClient()
```