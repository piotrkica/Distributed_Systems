import sys
import grpc
import base64
import climage
import argparse
from io import BytesIO
from time import time, sleep
from threading import Thread
from datetime import datetime

from protos import chat_pb2
from protos import chat_pb2_grpc

PORT = 32167


last_ack = 0


def encode_image(abs_path):
    with open(abs_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


def decode_image(b64image):
    return climage.convert(BytesIO(base64.b64decode(b64image)), width=50)


def receive_messages(stub, nick):
    global last_ack
    while True:
        try:
            for msg in stub.receive_msg(chat_pb2.Greeting(nick=nick, last_ack=last_ack)):
                last_ack += 1
                timestamp = datetime.fromtimestamp(msg.timestamp).strftime("%H:%M:%S")
                msg_repr = f"[MsgID={msg.msgID}][{timestamp}][Nick={msg.nick}]: {msg.content}"
                msg_repr += f"    (reply to msgID={msg.replyID})" if msg.replyID != "" else ""
                print(msg_repr)
                if msg.image.b64image != "" and msg.image.mimeType in ["image/png", "image/jpeg"]:
                    image = decode_image(msg.image.b64image)
                    print(image + "\n")
        except grpc.RpcError as e:
            print(e.details())
            print("Reconnecting ...")
            sleep(0.5)


def parse_input(user_input):
    content = user_input.split(' --', 1)[0]
    parser = argparse.ArgumentParser()
    for arg in ['--image', '--priority', '--replyID']:
        parser.add_argument(arg)
    args, unknown = parser.parse_known_args(user_input.split(" "))

    return {**vars(args), "content": content}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        last_ack = int(sys.argv[1])
        print(last_ack)

    channel = grpc.insecure_channel(f'localhost:{PORT}')
    stub = chat_pb2_grpc.ChatStub(channel)

    print("Client started ...")
    nick = input("Choose your nick: ")
    group = input("Choose your group: ")

    response = stub.client_update(chat_pb2.Greeting(nick=nick, group=group, last_ack=last_ack))
    thread = Thread(target=receive_messages, daemon=True, args=[stub, nick])
    thread.start()

    while True:
        user_input = input()
        if user_input == "/exit":
            break
        elif user_input == "/group":
            new_group = input("Choose new group: ")
            last_ack = 0
            response = stub.client_update(chat_pb2.Greeting(nick=nick, group=new_group, last_ack=last_ack))
            print("Changed group to " + new_group)
            continue

        parsed_input = parse_input(user_input)

        parsed_input = {k: v for k, v in parsed_input.items() if v is not None}

        if "image" in parsed_input:
            parsed_input["image"] = chat_pb2.B64Image(b64image=encode_image(parsed_input["image"]),
                                                      mimeType="image/png")

        message_to_send = chat_pb2.Msg(timestamp=int(time()), nick=nick, **parsed_input)

        try:
            response = stub.send_msg(message_to_send)
        except grpc.RpcError as e:
            print(e.details())

    channel.close()
