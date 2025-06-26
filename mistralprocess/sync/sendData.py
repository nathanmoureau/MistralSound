from pythonosc import udp_client, osc_message_builder

# from pythonosc.dispatcher import Dispatcher
# from pythonosc.osc_server import ThreadingOSCUDPServer
import time


def sendMsg(sender, address, value):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(value)
    sender.send(msg.build())


def receiveMsg(address, *args):
    value = args[0]
    print(f"{address} : {value}")


if __name__ == "__main__":
    oscSender = udp_client.UDPClient("127.0.0.1", 57120)
    value = 0

    # server = osc_server.ThreadingOSCUDPServer(("localhost", 57220), dispatcher)
    # server.serve_forever()
    while True:
        print("top")
        value += 0.1
        sendMsg(oscSender, "/langmuir", value)
        if value >= 1:
            value = 0
        time.sleep(0.5)
