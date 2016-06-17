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

class AnalyzedTypeExposedByTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedType):
		if analyzedType == None:
			raise ArgumentNullException("analyzedType")
		self._analyzedType = analyzedType

	def get_Text(self):
		return "Exposed By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedType, FindReferencesInType)
		return analyzer.PerformAnalysis(ct).OrderBy()

	def FindReferencesInType(self, type):
		if self._analyzedType.IsEnum and type == self._analyzedType:
		if not self._Language.ShowMember(type):
		enumerator = type.Fields.GetEnumerator()
		while enumerator.MoveNext():
			field = enumerator.Current
			if self.TypeIsExposedBy(field):
				node = AnalyzedFieldTreeNode(field)
				node.Language = self._Language
		enumerator = type.Properties.GetEnumerator()
		while enumerator.MoveNext():
			property = enumerator.Current
			if self.TypeIsExposedBy(property):
				node = AnalyzedPropertyTreeNode(property)
				node.Language = self._Language
		enumerator = type.Events.GetEnumerator()
		while enumerator.MoveNext():
			eventDef = enumerator.Current
			if self.TypeIsExposedBy(eventDef):
				node = AnalyzedEventTreeNode(eventDef)
				node.Language = self._Language
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			if self.TypeIsExposedBy(method):
				node = AnalyzedMethodTreeNode(method)
				node.Language = self._Language

	def TypeIsExposedBy(self, field):
		if field.IsPrivate:
			return False
		if field.FieldType.Resolve() == self._analyzedType:
			return True
		return False

	def TypeIsExposedBy(self, property):
		if self.IsPrivate(property):
			return False
		if property.PropertyType.Resolve() == self._analyzedType:
			return True
		return False

	def TypeIsExposedBy(self, eventDef):
		if self.IsPrivate(eventDef):
			return False
		if eventDef.EventType.Resolve() == self._analyzedType:
			return True
		return False

	def TypeIsExposedBy(self, method):
		# if the method has overrides, it is probably an explicit interface member
		# and should be considered part of the public API even though it is marked private.
		if method.IsPrivate:
			if not method.HasOverrides:
				return False
			typeDefinition = method.Overrides[0].DeclaringType.Resolve()
			if typeDefinition != None and not typeDefinition.IsInterface:
				return False
		# exclude methods with 'semantics'. for example, property getters & setters.
		# HACK: this is a potentially fragile implementation, as the MethodSemantics may be extended to other uses at a later date.
		if method.SemanticsAttributes != MethodSemanticsAttributes.None:
			return False
		if method.ReturnType.Resolve() == self._analyzedType:
			return True
		if method.HasParameters:
			enumerator = method.Parameters.GetEnumerator()
			while enumerator.MoveNext():
				parameter = enumerator.Current
				if parameter.ParameterType.Resolve() == self._analyzedType:
					return True
		return False

	def IsPrivate(property):
		isGetterPublic = (property.GetMethod != None and not property.GetMethod.IsPrivate)
		isSetterPublic = (property.SetMethod != None and not property.SetMethod.IsPrivate)
		return not (isGetterPublic or isSetterPublic)

	IsPrivate = staticmethod(IsPrivate)

	def IsPrivate(eventDef):
		isAdderPublic = (eventDef.AddMethod != None and not eventDef.AddMethod.IsPrivate)
		isRemoverPublic = (eventDef.RemoveMethod != None and not eventDef.RemoveMethod.IsPrivate)
		return not (isAdderPublic or isRemoverPublic)

	IsPrivate = staticmethod(IsPrivate)

	def CanShow(type):
		return True

	CanShow = staticmethod(CanShow)