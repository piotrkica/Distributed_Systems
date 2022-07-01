import pika


def supplier():
    def callback(ch, method, properties, body):
        crew_id, msg = body.decode().split(" requests ")
        print(f"[{supplier_id}] Received {msg} request from crew {crew_id}")

        response = f"Supplier {supplier_id} sending {msg} to crew {crew_id}"
        print(response)
        channel.basic_publish(exchange='exchange1', routing_key=f'crew.{crew_id}', body=response.encode())

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare("exchange1", exchange_type="topic")

    supplier_id = input(f"Supplier id:")
    items_no = int(input(f"No. items:"))
    print("List those items in new line each:")
    items = [input() for _ in range(items_no)]

    for item in items:
        channel.queue_declare(queue=f'items.{item}')
        channel.queue_bind(queue=f'items.{item}', exchange="exchange1", routing_key=f'items.{item}')
        channel.basic_consume(queue=f'items.{item}', on_message_callback=callback, auto_ack=True)

    print(f'[{supplier_id}] Waiting for messages ...')
    channel.start_consuming()


supplier()
