import os
import sys

import pika
from dotenv import dotenv_values

from printfilesystem.create.create_json import CreateJson
from printfilesystem.read.read_folder import ReadFolder
from printfilesystem.store.store_json import StoreJson
from printfilesystem.store.store_mongo_pfs import StoreMongoPfs


def main():
    source_path = "/Users/marcoguastalli/temp"
    dot_env = dotenv_values(".env")

    rf = ReadFolder(source_path)
    files_in_folder = rf.read_files_in_folder_using_os()
    print("The folder with path '%s' contains %s files" % (source_path, files_in_folder.__len__()))

    cj = CreateJson(dot_env['RABBITMQ_HOST'], dot_env['RABBITMQ_LOGIN'], dot_env['RABBITMQ_SECRET'], dot_env['RABBITMQ_QUEUE'], files_in_folder)
    cj.create_and_publish()
    print("Json created and published to Rabbit MQ Queue")

    credentials = pika.PlainCredentials(dot_env['RABBITMQ_LOGIN'], dot_env['RABBITMQ_SECRET'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=dot_env['RABBITMQ_HOST'], credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=dot_env['RABBITMQ_QUEUE'])

    def consume_queue(ch, method, properties, body):
        message = body.decode('UTF-8')
        sj = StoreJson(message)
        stored_json = sj.store('http://localhost:8080/marco27-web/v1/pfs/create')
        sm_pfs = StoreMongoPfs(message)
        sm_pfs.store()
        print("Json Stored '%s'" % stored_json)

    channel.basic_consume(queue=dot_env['RABBITMQ_QUEUE'], on_message_callback=consume_queue, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
