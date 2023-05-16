import pika, sys  # import the library to connect to RabbitMQ

# Set the hostname that we'll connect to
parameters = pika.ConnectionParameters(host='rabbitmq')

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(parameters)

# Open a channel to RabbitMQ
channel = connection.channel()

# Create a queue if it does not exist
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

# Send the message to the queue
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE,
                      ))

# Print a status message
print("[x] Sent %r" % message)

# Close the connection to RabbitMQ
connection.close()
