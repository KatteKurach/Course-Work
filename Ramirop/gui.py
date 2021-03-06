import Tkinter as tk
from main import *
import psutil

root = tk.Tk()
root.wm_title("Ramirop")
root.minsize(width = 900, height = 620)
root.maxsize(width = 900, height = 620)
root.resizable(width = False, height = False)

v_uptime = tk.StringVar()
v_task = tk.StringVar()
v_thr = tk.StringVar()
mem_value = tk.StringVar()
cpu_value = tk.StringVar()

flag_sort_pid = False
flag_sort_name = False
flag_filter = False
flag_search = False

select_str = ""

def get_pid():
    global select_str

    if select_str == "":
        return None
    pid = select_str.split(" ")[0]
    return pid

def kill_proc():
    pid = get_pid()
    print pid
    kill(int(pid))


def suspend_proc():
     pid = get_pid()
     suspend(int(pid))


def resume_proc():
     pid = get_pid()
     resume(int(pid))


def terminate_proc():
    pid = get_pid()
    terminate(int(pid))


def set_nice_proc():
    pid = get_pid()
    set_nice(int(pid), 10)


def view_popup(event):
    popup.tk_popup(event.x_root, event.y_root, 0)


def set_flag_pid():
    global flag_sort_pid
    global flag_sort_name
    global flag_filter
    global flag_search
    
    flag_sort_pid = True
    flag_sort_name = False
    flag_filter = False
    flag_search = False


def set_flag_name():
    global flag_sort_pid
    global flag_sort_name
    global flag_filter
    global flag_search
    
    flag_sort_pid = False
    flag_sort_name = True
    flag_filter = False
    flag_search = False



def set_flag_filter():
    global flag_sort_pid
    global flag_sort_name
    global flag_filter
    global flag_search
    
    flag_sort_pid = False
    flag_sort_name = False
    flag_filter = True
    flag_search = False


def set_flag_search():
    global flag_sort_pid
    global flag_sort_name
    global flag_filter
    global flag_search
    
    flag_sort_pid = False
    flag_sort_name = False
    flag_filter = False
    flag_search = True



btn1 = tk.Button(root, text = "Sort by pid", width = 10, fg = "#6543B5", command = set_flag_pid)
btn2 = tk.Button(root, text = "Sort by name", width = 10, fg = "#6543B5", command = set_flag_name)
btn3 = tk.Button(root, text = "Filter", width = 10, fg = "#6543B5", command = set_flag_filter)
btn4 = tk.Button(root, text = "Search", width = 10, fg = "#6543B5", command = set_flag_search)
tx = tk.Text(root, font = ('times',12), width = 75, height = 1, wrap = tk.WORD, 
        highlightbackground = "#6543B5")

scrollbar = tk.Scrollbar(root)
lb = tk.Listbox(root, font = ('Monaco', 12), width = 117, height = 25, selectbackground = "#FFE692",
        yscrollcommand = scrollbar.set)
scrollbar.config(command = lb.yview)
lb.bind("<Button-2>", view_popup)
table_row = tk.Label(root, font = ('aAssuanNr', 14), fg = "#2341B6", text = "   Pid                                     Name                                           User name              Status     Nice         Memory %              Cpu %")
uptime_l = tk.Label(root, text = 'Uptime : ', font = ('Monaco', 15), fg = "#07C8F9")
uptime_value = tk.Label(root, textvariable = v_uptime, font = ('Monaco', 15), fg = "#F9B807")
tasks_l = tk.Label(root, text = 'Tasks : ', font = ('Monaco', 15), fg = "#07C8F9")
tasks_value = tk.Label(root, textvariable = v_task, font = ('Monaco', 15), fg = "#F9B807")
run_threads_l = tk.Label(root, text = 'Run threads : ', font = ('Monaco', 15), fg = "#07C8F9")
run_threads_value = tk.Label(root, textvariable = v_thr, font = ('Monaco', 15), fg = "#F9B807")

btn1.place(x = 5, y = 600)
btn2.place(x = 105, y = 600)
btn3.place(x = 205, y = 600)
btn4.place(x = 305, y = 600)

tx.place(x = 405, y = 597) 
lb.place(x = 10, y = 140)
table_row.place(x = 10, y = 110)

uptime_l.place(x = 10, y = 20)
uptime_value.place(x = 89, y = 20) 
tasks_l.place(x = 10, y = 45)
tasks_value.place(x = 82, y = 45)
run_threads_l.place(x = 10, y = 70)
run_threads_value.place(x = 133, y = 70)

scrollbar.pack(side = tk.RIGHT, fill = tk.Y)    

memory_l = tk.Label(root, text = "Memory % :", font = ('Monaco', 15), fg = "#07C8F9")
memory_l.place(x = 570, y = 20)

cpu_l = tk.Label(root, text = "Cpu % :", font = ('Monaco', 15), fg = "#07C8F9")
cpu_l.place(x = 570, y = 45)

memory_v = tk.Label(root, textvariable = mem_value, font = ('Monaco', 15), fg = "#F9B807")
cpu_v = tk.Label(root, textvariable = cpu_value, font = ('Monaco', 15), fg = "#F9B807")

memory_v.place(x = 800, y = 20)
cpu_v.place(x = 800, y = 45)

popup = tk.Menu(root, tearoff=0)
popup.add_command(label = "Kill", command = kill_proc)
popup.add_command(label = "Suspend", command = suspend_proc)
popup.add_command(label = "Resume", command = resume_proc)
popup.add_command(label = "Terminate", command = terminate_proc)
popup.add_separator()
popup.add_command(label="Set nice", command = set_nice_proc)



def update():
    global select_str
    vw = lb.yview()
    cur_select = lb.curselection()

    lb.delete(0, tk.END)
    view_procs()
    
    p = Procs()
    p.get_processes()
    
    c1 = tk.Canvas(root, width = 101, height = 10, bg = "#C9C2C2")
    c1.place(x = 676, y = 28)

    c2 = tk.Canvas(root, width = 101, height = 10, bg = "#C9C2C2")
    c2.place(x = 676, y = 53)
   
    data = get_data()
    memory = data[0]
    cpu = data[1]
    if memory < 40:
        id1 = c1.create_rectangle(6, 6, int(memory), 8, fill = "#98FCDB", outline = "#98FCDB")
    elif memory > 80:
        id1 = c1.create_rectangle(6, 6, int(memory), 8, fill = "#FF562C", outline = "#FF562C")
    else:
        id1 = c1.create_rectangle(6, 6, int(memory), 8, fill = "#FFFC97", outline = "#FFFC97")
    if cpu < 40:
        id2 = c2.create_rectangle(6, 6, int(cpu), 8, fill = "#98FCDB", outline = "#98FCDB")
    elif cpu > 50:
        id2 = c2.create_rectangle(6, 6, int(cpu), 8, fill = "#FF562C", outline = "#FF562C")
    else:
        id2 = c2.create_rectangle(6, 6, int(cpu), 8, fill = "#FFFC97", outline = "#FFFC97")
    
    mem_value.set(str(memory) + "%")
    cpu_value.set(str(cpu) + "%")
    v_task.set(p.get_num())
    v_uptime.set(get_uptime())
    v_thr.set(get_thread())
    select = 0
        
    if len(cur_select) != 0:
        select = cur_select[0]
    select_str = lb.get(select, select)[0]
    lb.select_set(select)
    lb.yview_moveto(vw[0])
    root.update()
    root.after(2000, update())


def get_data():
    pr = Procs()
    procs = pr.get_processes()

    memory = psutil.virtual_memory()[2]
    cpu = psutil.cpu_percent()
    return (memory, cpu)


def view_procs():
    global flag_sort_pid
    global flag_sort_name
    global flag_filter
    global flag_search
    
    pr = Procs()
    procs = pr.get_processes() 

    if flag_sort_pid:
        procs = pr.sort_by_pid()
    if flag_sort_name:
        procs = pr.sort_by_name()
    if flag_filter:
        text = tx.get(1.0, tk.END)
        if text != " " and text != "":
            procs = pr.my_filter(text)
    if flag_search:
        text = tx.get(1.0, tk.END)
        if text != " " and text != "":
            procs = pr.search(text)
    for i in xrange(len(procs)):
        lb.insert(i, str(procs[i]))
        lb.itemconfig(i, foreground = "#6543B5")


view_procs()
root.after(1000, update())
root.mainloop()
