
import threading
import zmqserver
import sys
import os
from importlib import import_module

# import logging
# logging.basicConfig(filename='a.log', encoding='utf-8', filemode='w', level=logging.DEBUG)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# from robots.robot import Robot

if __name__ == '__main__':
    if len(sys.argv) > 1:
        puerto = int(sys.argv[1])
        params = sys.argv[2].split('|')
        
        # class_str: str = 'robots.robot.Robot'
        # class_str = config['GENERAL']['class']
        class_str = 'robots.' + os.environ['ROBOT_NAME']
        try:
            module_path, class_name = class_str.rsplit('.', 1)
            module = import_module(module_path)
            robot_class =  getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(class_str)

        robot = robot_class()
        # robot = Robot()

        d = threading.Thread(target=zmqserver.zmqserver, args=(puerto, robot,))
        d.daemon = True
        d.start()

        robot.start_app(
            # allparams=params[0]
            ccust=params[0],
            country=params[1] if params[1] != 'None' else '',
            document=params[2],
            pc=params[3]
        )

        sys.exit()
