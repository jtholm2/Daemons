#!/usr/bin/python3

"""
    This daemon was built out of not knowing how to effectively answer a couple of interview questions. I essentially merged the two questions (i.e. develop a daemon and develop a program that kills CPU intensive programs) and developed this program.

    If you wish to replicate this daemon, you will need to 'pip install python-daemon' and change the line on 56 to match the directory of where you would like the daemon to log.
"""
import time, os, subprocess
from subprocess import PIPE
from daemon import runner

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5
        
    def get_top_data(self):
        command = ['top', '-b', '-n', '1']
        result = subprocess.run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        data = result.stdout
        split_data = data.split('\n')[7:]
        
        formatted_top = []
        for item in split_data:
            temp = item.split(' ')
            list_to_add = []
            for col in temp:
                if col != '':
                    list_to_add.append(col)
            
            if len(list_to_add) > 0:
                formatted_top.append(list_to_add)
        
        return formatted_top

    def kill_program(self):
        data = self.get_top_data()
        program = []
        for row in data:
            if float(row[8]) > 85:
                program.append((row[0],row[-1], row[8]))
                os.system('kill -15 ' + row[0])
        
        if len(program) == 0:
            return 'no programs to kill'
        
        return program       


def run(self):
    while True:
        message = self.kill_program()
        file = open('/home/jtholmes/daemon-prac/syslog', 'a')
        if type(message) == str:
            file.write(time.ctime() + ' ' + message + '\n')
        else:
            for row in message:
                file.write(time.ctime() + ' terminated PID: ' + row[0] + '. ' + 'Program broke CPU threshold at: ' + row[2] + '\n')
                
        file.close()
        time.sleep(15)
        

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()   