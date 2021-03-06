import psutil
from uptime import uptime
import os
import signal
import re
import threading

class Proc(object):
    def __init__(self, pid, name, username, status, nice, memory_percent, cpu_percent):
        self.pid = pid
        self.name = name
        self.username = username
        self.status = status
        self.nice = nice
        if memory_percent == None:
            self.mem_p = 0
        else:
            self.mem_p = memory_percent
        if cpu_percent == None:
            self.cpu_p = 0
        else:
            self.cpu_p = cpu_percent

    def __str__(self):
        t = " | "
        space = " "
        max1 = 5 - len(str(self.pid))
        max2 = 41 - len(str(self.name))
        max3 = 15 - len(str(self.username))
        max4 = 8 - len(str(self.status))
        max5 = 2 - len(str(self.nice))
        max6 = 15 - len(str(self.mem_p))
        return str(self.pid) + space * max1 + t + \
               str(self.name) + space * max2 + t + \
               self.username + space * max3 + t + \
               self.status + space * max4 + t +  \
               str(self.nice) + space * max5 + t + \
               str(self.mem_p) + space * max6 + t + \
               str(self.cpu_p)

def kill(pid):
    os.kill(pid, signal.SIGKILL)

def suspend(pid):
    os.kill(pid, signal.SIGSTOP)

def resume(pid):
    os.kill(pid, signal.SIGCONT)

def terminate(pid):
    os.kill(pid, signal.SIGTERM)

def set_nice(p_id, n):
    p = psutil.Process(pid = p_id)
    p.nice(n)



class Procs(object):
    def __init__(self):
        self.list_procs = []
        self.num_proc = 0

    def get_processes(self):
        for p in psutil.process_iter():
            try:
                info = p.as_dict([ 'pid', 'username', 'nice', 'memory_info',
                                    'memory_percent', 'cpu_percent',
                                    'cpu_times', 'name', 'status'])
                new_process = Proc(info['pid'], info['name'], info['username'],
                        info['status'], info['nice'], info['memory_percent'],
                        info['cpu_percent'])
                self.list_procs.append(new_process)
            except psutil.NoSuchProcess:
                print "Error in get proc" + p
        self.num_proc = len(self.list_procs)
        return self.list_procs                                                                           

    def sort_by_pid(self):
        return sorted(self.list_procs, key = lambda p: p.pid)

    def sort_by_name(self):
        return sorted(self.list_procs, key = lambda p: p.name)
    
    def my_filter(self, s):
        result = []
        s = s[:-1]
        for p in self.list_procs:
            info = str(p)
            if s in info:
                result.append(p)
        return result
    
    def search(self, s):
        ans = []
        s = s[:-1]
        for p in self.list_procs:
            m = re.match('['+ s +']+', str(p.name))
            if m != None:
                ans.append(p)
        return ans

    def get_num(self):
        return str(self.num_proc)


def get_uptime():
    time = uptime()
    hours = int(time / 3600)
    minutes = int((time - hours * 3600) / 60)
    seconds = int(time - hours * 3600 - minutes * 60)
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)

def get_thread():
    return  threading.activeCount()                             

def main():
    pr = Procs()
    pr.get_processes()
    l = pr.my_filter('co')
    for p in l:
       print str(p)


if __name__ == "__main__":
    main()
