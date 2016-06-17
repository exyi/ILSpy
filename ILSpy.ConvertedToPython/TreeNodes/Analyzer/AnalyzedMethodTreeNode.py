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
from Mono.Cecil import *

class AnalyzedMethodTreeNode(AnalyzerEntityTreeNode):
	def __init__(self, analyzedMethod, prefix):
		if analyzedMethod == None:
			raise ArgumentNullException("analyzedMethod")
		self._analyzedMethod = analyzedMethod
		self._prefix = prefix
		self._LazyLoading = True

	def get_Icon(self):
		return MethodTreeNode.GetIcon(analyzedMethod)

	Icon = property(fget=get_Icon)

	def get_Text(self):
		return prefix + Language.TypeToString(analyzedMethod.DeclaringType, True) + "." + MethodTreeNode.GetText(analyzedMethod, Language)

	Text = property(fget=get_Text)

	def LoadChildren(self):
		if self._analyzedMethod.HasBody:
			self._Children.Add(AnalyzedMethodUsesTreeNode(self._analyzedMethod))
		if self._analyzedMethod.IsVirtual and not (self._analyzedMethod.IsNewSlot and self._analyzedMethod.IsFinal):
			self._Children.Add(AnalyzedVirtualMethodUsedByTreeNode(self._analyzedMethod))
		else:
			self._Children.Add(AnalyzedMethodUsedByTreeNode(self._analyzedMethod))
		if AnalyzedMethodOverridesTreeNode.CanShow(self._analyzedMethod):
			self._Children.Add(AnalyzedMethodOverridesTreeNode(self._analyzedMethod))
		if AnalyzedInterfaceMethodImplementedByTreeNode.CanShow(self._analyzedMethod):
			self._Children.Add(AnalyzedInterfaceMethodImplementedByTreeNode(self._analyzedMethod))

	def get_Member(self):
		return self._analyzedMethod

	Member = property(fget=get_Member)