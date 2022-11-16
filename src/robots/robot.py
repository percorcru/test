import time
import argparse


class Robot:
    def __init__(self):
        # self.name = name
        self.set_estado('creado')
    
    def set_estado(self, st):
        self.estado = st
        print(f'estado -> {self.estado}')

    def start_app(self, **kwargs):
        print('inicio del proceso')
        self.set_estado('iniciado')
        time.sleep(2)
        self.cont = 1
        while True:
            self.set_estado(f'procesando -> {self.cont}')
            time.sleep(2)
            if self.cont == 0:
                break
            self.cont += 1
            
    
    def stop(self):
        self.set_estado('finalizado')
        self.cont = 0

    def __repr__(self) -> str:
        return f'instancia de worker -> {self.name}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Linea de comandos Task bash')

    parser.add_argument('-opts', type=str, help="Ingresar opciones", nargs=5)
    args = parser.parse_args()

    obj = Robot()
    obj.start_app(
        ccust=args.opts[0],
        country=args.opts[1] if args.opts[1] != 'None' else '',
        document=args.opts[2],
        pc=args.opts[3]
    )

