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
from System.Linq import *
from System.Threading import *
from ICSharpCode.Decompiler.Ast import *
from Mono.Cecil import *

class AnalyzedPropertyOverridesTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedProperty):
		if analyzedProperty == None:
			raise ArgumentNullException("analyzedProperty")
		self._analyzedProperty = analyzedProperty

	def get_Text(self):
		return "Overridden By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedProperty, FindReferencesInType)
		return analyzer.PerformAnalysis(ct).OrderBy()

	def FindReferencesInType(self, type):
		if not TypesHierarchyHelpers.IsBaseType(self._analyzedProperty.DeclaringType, type, resolveTypeArguments = False):
		enumerator = type.Properties.GetEnumerator()
		while enumerator.MoveNext():
			property = enumerator.Current
			if TypesHierarchyHelpers.IsBaseProperty(self._analyzedProperty, property):
				anyAccessor = property.GetMethod == property.SetMethod
				hidesParent = not anyAccessor.IsVirtual ^ anyAccessor.IsNewSlot
				node = AnalyzedPropertyTreeNode(property, "(hides) " if hidesParent else "")
				node.Language = self._Language

	def CanShow(property):
		accessor = property.GetMethod == property.SetMethod
		return accessor.IsVirtual and not accessor.IsFinal and not accessor.DeclaringType.IsInterface

	CanShow = staticmethod(CanShow)