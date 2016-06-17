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
from System.Windows import *
from ICSharpCode.TreeView import *
from Mono.Cecil import *

class AnalyzeContextMenuEntry(IContextMenuEntry):
	def IsVisible(self, context):
		if  and context.SelectedTreeNodes != None and context.SelectedTreeNodes.All():
			return False
		if context.SelectedTreeNodes == None:
			return context.Reference != None and 
		return context.SelectedTreeNodes.All()

	def IsEnabled(self, context):
		if context.SelectedTreeNodes == None:
			return context.Reference != None and 
		enumerator = context.SelectedTreeNodes.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			if not ( or  or  or AnalyzedPropertyTreeNode.CanShow(node.Member) or AnalyzedEventTreeNode.CanShow(node.Member)):
				return False
		return True

	def Execute(self, context):
		if context.SelectedTreeNodes != None:
			enumerator = context.SelectedTreeNodes.GetEnumerator()
			while enumerator.MoveNext():
				node = enumerator.Current
				self.Analyze(node.Member)
		elif context.Reference != None and :
			if :
				self.Analyze(context.Reference.Reference)

	# TODO: implement support for other references: ParameterReference, etc.
	def Analyze(member):
		if :
			type = (member).Resolve()
			if type != None:
				AnalyzerTreeView.Instance.ShowOrFocus(AnalyzedTypeTreeNode(type))
		elif :
			field = (member).Resolve()
			if field != None:
				AnalyzerTreeView.Instance.ShowOrFocus(AnalyzedFieldTreeNode(field))
		elif :
			method = (member).Resolve()
			if method != None:
				AnalyzerTreeView.Instance.ShowOrFocus(AnalyzedMethodTreeNode(method))
		elif :
			property = (member).Resolve()
			if property != None:
				AnalyzerTreeView.Instance.ShowOrFocus(AnalyzedPropertyTreeNode(property))
		elif :
			event = (member).Resolve()
			if event != None:
				AnalyzerTreeView.Instance.ShowOrFocus(AnalyzedEventTreeNode(event))

	Analyze = staticmethod(Analyze)