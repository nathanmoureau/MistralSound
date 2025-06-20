from pythonosc import udp_client, osc_message_builder, osc_server
from pythonosc.dispatcher import Dispatcher
import time


def sendMsg(sender, address, value):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(value)
    sender.send(msg.build())


def receiveMsg(address, *args):
    value = args[0]
    print(f"{address} : {value}")


if __name__ == "__main__":
    oscSender = udp_client.UDPClient("localhost", 57120)
    value = 0
    dispatcher = Dispatcher()

    # server = osc_server.ThreadingOSCUDPServer(("localhost", 57220), dispatcher)
    # server.serve_forever()
    while True:
        value += 0.1
        sendMsg(oscSender, "/langmuir", value)
        if value >= 1:
            value = 0
        dispatcher.map("/*", receiveMsg)
        time.sleep(0.5)
