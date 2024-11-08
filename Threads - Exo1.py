import threading, time

def task(i):
    for n in range(5):
        print(f"Task {i}")
        time.sleep(1)
    
t1 = threading.Thread(target=task, args=[1])
t2 = threading.Thread(target=task, args=[2])
t1.start()
t2.start()