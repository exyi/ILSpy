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
from Mono.Cecil.Cil import *

class AnalyzedTypeUsedByTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedType):
		if analyzedType == None:
			raise ArgumentNullException("analyzedType")
		self._analyzedType = analyzedType

	def get_Text(self):
		return "Used By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedType, FindTypeUsage)
		return analyzer.PerformAnalysis(ct).Cast().Where().Distinct(AnalyzerEntityTreeNodeComparer()).OrderBy()

	def FindTypeUsage(self, type):
		if type == self._analyzedType:
		if self.IsUsedInTypeDefinition(type):
		enumerator = type.Fields.Where(IsUsedInFieldReference).GetEnumerator()
		while enumerator.MoveNext():
			field = enumerator.Current
		enumerator = type.Methods.Where(IsUsedInMethodDefinition).GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current

	def HandleSpecialMethodNode(self, method):
		property = method.DeclaringType.Properties.FirstOrDefault()
		if property != None:
			return AnalyzedPropertyTreeNode(propertyLanguage = Language)
		return AnalyzedMethodTreeNode(methodLanguage = Language)

	def IsUsedInTypeReferences(self, types):
		return types.Any(IsUsedInTypeReference)

	def IsUsedInTypeReference(self, type):
		if type == None:
			return False
		return self.TypeMatches(type.DeclaringType) or self.TypeMatches(type)

	def IsUsedInTypeDefinition(self, type):
		return self.IsUsedInTypeReference(type) or self.TypeMatches(type.BaseType) or self.IsUsedInTypeReferences(type.Interfaces)

	def IsUsedInFieldReference(self, field):
		if field == None:
			return False
		return self.TypeMatches(field.DeclaringType) or self.TypeMatches(field.FieldType)

	def IsUsedInMethodReference(self, method):
		if method == None:
			return False
		return self.TypeMatches(method.DeclaringType) or self.TypeMatches(method.ReturnType) or self.IsUsedInMethodParameters(method.Parameters)

	def IsUsedInMethodDefinition(self, method):
		return self.IsUsedInMethodReference(method) or self.IsUsedInMethodBody(method)

	def IsUsedInMethodBody(self, method):
		if method.Body == None:
			return False
		found = False
		enumerator = method.Body.Instructions.GetEnumerator()
		while enumerator.MoveNext():
			instruction = enumerator.Current
			tr = instruction.Operand
			if self.IsUsedInTypeReference(tr):
				found = True
				break
			fr = instruction.Operand
			if self.IsUsedInFieldReference(fr):
				found = True
				break
			mr = instruction.Operand
			if self.IsUsedInMethodReference(mr):
				found = True
				break
		method.Body = None # discard body to reduce memory pressure & higher GC gen collections
		return found

	def IsUsedInMethodParameters(self, parameters):
		return parameters.Any(IsUsedInMethodParameter)

	def IsUsedInMethodParameter(self, parameter):
		return self.TypeMatches(parameter.ParameterType)

	def TypeMatches(self, tref):
		if tref != None and tref.Name == self._analyzedType.Name:
			tdef = tref.Resolve()
			if tdef != None:
				return (tdef == self._analyzedType)
		return False

	def CanShow(type):
		return type != None

	CanShow = staticmethod(CanShow)

class AnalyzerEntityTreeNodeComparer(IEqualityComparer):
	def Equals(self, x, y):
		return x.Member == y.Member

	def GetHashCode(self, node):
		return node.Member.GetHashCode()