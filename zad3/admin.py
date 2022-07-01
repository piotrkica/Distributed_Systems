import pika


def admin():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare("exchange1", exchange_type="topic")

    print(f"Admin running ...")
    channel.queue_declare(queue=f'admin')
    channel.queue_bind(queue="admin", exchange="exchange1", routing_key="#")

    def callback(ch, method, properties, body):
        print(f"{body.decode()}")

    channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
    print(f'[Admin] Waiting for messages ...')
    channel.start_consuming()


admin()
