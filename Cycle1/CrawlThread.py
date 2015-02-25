import threading
import ctypes
import inspect

'''
Class defining a threaded social media crawling base class. 
Contains methods handling thread termination by exception throwing.

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class CrawlThread(threading.Thread):
    	def _get_my_tid(self):
		if not self.isAlive():
		    raise threading.ThreadError("the thread is not active")

		# do we have it cached?
		if hasattr(self, "_thread_id"):
		    return self._thread_id

		# no, look for it in the _active dict
		for tid, tobj in threading._active.items():
		    if tobj is self:
		        self._thread_id = tid
		        return tid

		raise AssertionError("could not determine the thread's id")

	def raiseExc(self, exctype):
        	self._async_raise( self._get_my_tid(), exctype )

	def _async_raise(self, tid, exctype):

	    if not inspect.isclass(exctype):
		raise TypeError("Only types can be raised (not instances)")
	    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
		                                          ctypes.py_object(exctype))
	    if res == 0:
		raise ValueError("invalid thread id")
	    elif res != 1:
		# "if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
		raise SystemError("PyThreadState_SetAsyncExc failed")

