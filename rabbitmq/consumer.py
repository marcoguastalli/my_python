import os
import pika
import sys


def main():
    credentials = pika.PlainCredentials('admin', 'qwerty')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='python.rabbitmq.queue')

    def callback(ch, method, properties, body):
        print("Message Received: '%r'" % body)

    channel.basic_consume(queue='python.rabbitmq.queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. Interrupt to exit.')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
