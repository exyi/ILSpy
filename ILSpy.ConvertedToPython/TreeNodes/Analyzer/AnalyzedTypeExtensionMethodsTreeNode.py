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
from Mono.Cecil import *

class AnalyzedTypeExtensionMethodsTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedType):
		if analyzedType == None:
			raise ArgumentNullException("analyzedType")
		self._analyzedType = analyzedType

	def get_Text(self):
		return "Extension Methods"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedType, FindReferencesInType)
		return analyzer.PerformAnalysis(ct).OrderBy()

	def FindReferencesInType(self, type):
		if not self.HasExtensionAttribute(type):
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			if method.IsStatic and self.HasExtensionAttribute(method):
				if method.HasParameters and method.Parameters[0].ParameterType.Resolve() == self._analyzedType:
					node = AnalyzedMethodTreeNode(method)
					node.Language = self._Language

	def HasExtensionAttribute(self, p):
		if p.HasCustomAttributes:
			enumerator = p.CustomAttributes.GetEnumerator()
			while enumerator.MoveNext():
				ca = enumerator.Current
				t = ca.AttributeType
				if t.Name == "ExtensionAttribute" and t.Namespace == "System.Runtime.CompilerServices":
					return True
		return False

	def CanShow(type):
		# show on all types except static classes
		return not (type.IsAbstract and type.IsSealed)

	CanShow = staticmethod(CanShow)