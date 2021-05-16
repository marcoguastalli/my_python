import os
import pika
import sys


def main():
    credentials = pika.PlainCredentials('admin', 'qwerty')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='python.rabbitmq.queue')

    message = b'I am a message for the queue'
    channel.basic_publish(exchange='', routing_key='python.rabbitmq.queue', body=message)
    print("Message Sent: '%s'" % message)
    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
