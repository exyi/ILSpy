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
from Mono.Cecil.Cil import *

class AnalyzedTypeInstantiationsTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedType):
		if analyzedType == None:
			raise ArgumentNullException("analyzedType")
		self._analyzedType = analyzedType
		self._isSystemObject = (analyzedType.FullName == "System.Object")

	def get_Text(self):
		return "Instantiated By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedType, FindReferencesInType)
		return analyzer.PerformAnalysis(ct).OrderBy()

	def FindReferencesInType(self, type):
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			found = False
			if not method.HasBody:
				continue
			# ignore chained constructors
			# (since object is the root of everything, we can short circuit the test in this case)
			if method.Name == ".ctor" and (self._isSystemObject or self._analyzedType == type or TypesHierarchyHelpers.IsBaseType(self._analyzedType, type, False)):
				continue
			enumerator = method.Body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				instr = enumerator.Current
				mr = instr.Operand
				if mr != None and mr.Name == ".ctor":
					if Helpers.IsReferencedBy(self._analyzedType, mr.DeclaringType):
						found = True
						break
			method.Body = None
			if found:
				node = AnalyzedMethodTreeNode(method)
				node.Language = self._Language

	def CanShow(type):
		return (type.IsClass and not (type.IsAbstract and type.IsSealed) and not type.IsEnum)

	CanShow = staticmethod(CanShow)