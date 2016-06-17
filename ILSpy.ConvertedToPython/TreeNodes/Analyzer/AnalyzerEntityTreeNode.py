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
from ICSharpCode.TreeView import *
from Mono.Cecil import *

class AnalyzerEntityTreeNode(AnalyzerTreeNode, IMemberTreeNode):
	""" <summary>
	 Base class for entity nodes.
	 </summary>
	"""
	def get_Member(self):

	Member = property(fget=get_Member)

	def ActivateItem(self, e):
		e.Handled = True
		MainWindow.Instance.JumpToReference(self.Member)
		r = self.GetParentReference()
		if r != None:
			MainWindow.Instance.DecompilationTask.Then()

	def GetParentReference(self):
		p = Parent
		result = None
		while (result == None or ):