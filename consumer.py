import pika, sys, os, time  # Import stuff that will be used


# Create a function that will process the message when it arrives
def process_message(ch, method, properties, body):
    print("[x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print("[x] Done")


# Create a main method to run
def main():
    # Set the hostname that we'll connect to
    parameters = pika.ConnectionParameters(host='rabbitmq')

    # Create a connection to RabbitMQ
    connection = pika.BlockingConnection(parameters)

    # Open a channel to RabbitMQ
    channel = connection.channel()

    # Create an exchange if it does not exist
    channel.exchange_declare('tasks', exchange_type='fanout')

    # Create a queue if it does not exist
    result = channel.queue_declare(queue='', exclusive=True)

    queue_name = result.method.queue

    channel.queue_bind(exchange='tasks', queue=queue_name)

    # Configure the consumer to call the process_message function
    # when a message arrives
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=process_message,
        auto_ack=True
    )

    # Print a status
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Tell RabbitMQ that you're ready to receive messages
    channel.start_consuming()


# Just extra stuff to do when the script runs
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
