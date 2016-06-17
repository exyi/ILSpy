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

class AnalyzedInterfacePropertyImplementedByTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedProperty):
		if analyzedProperty == None:
			raise ArgumentNullException("analyzedProperty")
		self._analyzedProperty = analyzedProperty
		self._analyzedMethod = self._analyzedProperty.GetMethod == self._analyzedProperty.SetMethod

	def get_Text(self):
		return "Implemented By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedMethod, FindReferencesInType)
		return analyzer.PerformAnalysis(ct).OrderBy()

	def FindReferencesInType(self, type):
		if not type.HasInterfaces:
		implementedInterfaceRef = type.Interfaces.FirstOrDefault()
		if implementedInterfaceRef == None:
		enumerator = type.Properties.Where().GetEnumerator()
		while enumerator.MoveNext():
			property = enumerator.Current
			accessor = property.GetMethod == property.SetMethod
			if TypesHierarchyHelpers.MatchInterfaceMethod(accessor, self._analyzedMethod, implementedInterfaceRef):
				node = AnalyzedPropertyTreeNode(property)
				node.Language = self._Language
		enumerator = type.Properties.Where().GetEnumerator()
		while enumerator.MoveNext():
			property = enumerator.Current
			accessor = property.GetMethod == property.SetMethod
			if accessor.HasOverrides and accessor.Overrides.Any():
				node = AnalyzedPropertyTreeNode(property)
				node.Language = self._Language

	def CanShow(property):
		return property.DeclaringType.IsInterface

	CanShow = staticmethod(CanShow)