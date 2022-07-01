import subprocess
import sys

from kazoo.client import KazooClient


class Client:
    proc = None
    init = True
    nodes = []

    def __init__(self, app):
        self.zk = KazooClient(hosts=['127.0.0.1:2181', '127.0.0.1:2182', '127.0.0.1:2183'])
        self.zk.start()
        self.app = app

    def start(self):
        self.watch_app()
        self.watch_node_and_children("/z")
        self.init = False

        while True:
            user_input = input()
            if user_input == "/exit":
                break
            elif user_input == "/tree":
                self.print_tree()
            elif user_input == "/nodes":
                self.print_nodes()

        self.zk.stop()

    def watch_app(self):
        @self.zk.DataWatch("/z")
        def startapp(data, stat):
            if stat is not None:
                print("Running app")
                self.proc = subprocess.Popen([self.app])
                pass
            else:
                if self.proc:
                    self.proc.kill()
                    print("Process has been terminated")
                else:
                    print("Process not found")

    def watch_node_and_children(self, node):

        @self.zk.DataWatch(node)
        def set_watch(data, stat):
            if stat is not None:
                self.nodes.append(node)

                @self.zk.ChildrenWatch(node)
                def set_children_watch(children):
                    for child in children:
                        child_path = node + "/" + child
                        if child_path not in self.nodes:
                            self.watch_node_and_children(child_path)

                if not self.init:
                    print("Node added")
            else:
                if node in self.nodes:
                    self.nodes.remove(node)
                    print("Node removed")

            descendants = len(self.nodes)
            if "/z" in self.nodes:
                descendants -= 1
            print("Current number of descendants = " + str(descendants))

    def print_tree(self):
        nodes = sorted(self.nodes)
        nodes = [(node, node[node.rfind("/"):], node.count("/")-1) for node in nodes]
        for path, basename, depth in nodes:
            print('\t' * depth + " " + basename)

    def print_nodes(self):
        print(self.nodes)


# C:\Program Files (x86)\Windows Media Player\wmplayer.exe
# C:\WINDOWS\system32\notepad.exe
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python zookeeper_lab.py <absolute/path/to/app.exe>")
        exit()

    app = sys.argv[1]
    client = Client(app)
    client.start()
