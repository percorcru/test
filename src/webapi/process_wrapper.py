import zmq, sys, os, time, psutil, random, subprocess, signal

class ProcessWrapper:

    def __init__(self, port=0, pid=0, params=''):
        self.port = int(port)
        self.pid = int(pid)
        self.params = params

        # esto importarlo de config
        self.localpath = (os.path.dirname(__file__))

    def __find_free_port(self):
        list_conn = psutil.net_connections()
        while True:
            rnd = random.randint(60000,64000)
            if list_conn == []:
                return rnd
            for item in list_conn:
                if item not in list(map(lambda x: x.laddr[1], list_conn)):
                    return rnd

    def __listen_port(self, port):
        print('__listen_port')
        list_conn = psutil.net_connections()
        for item in list_conn:
            if item.laddr[1] == int(port) and item.status == 'LISTEN':
                return True
        return False

    def send_message_to_process(self, mensaje):
        print('send_message_to_process')
        if not self.__listen_port(self.port):
            print('servidor no disponible')
            return None
        with zmq.Context() as zmqcontext:
            zmq_socket = zmqcontext.socket(zmq.REQ)
            zmq_socket.connect(f"tcp://localhost:{self.port}")
            zmq_socket.send_string(mensaje)
            message = zmq_socket.recv()
            zmq_socket.close()
            return message.decode()

    def launch_process(self):
        print('launch_process...')
        self.port = self.__find_free_port()
        print('puerto ->', self.port)
        if sys.platform == 'win32':
            # print(f'{sys.executable} "{self.localpath}\\launcher.py" {self.port} "{self.params}" ')
            p = subprocess.Popen(f'{sys.executable} "{self.localpath}\\launcher.py" {self.port} {self.params}', shell=True, creationflags = subprocess.CREATE_NEW_CONSOLE)
        elif sys.platform == 'linux':
            subprocess.Popen(f'{sys.executable} "{self.localpath}/launcher.py" {self.port} "{self.params}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for i in range(10):
            time.sleep(1)
            if self.__listen_port(self.port):
                self.pid = int(self.send_message_to_process('PID'))
                print(int(self.send_message_to_process('PPID')))
                break
        print('pid proceso ->', self.pid)

        return {'puerto': self.port, 'pid': self.pid}

    def stop_process(self) -> str:
        """Envía señal al proceso (zmq server) para cancelarlo

        Args:
            port (int): puerto de intercomunicación

        Returns:
            str | None: respuesta del proceso
        """
        rpta = self.send_message_to_process('STOP')
        # if rpta is None:
        #     print('retirar el proceso de la db')
        return rpta

    def kill_process(self):
        """Envía señal del sistema SIGTERM para terminar el proceso

        Args:
            pid (int): pid
        """
        try:
            os.kill(self.pid, signal.SIGTERM)
        except:
            pass

    def get_resources(self):
        cpu_porcent = psutil.Process(self.pid).cpu_percent(interval=0.5)
        ram_mb = psutil.Process(self.pid).memory_info().rss / (1024*1024)

        return {'cpu_porcent': cpu_porcent, 'ram_mb': ram_mb}



