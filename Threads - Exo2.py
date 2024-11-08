import threading, time

def task(thread, count):
    while count >= 0:
        print(f"thread {thread}: {count}")
        count -= 1
        time.sleep(1)
    
t1 = threading.Thread(target=task, args=[1, 4])
t2 = threading.Thread(target=task, args=[2, 7])
t1.start()
t2.start()