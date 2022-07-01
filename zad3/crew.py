import pika
import threading


def read_queue(channel, crew_id):
    def callback(ch, method, properties, body):
        print(f"Received msg: {body.decode()}")

    channel.queue_declare(queue=f'crew.{crew_id}')
    channel.queue_bind(queue=f'crew.{crew_id}', exchange="exchange1", routing_key=f'crew.{crew_id}')
    channel.basic_consume(queue=f'crew.{crew_id}', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def callback(ch, method, properties, body):
    print(f"Received msg: {body.decode()}")


def crew():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare("exchange1", exchange_type="topic")

    crew_id = input("Crew id:")

    thread = threading.Thread(target=read_queue, args=(channel, crew_id), daemon=True)  #
    thread.start()

    while True:
        item = input()
        if item == "exit":
            break
        msg = f"{crew_id} requests {item}"
        channel.basic_publish(exchange='exchange1', routing_key=f'items.{item}', body=msg.encode())
        print(f"[{crew_id}] Sent {item} request")

    connection.close()


crew()
