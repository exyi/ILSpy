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
from System.Windows.Threading import *
from ICSharpCode.Decompiler import *
from ICSharpCode.TreeView import *
from Mono.Cecil import *

class BaseTypesTreeNode(ILSpyTreeNode):
	""" <summary>
	 Lists the base types of a class.
	 </summary>
	"""
	def __init__(self, type):
		self._type = type
		self._LazyLoading = True

	def get_Text(self):
		return "Base Types"

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.SuperTypes

	Icon = property(fget=get_Icon)

	def LoadChildren(self):
		self.AddBaseTypes(self._Children, self._type)

	def AddBaseTypes(children, type):
		if type.BaseType != None:
			children.Add(BaseTypesEntryNode(type.BaseType, False))
		enumerator = type.Interfaces.GetEnumerator()
		while enumerator.MoveNext():
			i = enumerator.Current
			children.Add(BaseTypesEntryNode(i, True))

	AddBaseTypes = staticmethod(AddBaseTypes)

	def Decompile(self, language, output, options):
		App.Current.Dispatcher.Invoke(DispatcherPriority.Normal, Action(EnsureLazyChildren))
		enumerator = self._Children.GetEnumerator()
		while enumerator.MoveNext():
			child = enumerator.Current
			child.Decompile(language, output, options)