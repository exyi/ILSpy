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
from System.Linq import *
from ICSharpCode.Decompiler import *

class NamespaceTreeNode(ILSpyTreeNode):
	""" <summary>
	 Namespace node. The loading of the type nodes is handled by the parent AssemblyTreeNode.
	 </summary>
	"""
	def get_Name(self):
		return self._name

	Name = property(fget=get_Name)

	def __init__(self, name):
		if name == None:
			raise ArgumentNullException("name")
		self._name = name

	def get_Text(self):
		return self.HighlightSearchMatch("-" if name.Length == 0 else name)

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.Namespace

	Icon = property(fget=get_Icon)

	def Filter(self, settings):
		if settings.SearchTermMatches(self._name):
			return FilterResult.MatchAndRecurse
		else:
			return FilterResult.Recurse

	def Decompile(self, language, output, options):
		language.DecompileNamespace(self._name, self._Children.OfType().Select(), output, options)