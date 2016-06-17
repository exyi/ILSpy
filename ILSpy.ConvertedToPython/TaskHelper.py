# Copyright (c) 2014 AlphaSierraPapa for the SharpDevelop Team
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
from System import *
from System.Threading import *
from System.Threading.Tasks import *
from ICSharpCode.ILSpy.TextView import *

class TaskHelper(object):
	def __init__(self):
		self._CompletedTask = self.FromResult(None)

	def FromResult(result):
		tcs = TaskCompletionSource[T]()
		tcs.SetResult(result)
		return tcs.Task

	FromResult = staticmethod(FromResult)

	def FromException(ex):
		tcs = TaskCompletionSource[T]()
		tcs.SetException(ex)
		return tcs.Task

	FromException = staticmethod(FromException)

	def FromCancellation():
		tcs = TaskCompletionSource[T]()
		tcs.SetCanceled()
		return tcs.Task

	FromCancellation = staticmethod(FromCancellation)

	def SetFromTask(tcs, task):
		""" <summary>
		 Sets the result of the TaskCompletionSource based on the result of the finished task.
		 </summary>
		"""
		if task.Status == TaskStatus.RanToCompletion:
			tcs.SetResult(task.Result)
		elif task.Status == TaskStatus.Canceled:
			tcs.SetCanceled()
		elif task.Status == TaskStatus.Faulted:
			tcs.SetException(task.Exception.InnerExceptions)
		else:
			raise InvalidOperationException("The input task must have already finished")

	SetFromTask = staticmethod(SetFromTask)

	def SetFromTask(tcs, task):
		""" <summary>
		 Sets the result of the TaskCompletionSource based on the result of the finished task.
		 </summary>
		"""
		if task.Status == TaskStatus.RanToCompletion:
			tcs.SetResult(None)
		elif task.Status == TaskStatus.Canceled:
			tcs.SetCanceled()
		elif task.Status == TaskStatus.Faulted:
			tcs.SetException(task.Exception.InnerExceptions)
		else:
			raise InvalidOperationException("The input task must have already finished")

	SetFromTask = staticmethod(SetFromTask)

	def Then(task, action):
		if action == None:
			raise ArgumentNullException("action")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext())

	Then = staticmethod(Then)

	def Then(task, func):
		if func == None:
			raise ArgumentNullException("func")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext())

	Then = staticmethod(Then)

	def Then(task, asyncFunc):
		if asyncFunc == None:
			raise ArgumentNullException("asyncFunc")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext()).Unwrap()

	Then = staticmethod(Then)

	def Then(task, asyncFunc):
		if asyncFunc == None:
			raise ArgumentNullException("asyncFunc")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext()).Unwrap()

	Then = staticmethod(Then)

	def Then(task, action):
		if action == None:
			raise ArgumentNullException("action")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext())

	Then = staticmethod(Then)

	def Then(task, func):
		if func == None:
			raise ArgumentNullException("func")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext())

	Then = staticmethod(Then)

	def Then(task, asyncAction):
		if asyncAction == None:
			raise ArgumentNullException("asyncAction")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext()).Unwrap()

	Then = staticmethod(Then)

	def Then(task, asyncFunc):
		if asyncFunc == None:
			raise ArgumentNullException("asyncFunc")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext()).Unwrap()

	Then = staticmethod(Then)

	def Catch(task, action):
		""" <summary>
		 If the input task fails, calls the action to handle the error.
		 </summary>
		 <returns>
		 Returns a task that finishes successfully when error handling has completed.
		 If the input task ran successfully, the returned task completes successfully.
		 If the input task was cancelled, the returned task is cancelled as well.
		 </returns>
		"""
		if action == None:
			raise ArgumentNullException("action")
		return task.ContinueWith(, CancellationToken.None, TaskContinuationOptions.NotOnCanceled, TaskScheduler.FromCurrentSynchronizationContext())

	Catch = staticmethod(Catch)

	def IgnoreExceptions(task):
		""" <summary>
		 Ignore exceptions thrown by the task.
		 </summary>
		"""
		pass

	IgnoreExceptions = staticmethod(IgnoreExceptions)

	def HandleExceptions(task):
		""" <summary>
		 Handle exceptions by displaying the error message in the text view.
		 </summary>
		"""
		task.Catch().IgnoreExceptions()

	HandleExceptions = staticmethod(HandleExceptions)