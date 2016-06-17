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
from Mono.Cecil import *

class AnalyzedTypeTreeNode(AnalyzerEntityTreeNode):
	def __init__(self, analyzedType):
		if analyzedType == None:
			raise ArgumentNullException("analyzedType")
		self._analyzedType = analyzedType
		self._LazyLoading = True

	def get_Icon(self):
		return TypeTreeNode.GetIcon(analyzedType)

	Icon = property(fget=get_Icon)

	def get_Text(self):
		return Language.TypeToString(analyzedType, True)

	Text = property(fget=get_Text)

	def LoadChildren(self):
		if AnalyzedAttributeAppliedToTreeNode.CanShow(self._analyzedType):
			self._Children.Add(AnalyzedAttributeAppliedToTreeNode(self._analyzedType))
		if AnalyzedTypeInstantiationsTreeNode.CanShow(self._analyzedType):
			self._Children.Add(AnalyzedTypeInstantiationsTreeNode(self._analyzedType))
		if AnalyzedTypeUsedByTreeNode.CanShow(self._analyzedType):
			self._Children.Add(AnalyzedTypeUsedByTreeNode(self._analyzedType))
		if AnalyzedTypeExposedByTreeNode.CanShow(self._analyzedType):
			self._Children.Add(AnalyzedTypeExposedByTreeNode(self._analyzedType))
		if AnalyzedTypeExtensionMethodsTreeNode.CanShow(self._analyzedType):
			self._Children.Add(AnalyzedTypeExtensionMethodsTreeNode(self._analyzedType))

	def get_Member(self):
		return self._analyzedType

	Member = property(fget=get_Member)