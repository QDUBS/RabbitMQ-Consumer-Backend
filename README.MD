# Sales Order Consumer Documentation

This documentation provides an overview of the `SalesOrderConsumer` class, which is responsible for consuming messages from a RabbitMQ queue and creating sales orders in the Odoo ERP system based on the received data.

## Table of Contents

1. [Introduction](#introduction)
2. [Dependencies](#dependencies)
3. [Class Overview](#class-overview)
   - [Constructor](#constructor)
   - [connect](#connect)
   - [create_channel](#create-channel)
   - [start_consuming](#start-consuming)
   - [disconnect](#disconnect)
   - [callback](#callback)
   - [create_sales_order](#create-sales-order)

## 1. Introduction<a name="introduction"></a>

The `SalesOrderConsumer` class is a Python script designed to connect to a RabbitMQ queue, consume incoming messages, and create sales orders in the Odoo ERP system based on the received data. It is a critical component in integrating external systems with Odoo for handling sales orders.

## 2. Dependencies<a name="dependencies"></a>

The script relies on several external Python packages and modules, which need to be installed for it to function correctly. These dependencies include:

- `os`: Operating system interface for basic functionality.
- `sys`: Provides access to some variables used or maintained by the interpreter.
- `odoo.odoo`: Import from Odoo's Python API (assuming Odoo is installed and properly configured).
- `pika`: Python library for interacting with RabbitMQ.
- `json`: Used for parsing JSON data.
- `odoorpc`: Python library for connecting and interacting with Odoo ERP via XML-RPC.
- Custom modules (`utils.get_user`, `utils.logger`) are used for specific functionality.

## 3. Class Overview<a name="class-overview"></a>

### Constructor<a name="constructor"></a>

```python
def __init__(self, url, queue) -> None:
```

- Initializes the `SalesOrderConsumer` instance.
- `url`: RabbitMQ connection URL.
- `queue`: The name of the RabbitMQ queue to consume messages from.

### connect<a name="connect"></a>

```python
def connect(self):
```

- Establishes a connection to RabbitMQ.
- Retries connection in case of errors (up to 5 times).
- Returns the connection object if successful, or `None` if unsuccessful.

### create_channel<a name="create-channel"></a>

```python
def create_channel(self):
```

- Creates a channel on the established RabbitMQ connection.
- Returns the channel object if successful, or `None` if the connection is not established.

### start_consuming<a name="start-consuming"></a>

```python
def start_consuming(self):
```

- Starts consuming messages from the specified RabbitMQ queue.
- Creates a connection and channel if not already established.
- Handles keyboard interrupt to gracefully exit.

### disconnect<a name="disconnect"></a>

```python
def disconnect(self):
```

- Closes the RabbitMQ connection.

### callback<a name="callback"></a>

```python
def callback(self, ch, method, properties, body):
```

- Callback function to process incoming messages.
- Parses JSON data from the message and calls `create_sales_order` method.

### create_sales_order<a name="create-sales-order"></a>

```python
def create_sales_order(self, data):
```

- Creates a sales order in Odoo ERP based on the received data.
- Data includes customer information and product details.
- Handles various exceptions and logs error messages.

This documentation provides an overview of the `SalesOrderConsumer` class, its methods, and their functionalities. Proper configuration of RabbitMQ and Odoo is essential for this script to work as intended. Additionally, ensure that the required dependencies are installed before running the script.

2. Dependencies<a name="dependencies"></a>
   The script relies on several external Python packages and modules, which need to be installed for it to function correctly. These dependencies include:

os: Operating system interface for basic functionality.
sys: Provides access to some variables used or maintained by the interpreter.
odoo.odoo: Import from Odoo's Python API (assuming Odoo is installed and properly configured).
pika: Python library for interacting with RabbitMQ.
json: Used for parsing JSON data.
odoorpc: Python library for connecting and interacting with Odoo ERP via XML-RPC.
Custom modules (utils.get_user, utils.logger) are used for specific functionality. 3. Class Overview<a name="class-overview"></a>
Constructor<a name="constructor"></a>

```python
def **init**(self, url, queue) -> None:
```
Initializes the SalesOrderConsumer instance.
url: RabbitMQ connection URL.
queue: The name of the RabbitMQ queue to consume messages from.
connect<a name="connect"></a>

```python
def create_channel(self):
```
Creates a channel on the established RabbitMQ connection.
Returns the channel object if successful, or None if the connection is not established.
start_consuming<a name="start-consuming"></a>

```
def start_consuming(self):
```

Starts consuming messages from the specified RabbitMQ queue.
Creates a connection and channel if not already established.
Handles keyboard interrupt to gracefully exit.
```
disconnect<a name="disconnect"></a>
```
```
python
def disconnect(self):
```
Closes the RabbitMQ connection.
callback<a name="callback"></a>
python

```python
def callback(self, ch, method, properties, body):
```

Callback function to process incoming messages.
Parses JSON data from the message and calls create_sales_order method.

```python
def create_sales_order(self, data):
```
Creates a sales order in Odoo ERP based on the received data.
Data includes customer information and product details.
Handles various exceptions and logs error messages.
This documentation provides an overview of the SalesOrderConsumer class, its methods, and their functionalities. Proper configuration of RabbitMQ and Odoo is essential for this script to work as intended. Additionally, ensure that the required dependencies are installed before running the script.
