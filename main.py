import argparse
import zmq
import time

def main():
  parser = argparse.ArgumentParser(
    prog="Proxy Tester",
  )

  parser.add_argument("-s", "--sender", action="store_true")
  parser.add_argument("-r", "--receiver", action="store_true")
  parser.add_argument("-l", "--logger", action="store_true")
  parser.add_argument("-u", "--url", const="localhost", nargs="?", default="localhost")

  args = parser.parse_args()

  if (args.sender):
    sender(args.url)
  elif (args.receiver):
    receiver(args.url)
  elif (args.logger):
    logger(args.url)
    
def logger(url: str):
  context = zmq.Context()
  socket = context.socket(zmq.SUB)
  socket.connect(f"tcp://{url}:9960")
  socket.subscribe("")
  print("logging")

  while True:
    msg = socket.recv()
    print(msg)

def sender(url: str):
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect(f"tcp://{url}:9951")

  while True:
    time.sleep(0.5)
    socket.send_string("heartbeat 00:00:00:00:00:00")
    socket.recv_string()

def receiver(url: str):
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.connect(f"tcp://{url}:9950")
  i = 0;

  while True:
    message = socket.recv_string()
    print(i)
    socket.send_string("ACK")
    i += 1


if __name__ == "__main__":
  main()