# Copyright (c) 2011 AlphaSierraPapa for the SharpDevelop Team
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
from System.Collections.Generic import *
from System.Linq import *
from System.Threading import *
from System.Threading.Tasks import *
from System.Windows.Threading import *
from ICSharpCode.Decompiler import *
from ICSharpCode.TreeView import *

class ThreadingSupport(object):
	""" <summary>
	 Adds threading support to nodes
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Adds threading support to nodes
		 </summary>
		"""
		self._cancellationTokenSource = CancellationTokenSource()

	def get_IsRunning(self):
		return self._loadChildrenTask != None and not self._loadChildrenTask.IsCompleted

	IsRunning = property(fget=get_IsRunning)

	def Cancel(self):
		self._cancellationTokenSource.Cancel()
		self._loadChildrenTask = None
		self._cancellationTokenSource = CancellationTokenSource()

	def LoadChildren(self, node, fetchChildren):
		""" <summary>
		 Starts loading the children of the specified node.
		 </summary>
		"""
		node.Children.Add(LoadingTreeNode())
		ct = self._cancellationTokenSource.Token
		fetchChildrenEnumerable = self.fetchChildren(ct)
		thisTask = None
		thisTask = Task[List](, 		# don't access "child" here the
		# background thread might already be running the next loop iteration
ct)
		self._loadChildrenTask = thisTask
		thisTask.Start()
		thisTask.ContinueWith() # remove 'Loading...' # observe exception even when task isn't current
		# Give the task a bit time to complete before we return to WPF - this keeps "Loading..."
		# from showing up for very short waits.
		thisTask.Wait(TimeSpan.FromMilliseconds(200))

	def Decompile(self, language, output, options, ensureLazyChildren):
		loadChildrenTask = self._loadChildrenTask
		if self._loadChildrenTask == None:
			App.Current.Dispatcher.Invoke(DispatcherPriority.Normal, ensureLazyChildren)
			self._loadChildrenTask = self._loadChildrenTask
		if self._loadChildrenTask != None:
			enumerator = self._loadChildrenTask.Result.Cast().GetEnumerator()
			while enumerator.MoveNext():
				child = enumerator.Current
				child.Decompile(language, output, options)

	class LoadingTreeNode(ILSpyTreeNode):
		def get_Text(self):
			return "Loading..."

		Text = property(fget=get_Text)

		def Filter(self, settings):
			return FilterResult.Match

		def Decompile(self, language, output, options):
			pass

	class ErrorTreeNode(ILSpyTreeNode):
		def get_Text(self):
			return self._text

		Text = property(fget=get_Text)

		def __init__(self, text):
			self._text = text

		def Filter(self, settings):
			return FilterResult.Match

		def Decompile(self, language, output, options):
			pass