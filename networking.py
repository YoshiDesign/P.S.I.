import socket
import sys, os

class MySocket():
	
	def __init__(self, sock=None, _MAXLEN=4096):
		self._MAXLEN = _MAXLEN
		if sock is None:
			self.sock = socket.socket(
								socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		self.sock.connect((host, port))

	def mysend(self, msg):
		totalsent = 0
		while totalsent < self._MAXLEN:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				break
				#raise RuntimeError("SOCKET connection broken")
			totalsent = totalsent + sent

	def myreceive(self):
		chunks = []
		bytes_recd = 0
		while bytes_recd < self._MAXLEN:
			chunk = self.sock.recv(min(self._MAXLEN - bytes_recd, 2048))
			if chunk == b'':
				#raise RuntimeError("Socket Connection Has Been broken")
				break
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return b''.join(chunks)