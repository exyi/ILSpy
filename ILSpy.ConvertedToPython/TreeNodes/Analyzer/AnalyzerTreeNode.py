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
from System.Collections.Specialized import *
from System.Linq import *
from ICSharpCode.TreeView import *

class AnalyzerTreeNode(SharpTreeNode):
	def __init__(self):

	def get_Language(self):
		return self._language

	def set_Language(self, value):
		if self._language != value:
			self._language = value
			enumerator = self._Children.OfType().GetEnumerator()
			while enumerator.MoveNext():
				child = enumerator.Current
				child.Language = value

	Language = property(fget=get_Language, fset=set_Language)

	def CanDelete(self):
		return Parent != None and Parent.IsRoot

	def DeleteCore(self):
		Parent.Children.Remove(self)

	def Delete(self):
		self.DeleteCore()

	def OnChildrenChanged(self, e):
		if e.NewItems != None:
			enumerator = e.NewItems.OfType().GetEnumerator()
			while enumerator.MoveNext():
				a = enumerator.Current
				a.Language = self.Language
		self.OnChildrenChanged(e)

	def HandleAssemblyListChanged(self, removedAssemblies, addedAssemblies):
		""" <summary>
		 Handles changes to the assembly list.
		 </summary>
		"""
		pass