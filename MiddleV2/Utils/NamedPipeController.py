#!/usr/bin/env python3

import sys
import time
import json
import threading
import win32file
import pywintypes
from attrdict import AttrDict

class NamedPipeController:

	def __init__(self, abort, name, server_to_client, client_to_server, chunk_size):
		self.abort = abort
		self.name = name
		self.chunk_size = chunk_size
		self.server_to_client = server_to_client
		self.client_to_server = client_to_server
		self.pipe_in = None
		self.pipe_out = None
		self.running = False

	def _connect(self, suffix, flag):
		try:
			return win32file.CreateFile(r'\\.\pipe\{}_{}'.format(self.name, suffix), flag, 0, None, win32file.OPEN_EXISTING, 0, None)
		except:
			return None

	def connect(self):
		while self.running:
			if not self.pipe_in:
				self.pipe_in = self._connect(self.server_to_client, win32file.GENERIC_READ)
			elif not self.pipe_out:
				self.pipe_out = self._connect(self.client_to_server, win32file.GENERIC_WRITE)
			else:
				break

	def _hide_legitimate_errors(f):
		def func(self, *args, **kwargs):
			try:
				return f(self, *args, **kwargs)
			except pywintypes.error as e:
				if self.running:
					raise
		func.__name__ = f.__name__
		return func

	@_hide_legitimate_errors
	def read(self):
		'''Reads a json object'''
		error, msg = win32file.ReadFile(self.pipe_in, self.chunk_size)
		assert not error, error
		s = msg.rstrip(b'\x00').decode()
		return None if not s else AttrDict(json.loads(s))

	@_hide_legitimate_errors
	def write(self, msg):
		'''Writes a json object'''
		s = json.dumps(msg)
		win32file.WriteFile(self.pipe_out, (s + '\r\n').encode())

	def _read(self, cb):
		self.connect()
		try:
			while self.running:
				cb(self.read())
		except:
			self.stop()
			raise

	def start(self, read_callback):
		self.running = True
		self.reader = threading.Thread(target=self._read, args=(read_callback,))
		self.reader.start()

	def stop(self):
		'''Closes pipes'''
		if not self.running:
			return
		self.running = False
		for pipe in (self.pipe_in, self.pipe_out):
			if pipe:
				win32file.CloseHandle(pipe)
		try:
			self.reader.join()
		except RuntimeError:
			pass
		self.abort()
