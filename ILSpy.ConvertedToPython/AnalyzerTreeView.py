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
from System.Windows import *
from ICSharpCode.ILSpy.TreeNodes.Analyzer import *
from ICSharpCode.TreeView import *

class AnalyzerTreeView(SharpTreeView, IPane):
	""" <summary>
	 Analyzer tree view.
	 </summary>
	"""
	def get_Instance(self):
		if self._instance == None:
			App.Current.VerifyAccess()
			self._instance = AnalyzerTreeView()
		return self._instance

	Instance = property(fget=get_Instance)

	def __init__(self):
		self._ShowRoot = False
		self._Root = AnalyzerRootNode(Language = MainWindow.Instance.CurrentLanguage)
		self._BorderThickness = Thickness(0)
		ContextMenuProvider.Add(self)
		MainWindow.Instance.CurrentAssemblyListChanged += self.MainWindow_Instance_CurrentAssemblyListChanged

	def MainWindow_Instance_CurrentAssemblyListChanged(self, sender, e):
		if e.Action == NotifyCollectionChangedAction.Reset:
			self._Root.Children.Clear()
		else:
			removedAssemblies = List[LoadedAssembly]()
			if e.OldItems != None:
				removedAssemblies.AddRange(e.OldItems.Cast())
			addedAssemblies = List[LoadedAssembly]()
			if e.NewItems != None:
				addedAssemblies.AddRange(e.NewItems.Cast())
			(self._Root).HandleAssemblyListChanged(removedAssemblies, addedAssemblies)

	def Show(self):
		if not IsVisible:
			MainWindow.Instance.ShowInBottomPane("Analyzer", self)

	def Show(self, node):
		self.Show()
		node.IsExpanded = True
		self._Root.Children.Add(node)
		self._SelectedItem = node
		self.FocusNode(node)

	def ShowOrFocus(self, node):
		if :
			an = node
			found = self._Root.Children.OfType().FirstOrDefault()
			if found != None:
				self.Show()
				found.IsExpanded = True
				self._SelectedItem = found
				self.FocusNode(found)
				return 
		self.Show(node)

	def Closed(self):
		self._Root.Children.Clear()

	class AnalyzerRootNode(AnalyzerTreeNode):
		def HandleAssemblyListChanged(self, removedAssemblies, addedAssemblies):
			self._Children.RemoveAll()
			return True