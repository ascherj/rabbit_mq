import pika, sys  # import the library to connect to RabbitMQ

# Set the hostname that we'll connect to
parameters = pika.ConnectionParameters(host='rabbitmq')

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(parameters)

# Open a channel to RabbitMQ
channel = connection.channel()

# Create an exchange if it does not exist
channel.exchange_declare(exchange='tasks', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "Hello World!"

# Send the message to the queue
channel.basic_publish(exchange='tasks',
                      routing_key='',
                      body=message)

# Print a status message
print("[x] Sent %r" % message)

# Close the connection to RabbitMQ
connection.close()
