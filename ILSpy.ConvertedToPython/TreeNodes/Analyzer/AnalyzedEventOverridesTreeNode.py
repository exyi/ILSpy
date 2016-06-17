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

class AnalyzedEventOverridesTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedEvent):
		if analyzedEvent == None:
			raise ArgumentNullException("analyzedEvent")
		self._analyzedEvent = analyzedEvent

	def get_Text(self):
		return "Overridden By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedEvent, FindReferencesInType)
		return analyzer.PerformAnalysis(ct).OrderBy()

	def FindReferencesInType(self, type):
		if not TypesHierarchyHelpers.IsBaseType(self._analyzedEvent.DeclaringType, type, resolveTypeArguments = False):
		enumerator = type.Events.GetEnumerator()
		while enumerator.MoveNext():
			eventDef = enumerator.Current
			if TypesHierarchyHelpers.IsBaseEvent(self._analyzedEvent, eventDef):
				anyAccessor = eventDef.AddMethod == eventDef.RemoveMethod
				hidesParent = not anyAccessor.IsVirtual ^ anyAccessor.IsNewSlot
				node = AnalyzedEventTreeNode(eventDef, "(hides) " if hidesParent else "")
				node.Language = self._Language

	def CanShow(property):
		accessor = property.AddMethod == property.RemoveMethod
		return accessor.IsVirtual and not accessor.IsFinal and not accessor.DeclaringType.IsInterface

	CanShow = staticmethod(CanShow)