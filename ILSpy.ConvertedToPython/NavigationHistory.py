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

class NavigationHistory(object):
	""" <summary>
	 Stores the navigation history.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Stores the navigation history.
		 </summary>
		"""
		self._NavigationSecondsBeforeNewEntry = 0.5
		self._lastNavigationTime = DateTime.MinValue
		self._back = List[T]()
		self._forward = List[T]()

	def get_CanNavigateBack(self):
		return self._back.Count > 0

	CanNavigateBack = property(fget=get_CanNavigateBack)

	def get_CanNavigateForward(self):
		return self._forward.Count > 0

	CanNavigateForward = property(fget=get_CanNavigateForward)

	def GoBack(self):
		self._forward.Add(self._current)
		self._current = self._back[self._back.Count - 1]
		self._back.RemoveAt(self._back.Count - 1)
		return self._current

	def GoForward(self):
		self._back.Add(self._current)
		self._current = self._forward[self._forward.Count - 1]
		self._forward.RemoveAt(self._forward.Count - 1)
		return self._current

	def RemoveAll(self, predicate):
		self._back.RemoveAll(predicate)
		self._forward.RemoveAll(predicate)

	def Clear(self):
		self._back.Clear()
		self._forward.Clear()

	def UpdateCurrent(self, node):
		self._current = node

	def Record(self, node):
		navigationTime = DateTime.Now
		period = navigationTime - self._lastNavigationTime
		if period.TotalSeconds < self._NavigationSecondsBeforeNewEntry:
			self._current = node
		else:
			if self._current != None:
				self._back.Add(self._current)
			# We only store a record once, and ensure it is on the top of the stack, so we just remove the old record
			self._back.Remove(node)
			self._current = node
		self._forward.Clear()
		self._lastNavigationTime = navigationTime