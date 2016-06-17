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
from System.Diagnostics import *
from Mono.Cecil import *
from ICSharpCode.TreeView import *
from ICSharpCode.ILSpy.TreeNodes.Analyzer import *

class SearchMsdnContextMenuEntry(IContextMenuEntry):
	def __init__(self):
		self._msdnAddress = "http://msdn.microsoft.com/en-us/library/{0}"

	def IsVisible(self, context):
		if context.SelectedTreeNodes == None:
			return False
		return context.SelectedTreeNodes.All()

	def IsEnabled(self, context):
		if context.SelectedTreeNodes == None:
			return False
		enumerator = context.SelectedTreeNodes.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			typeNode = node
			if typeNode != None and not typeNode.IsPublicAPI:
				return False
			eventNode = node
			if eventNode != None and (not eventNode.IsPublicAPI or not eventNode.EventDefinition.DeclaringType.IsPublic):
				return False
			fieldNode = node
			if fieldNode != None and (not fieldNode.IsPublicAPI or not fieldNode.FieldDefinition.DeclaringType.IsPublic):
				return False
			propertyNode = node
			if propertyNode != None and (not propertyNode.IsPublicAPI or not propertyNode.PropertyDefinition.DeclaringType.IsPublic):
				return False
			methodNode = node
			if methodNode != None and (not methodNode.IsPublicAPI or not methodNode.MethodDefinition.DeclaringType.IsPublic):
				return False
			namespaceNode = node
			if namespaceNode != None and str.IsNullOrEmpty(namespaceNode.Name):
				return False
		return True

	def Execute(self, context):
		if context.SelectedTreeNodes != None:
			enumerator = context.SelectedTreeNodes.GetEnumerator()
			while enumerator.MoveNext():
				node = enumerator.Current
				self.SearchMsdn(node)

	def SearchMsdn(node):
		address = str.Empty
		namespaceNode = node
		if namespaceNode != None:
			address = str.Format(self._msdnAddress, namespaceNode.Name)
		memberNode = node
		if memberNode != None:
			member = memberNode.Member
			memberName = str.Empty
			if member.DeclaringType == None:
				memberName = member.FullName
			else:
				memberName = str.Format("{0}.{1}", member.DeclaringType.FullName, member.Name)
			address = str.Format(self._msdnAddress, memberName)
		address = address.ToLower()
		if not str.IsNullOrEmpty(address):
			Process.Start(address)

	SearchMsdn = staticmethod(SearchMsdn)