import pika


def publish_message(rabbitmq_host: str, rabbitmq_login: str, rabbitmq_secret: str, rabbitmq_queue: str, message):
    credentials = pika.PlainCredentials(rabbitmq_login, rabbitmq_secret)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
    connection.close()
