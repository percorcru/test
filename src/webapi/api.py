from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import sqlite3
import sys
from webapi.process_wrapper import ProcessWrapper
import subprocess

app = Flask(__name__)
CORS(app)
api = Api(app)


class Tasks:
    def __init__(self):
        if sys.platform == 'win32':
            self._ruta_db = './data/tasksdb.db'
        elif sys.platform == 'linux':
            self._ruta_db = '/data/tasksdb.db'
        # self._ruta_db = os.path.dirname(
        # os.path.realpath(__file__)) + '/' + nombre_archivo_log
        self._con = sqlite3.connect(self._ruta_db)

        cur = self._con.cursor()
        sql_crea = """  CREATE TABLE IF NOT EXISTS tasks (
                        pid INT,
                        port INT,
                        params TEXT
                    ); """
        cur.execute(sql_crea)
        cur.close()

    def get_list(self):
        cur = self._con.cursor()
        li = []
        for row in cur.execute('select pid, port, params from tasks').fetchall():
            li.append([row[0], row[1], row[2]])
        cur.close()
        return li

    def add_task(self, pid, port, params):
        sql_insert = f"INSERT INTO tasks VALUES ({pid}, {port}, '{params}')"
        cur = self._con.cursor()
        cur.execute(sql_insert)
        self._con.commit()
        cur.close()

    def remove_task(self, pid):
        sql_remove = f"DELETE FROM tasks WHERE pid={pid}"
        cur = self._con.cursor()
        cur.execute(sql_remove)
        self._con.commit()
        cur.close()

    def __del__(self):
        self._con.close()


class Execute(Resource):
    def post(self):
        response = {'status': 'success', 'message': '', 'data': None}
        try:
            json_data = request.get_json(force=True)
            print(json_data['params'])
            process = ProcessWrapper(params=json_data['params'])
            response = process.launch_process()
            db = Tasks()
            db.add_task(response['pid'], response['puerto'], json_data['params'])
        except:
            response['status'] = 'error'
        return response


class Stop(Resource):
    def post(self):
        response = {'status': 'success', 'message': '', 'data': None}
        try:
            json_data = request.get_json(force=True)
            port = json_data['port']
            pid = json_data['pid']
            process = ProcessWrapper(port=port, pid=pid)
            process.stop_process()
            db = Tasks()
            db.remove_task(pid)
            response['message'] = 'task removed'
        except:
            response['status'] = 'error'
        return response


class Kill(Resource):
    def post(self):
        response = {'status': 'success', 'message': '', 'data': None}
        try:
            json_data = request.get_json(force=True)
            pid = json_data['pid']
            import os
            import signal
            os.kill(pid, signal.SIGTERM)
            response['message'] = 'kill sended'
        except:
            response['status'] = 'error'
        return response


class GetTasks(Resource):
    def post(self):
        response = {'status': 'success', 'message': '', 'data': None}
        try:
            db = Tasks()
            ls = []
            for elem in db.get_list():
                ls.append({'pid': elem[0], 'port': elem[1], 'params': elem[2]})
            response['data'] = ls
        except:
            response['status'] = 'error'
        return response

class KillZombies(Resource):
    def post(self):
        response = {'status': 'success', 'message': '', 'data': None}
        try:
            process = subprocess.run(args=["kill", "-HUP", "`ps -A -ostat,ppid | grep -e '^[Zz]' | awk '{print $2}'`"],
                           stdout=subprocess.PIPE,
                           stdin=subprocess.PIPE,
                           encoding='utf8'
                           )
            if process.stderr is not None:
                response['status'] = 'error'
                response['message'] = process.stderr
            else:
                response['message'] = process.stdout
        except:
            response['status'] = 'error'
        return response


api.add_resource(Execute, '/execute')
api.add_resource(Stop, '/stop')
api.add_resource(Kill, '/kill')
api.add_resource(GetTasks, '/gettasks')
api.add_resource(KillZombies, '/killzombies')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# pl = ProcessWrapper()
# print(pl.launch_process(''))
