import os
import grpc
import pickle
from datetime import datetime
from concurrent import futures
from collections import defaultdict

from protos import chat_pb2
from protos import chat_pb2_grpc

PORT = 32167


class Server(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.chat_history = defaultdict(list)  # group: group_chat_history
        self.group_map = {}                    # client: group
        self.ack_map = {}                      # client: last_ack
        if os.path.exists("server_state.pickle"):
            with open("server_state.pickle", "rb") as f:
                self.chat_history, self.group_map, self.ack_map = pickle.load(f)

    def __update_state(self):
        with open(b"server_state.pickle", "wb+") as f:
            pickle.dump((self.chat_history, self.group_map, self.ack_map), f)

    def send_msg(self, request, context):
        group = self.group_map[request.nick]
        msgID = len(self.chat_history[group])
        timestamp = datetime.fromtimestamp(request.timestamp).strftime("%H:%M:%S")
        setattr(request, "msgID", msgID)
        self.chat_history[group].append(request)
        self.__update_state()

        msg_repr = f"[Group={self.group_map[request.nick]}][MsgID={msgID}][{timestamp}][Nick={request.nick}]:" \
                   f" {request.content}  {'*image*' if request.image.b64image != '' else ''}"
        msg_repr += f"    (reply to msgID={request.replyID})" if request.replyID != "" else ""
        print(msg_repr)

        return chat_pb2.Empty()

    def receive_msg(self, request, context):
        self.ack_map[request.nick] = request.last_ack
        self.__update_state()
        msg_counter = request.last_ack
        group = self.group_map[request.nick]

        while True:
            if group != self.group_map[request.nick]:
                group = self.group_map[request.nick]
                msg_counter = self.ack_map[request.nick]

            while len(self.chat_history[group]) > msg_counter:
                msg = self.chat_history[group][msg_counter]
                msg_counter += 1
                if msg.nick == request.nick:
                    continue
                yield msg

    def client_update(self, request, context):
        self.group_map[request.nick] = request.group
        self.ack_map[request.nick] = request.last_ack
        self.__update_state()

        return chat_pb2.Empty()


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(Server(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()

    print("Server started ...")

    server.wait_for_termination()
