import zmq, os, sys

def zmqserver(port, proceso):
    print(f'ZMQSERVER puerto:{port}')
    context = zmq.Context()
    sck = context.socket(zmq.REP)

    sck.bind(f"tcp://*:{port}")
    print(f"biind: tcp://*:{port}")

    while True:
        #  Wait for next request from client
        message = sck.recv()
        msg = message.decode('utf-8')
        list_msg = msg.split('|')
        if list_msg[0] == 'STOP':
            proceso.stop()
            sck.send_string("Proceso detenido")
            sys.exit()
        elif list_msg[0] == 'RESOURCES':
            sck.send_string("Devuelvo recursos")
        elif list_msg[0] == 'PID':
            sck.send_string(str(os.getpid()))
        elif list_msg[0] == 'PPID':
            sck.send_string(str(os.getppid()))
        else:
            sck.send_string(f"Se recibio el mensaje desconocido: {list_msg[0]}")