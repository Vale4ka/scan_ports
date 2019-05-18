import socket
import threading
import queue as Q
import os
from queue import Queue
import time
q = Q.PriorityQueue()
q2 = Queue()
ScannedCount = 0
lock=threading.Lock()


hst = 'google.com'
def thr(p,data):
    global q
    global ScannedCount
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock1.connect((data, p))
        q.put(p)
        sock1.close()
    except socket.error:
        c=None
    with lock:
        ScannedCount += 1

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    os.system("cls")
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print()

def ThreadPB ():
    Progress = 0
    LastProgress = Progress
    while Progress < 65536:
        with lock:
            Progress = ScannedCount
        if LastProgress != Progress:
            printProgressBar(Progress, 65536, prefix='Progress:', suffix='Complete')
            LastProgress = Progress
            time.sleep(0.1)


ProgressThread = threading.Thread(target=ThreadPB)
ProgressThread.start()
Step = 700
for i in range(0,65536,Step):
    count = 65536 - i
    count = min(count, Step)
    for j in range(0,count):
        my_thread = threading.Thread(target=thr,args=(i+j,hst))
        my_thread.start()
        q2.put(my_thread)


    while not q2.empty():
        thread = q2.get()
        thread.join()

while not q.empty():
    ProgressThread.join()
    print(q.get())






