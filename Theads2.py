#!/usr/bin/python

import threading
import time

print_lock = threading.Lock()

def runA(arg1, stop_event):
	while (not stop_event.is_set()):
		print_lock.acquire()
		printer('A\n')
		print_lock.release()
		time.sleep(0.5)
		pass
	print "Exiting A\n"

def runB(arg1, stop_event):
	input = 0
	while (not stop_event.is_set()):
		input += 1
		if input == 5:
			stop_event.set()
		else:
			print_lock.acquire()
			printer('B\n')
			print_lock.release()
		time.sleep(0.5)
		pass
	print "Exiting B\n"
        
def printer(message):
	print str(message)

if __name__ == "__main__":
	threads = [] 
	t1_stop = threading.Event()
	t1 = threading.Thread(target = runA, args=(1, t1_stop))
	t2_stop = threading.Event()
	t2 = threading.Thread(target = runB, args=(2, t2_stop))
	t1.setDaemon(True)
	t2.setDaemon(True)
	threads.append(t1)
	threads.append(t2)
	t1.start()
	t2.start()
	
	time.sleep(2)
	#stop the thread2
	t1_stop.set()
	
	for x in threads: 
		x.join()
		
	print "Done"