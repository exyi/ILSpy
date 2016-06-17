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
from ICSharpCode.ILSpy.TextView import *
from ICSharpCode.TreeView import *

class NavigationState(IEquatable):
	def get_TreeNodes(self):
		return self._treeNodes

	TreeNodes = property(fget=get_TreeNodes)

	def get_ViewState(self):

	def set_ViewState(self, value):

	ViewState = property(fget=get_ViewState, fset=set_ViewState)

	def __init__(self, treeNodes):
		self._treeNodes = HashSet[SharpTreeNode](treeNodes)

	def __init__(self, treeNodes):
		self._treeNodes = HashSet[SharpTreeNode](treeNodes)

	def Equals(self, other):
		# TODO: should this care about the view state as well?
		return self._treeNodes.SetEquals(other.treeNodes)