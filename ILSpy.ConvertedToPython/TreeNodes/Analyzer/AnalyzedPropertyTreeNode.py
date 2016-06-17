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
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class AnalyzedPropertyTreeNode(AnalyzerEntityTreeNode):
	def __init__(self, analyzedProperty, prefix):
		if analyzedProperty == None:
			raise ArgumentNullException("analyzedProperty")
		self._isIndexer = analyzedProperty.IsIndexer()
		self._analyzedProperty = analyzedProperty
		self._prefix = prefix
		self._LazyLoading = True

	def get_Icon(self):
		return PropertyTreeNode.GetIcon(analyzedProperty, self._isIndexer)

	Icon = property(fget=get_Icon)

	def get_Text(self):
		# TODO: This way of formatting is not suitable for properties which explicitly implement interfaces.
		return prefix + Language.TypeToString(analyzedProperty.DeclaringType, True) + "." + PropertyTreeNode.GetText(analyzedProperty, Language, self._isIndexer)

	Text = property(fget=get_Text)

	def LoadChildren(self):
		if self._analyzedProperty.GetMethod != None:
			self._Children.Add(AnalyzedPropertyAccessorTreeNode(self._analyzedProperty.GetMethod, "get"))
		if self._analyzedProperty.SetMethod != None:
			self._Children.Add(AnalyzedPropertyAccessorTreeNode(self._analyzedProperty.SetMethod, "set"))
		enumerator = self._analyzedProperty.OtherMethods.GetEnumerator()
		while enumerator.MoveNext():
			accessor = enumerator.Current
			self._Children.Add(AnalyzedPropertyAccessorTreeNode(accessor, None))
		if AnalyzedPropertyOverridesTreeNode.CanShow(self._analyzedProperty):
			self._Children.Add(AnalyzedPropertyOverridesTreeNode(self._analyzedProperty))
		if AnalyzedInterfacePropertyImplementedByTreeNode.CanShow(self._analyzedProperty):
			self._Children.Add(AnalyzedInterfacePropertyImplementedByTreeNode(self._analyzedProperty))

	def TryCreateAnalyzer(member):
		if AnalyzedPropertyTreeNode.CanShow(member):
			return AnalyzedPropertyTreeNode(member)
		else:
			return None

	TryCreateAnalyzer = staticmethod(TryCreateAnalyzer)

	def CanShow(member):
		property = member
		if property == None:
			return False
		return not MainWindow.Instance.CurrentLanguage.ShowMember(property.GetMethod == property.SetMethod) or AnalyzedPropertyOverridesTreeNode.CanShow(property)

	CanShow = staticmethod(CanShow)

	def get_Member(self):
		return self._analyzedProperty

	Member = property(fget=get_Member)