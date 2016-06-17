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

class AnalyzedFieldTreeNode(AnalyzerEntityTreeNode):
	def __init__(self, analyzedField):
		if analyzedField == None:
			raise ArgumentNullException("analyzedField")
		self._analyzedField = analyzedField
		self._LazyLoading = True

	def get_Icon(self):
		return FieldTreeNode.GetIcon(analyzedField)

	Icon = property(fget=get_Icon)

	def get_Text(self):
		return Language.TypeToString(analyzedField.DeclaringType, True) + "." + analyzedField.Name + " : " + self._Language.TypeToString(analyzedField.FieldType, False, analyzedField)

	Text = property(fget=get_Text)

	def LoadChildren(self):
		self._Children.Add(AnalyzedFieldAccessTreeNode(self._analyzedField, False))
		if not self._analyzedField.IsLiteral:
			self._Children.Add(AnalyzedFieldAccessTreeNode(self._analyzedField, True))

	def get_Member(self):
		return self._analyzedField

	Member = property(fget=get_Member)