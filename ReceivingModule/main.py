from server import TCPServer
from params import HEADERSIZE, SERVER_PORT, PIPE_NAME

if __name__ == "__main__":
    mytcp = TCPServer(HEADERSIZE, SERVER_PORT, PIPE_NAME)
    mytcp.startServer()
    mytcp.accept_recv()
    mytcp.socket.close()