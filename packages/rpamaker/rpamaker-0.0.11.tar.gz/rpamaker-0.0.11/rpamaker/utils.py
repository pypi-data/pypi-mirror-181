import datetime
import logging
import os
import pathlib
import subprocess
import sys
from datetime import datetime

from rpamaker.orquestador import OrquestadorAPI


def get_base_path():
    # file_path = sys.argv[0]
    # file_location = os.path.dirname(file_path)
    file_location = os.getcwd()
    return file_location


def call_robot(keyword, variables, t_id):
    library_path = pathlib.Path(__file__).parent.resolve()
    root_path = get_base_path()
    base_path = os.path.join(root_path, f'{keyword}/')

    logging.info(f'call_robot: {keyword} {variables} {base_path}')

    output_path = os.path.join(base_path, 'output/')
    robot_path = os.path.join(base_path, f'tasks.robot')

    d = datetime.strftime(datetime.now(), '%y%m%d%H%M%S%f')
    output_file = 'output-' + d + '.xml'
    log_file = 'log-' + d + '.html'
    report_file = 'report-' + d + '.html'

    command = [
        os.path.join(base_path, 'venv/Scripts/python.exe'),
        '-m',
        'robot',
        '--pythonpath', base_path,
        '--listener', 'rpamaker.listener.Listener',
        *variables,
        '--log', os.path.join(output_path, log_file),
        '--output', os.path.join(output_path, output_file),
        '--report', os.path.join(output_path, report_file),
        robot_path,
    ]

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stdout = ''

    while True:
        nextline = process.stdout.readline()
        if nextline == b'' and process.poll() is not None:
            break

        stdout = stdout + nextline.decode('utf-8')
        sys.stdout.write(nextline.decode('utf-8'))
        sys.stdout.flush()

    exitCode = process.returncode

    orquestador = OrquestadorAPI(t_id)
    if exitCode == 0:
        orquestador.send_logs_infra(stdout)
    else:
        orquestador.send_status('FAILURE', 'Error al ejecutar el robot')
        orquestador.send_logs_infra(stdout)
