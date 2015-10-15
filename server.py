import socket
import sys
from threading import Thread
from Queue import Queue
import os

HOST = '' #host becomes any address the machine happens to have
PORT = int(sys.argv[1]) #get the port from the command line arguments and convert to int
STUDENT_ID = '39e95f0efebef82542626bd6c3c28765726768817d45d38b2d911b26eb5d0b37'

class Worker(Thread):
	"""individual thread that handles the clients requests"""
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks #each task will be an individual connection
		self.daemon = True
		self.start()

	def run(self):
		#run forever
		while True:
			conn = self.tasks.get() #take a connection from the queue
			data = conn.recv(2048)
			if data.startswith("HELO ") :
				reply = '{}IP:{}\nPort:{}\nStudentID:{}\n'.format(data,my_socket.getsockname()[0],PORT,STUDENT_ID)
			
			elif data == "KILL_SERVICE\n" : 
				my_socket.close()
				os._exit(0) #exits the program				
			
			else:
				reply = '' #any other message
			conn.sendall(reply)
			self.tasks.task_done()

class ThreadPool:
	"""pool of worker threads all consuming tasks"""
	def __init__(self,num_thread):
		self.tasks = Queue(num_thread)
		for _ in range(num_thread):
			Worker(self.tasks)

	def add_tasks(self, conn):
		#put a new connection on the queue
		self.tasks.put((conn))
		



#socket binding:
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	my_socket.bind((HOST,PORT))
except socket.error , msg:
	print 'binding failed, error: ' + str(msg[0])
	sys.exit()
print 'succesful bind'
my_socket.listen(5)
print 'listening now'

#init a thread pool:
pool = ThreadPool(20)

#keep the server alive 
while True:
	connection, addr = my_socket.accept() #blocking call to wait for a connection
	print 'connected with ' + addr[0] + ' port: ' + str(addr[1])
	pool.add_tasks(connection)

my_socket.close()



