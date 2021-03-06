﻿# Copyright (c) 2011 AlphaSierraPapa for the SharpDevelop Team
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
from System.Linq import *
from System.Windows.Threading import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class ResourceListTreeNode(ILSpyTreeNode):
	""" <summary>
	 Lists the embedded resources in an assembly.
	 </summary>
	"""
	def __init__(self, module):
		self._LazyLoading = True
		self._module = module

	def get_Text(self):
		return "Resources"

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.FolderClosed

	Icon = property(fget=get_Icon)

	def get_ExpandedIcon(self):
		return Images.FolderOpen

	ExpandedIcon = property(fget=get_ExpandedIcon)

	def LoadChildren(self):
		enumerator = self._module.Resources.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			r = enumerator.Current
			self._Children.Add(ResourceTreeNode.Create(r))

	def Filter(self, settings):
		if str.IsNullOrEmpty(settings.SearchTerm):
			return FilterResult.MatchAndRecurse
		else:
			return FilterResult.Recurse

	def Decompile(self, language, output, options):
		App.Current.Dispatcher.Invoke(DispatcherPriority.Normal, Action(EnsureLazyChildren))
		enumerator = self._Children.GetEnumerator()
		while enumerator.MoveNext():
			child = enumerator.Current
			child.Decompile(language, output, options)
			output.WriteLine()