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
from ICSharpCode.NRefactory.Utils import *
from Mono.Cecil import *

class ScopedWhereUsedAnalyzer(object):
	""" <summary>
	 Determines the accessibility domain of a member for where-used analysis.
	 </summary>
	"""
	def __init__(self, field, typeAnalysisFunction):
		self._memberAccessibility = Accessibility.Public
		self._typeAccessibility = Accessibility.Public
		# we only have to check the accessibility of the the get method
		# [CLS Rule 30: The accessibility of an event and of its accessors shall be identical.]
		if field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Private or field.Attributes & FieldAttributes.FieldAccessMask == :
			self._memberAccessibility = Accessibility.Private
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamANDAssem:
			self._memberAccessibility = Accessibility.FamilyAndInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Assembly:
			self._memberAccessibility = Accessibility.Internal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Family:
			self._memberAccessibility = Accessibility.Family
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamORAssem:
			self._memberAccessibility = Accessibility.FamilyOrInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Public:
			self._memberAccessibility = Accessibility.Public

	def __init__(self, field, typeAnalysisFunction):
		self._memberAccessibility = Accessibility.Public
		self._typeAccessibility = Accessibility.Public
		if field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Private or field.Attributes & FieldAttributes.FieldAccessMask == :
			self._memberAccessibility = Accessibility.Private
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamANDAssem:
			self._memberAccessibility = Accessibility.FamilyAndInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Assembly:
			self._memberAccessibility = Accessibility.Internal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Family:
			self._memberAccessibility = Accessibility.Family
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamORAssem:
			self._memberAccessibility = Accessibility.FamilyOrInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Public:
			self._memberAccessibility = Accessibility.Public

	def __init__(self, field, typeAnalysisFunction):
		self._memberAccessibility = Accessibility.Public
		self._typeAccessibility = Accessibility.Public
		if field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Private or field.Attributes & FieldAttributes.FieldAccessMask == :
			self._memberAccessibility = Accessibility.Private
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamANDAssem:
			self._memberAccessibility = Accessibility.FamilyAndInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Assembly:
			self._memberAccessibility = Accessibility.Internal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Family:
			self._memberAccessibility = Accessibility.Family
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamORAssem:
			self._memberAccessibility = Accessibility.FamilyOrInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Public:
			self._memberAccessibility = Accessibility.Public

	def __init__(self, field, typeAnalysisFunction):
		self._memberAccessibility = Accessibility.Public
		self._typeAccessibility = Accessibility.Public
		if field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Private or field.Attributes & FieldAttributes.FieldAccessMask == :
			self._memberAccessibility = Accessibility.Private
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamANDAssem:
			self._memberAccessibility = Accessibility.FamilyAndInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Assembly:
			self._memberAccessibility = Accessibility.Internal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Family:
			self._memberAccessibility = Accessibility.Family
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamORAssem:
			self._memberAccessibility = Accessibility.FamilyOrInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Public:
			self._memberAccessibility = Accessibility.Public

	def __init__(self, field, typeAnalysisFunction):
		self._memberAccessibility = Accessibility.Public
		self._typeAccessibility = Accessibility.Public
		if field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Private or field.Attributes & FieldAttributes.FieldAccessMask == :
			self._memberAccessibility = Accessibility.Private
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamANDAssem:
			self._memberAccessibility = Accessibility.FamilyAndInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Assembly:
			self._memberAccessibility = Accessibility.Internal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Family:
			self._memberAccessibility = Accessibility.Family
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamORAssem:
			self._memberAccessibility = Accessibility.FamilyOrInternal
		elif field.Attributes & FieldAttributes.FieldAccessMask == FieldAttributes.Public:
			self._memberAccessibility = Accessibility.Public

	def GetMethodAccessibility(self, method):
		if method.Attributes & MethodAttributes.MemberAccessMask == MethodAttributes.Private or method.Attributes & MethodAttributes.MemberAccessMask == :
			accessibility = Accessibility.Private
		elif method.Attributes & MethodAttributes.MemberAccessMask == MethodAttributes.FamANDAssem:
			accessibility = Accessibility.FamilyAndInternal
		elif method.Attributes & MethodAttributes.MemberAccessMask == MethodAttributes.Family:
			accessibility = Accessibility.Family
		elif method.Attributes & MethodAttributes.MemberAccessMask == MethodAttributes.Assembly:
			accessibility = Accessibility.Internal
		elif method.Attributes & MethodAttributes.MemberAccessMask == MethodAttributes.FamORAssem:
			accessibility = Accessibility.FamilyOrInternal
		elif method.Attributes & MethodAttributes.MemberAccessMask == MethodAttributes.Public:
			accessibility = Accessibility.Public
		return accessibility

	def PerformAnalysis(self, ct):
		if self._memberAccessibility == Accessibility.Private:
			return self.FindReferencesInTypeScope(ct)
		self.DetermineTypeAccessibility()
		if self._typeAccessibility == Accessibility.Private:
			return self.FindReferencesInEnclosingTypeScope(ct)
		if self._memberAccessibility == Accessibility.Internal or self._memberAccessibility == Accessibility.FamilyAndInternal or self._typeAccessibility == Accessibility.Internal or self._typeAccessibility == Accessibility.FamilyAndInternal:
			return self.FindReferencesInAssemblyAndFriends(ct)
		return self.FindReferencesGlobal(ct)

	def DetermineTypeAccessibility(self):
		while self._typeScope.IsNested:
			accessibility = self.GetNestedTypeAccessibility(self._typeScope)
			if self._typeAccessibility > accessibility:
				self._typeAccessibility = accessibility
				if self._typeAccessibility == Accessibility.Private:
					return 
			self._typeScope = self._typeScope.DeclaringType
		if self._typeScope.IsNotPublic and (self._typeAccessibility > Accessibility.Internal):
			self._typeAccessibility = Accessibility.Internal

	def GetNestedTypeAccessibility(type):
		if type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedPublic:
			result = Accessibility.Public
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedPrivate:
			result = Accessibility.Private
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamily:
			result = Accessibility.Family
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedAssembly:
			result = Accessibility.Internal
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamANDAssem:
			result = Accessibility.FamilyAndInternal
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamORAssem:
			result = Accessibility.FamilyOrInternal
		else:
			raise InvalidOperationException()
		return result

	GetNestedTypeAccessibility = staticmethod(GetNestedTypeAccessibility)

	class Accessibility(object):
		""" <summary>
		 The effective accessibility of a member
		 </summary>
		"""
		def __init__(self):
			""" <summary>
			 The effective accessibility of a member
			 </summary>
			"""

	def FindReferencesInAssemblyAndFriends(self, ct):
		assemblies = self.GetAssemblyAndAnyFriends(assemblyScope, ct)
		# use parallelism only on the assembly level (avoid locks within Cecil)
		return assemblies.AsParallel().WithCancellation(ct).SelectMany()

	def FindReferencesGlobal(self, ct):
		assemblies = self.GetReferencingAssemblies(assemblyScope, ct)
		# use parallelism only on the assembly level (avoid locks within Cecil)
		return assemblies.AsParallel().WithCancellation(ct).SelectMany()

	def FindReferencesInAssembly(self, asm, ct):
		enumerator = TreeTraversal.PreOrder(asm.MainModule.Types, ).GetEnumerator()
		while enumerator.MoveNext():
			type = enumerator.Current
			ct.ThrowIfCancellationRequested()
			enumerator = self.typeAnalysisFunction(type).GetEnumerator()
			while enumerator.MoveNext():
				result = enumerator.Current
				ct.ThrowIfCancellationRequested()

	def FindReferencesInTypeScope(self, ct):
		enumerator = TreeTraversal.PreOrder(typeScope, ).GetEnumerator()
		while enumerator.MoveNext():
			type = enumerator.Current
			ct.ThrowIfCancellationRequested()
			enumerator = self.typeAnalysisFunction(type).GetEnumerator()
			while enumerator.MoveNext():
				result = enumerator.Current
				ct.ThrowIfCancellationRequested()

	def FindReferencesInEnclosingTypeScope(self, ct):
		enumerator = TreeTraversal.PreOrder(typeScope.DeclaringType, ).GetEnumerator()
		while enumerator.MoveNext():
			type = enumerator.Current
			ct.ThrowIfCancellationRequested()
			enumerator = self.typeAnalysisFunction(type).GetEnumerator()
			while enumerator.MoveNext():
				result = enumerator.Current
				ct.ThrowIfCancellationRequested()

	def GetReferencingAssemblies(self, asm, ct):
		requiredAssemblyFullName = asm.FullName
		assemblies = MainWindow.Instance.CurrentAssemblyList.GetAssemblies().Where()
		enumerator = assemblies.GetEnumerator()
		while enumerator.MoveNext():
			assembly = enumerator.Current
			ct.ThrowIfCancellationRequested()
			found = False
			enumerator = assembly.AssemblyDefinition.MainModule.AssemblyReferences.GetEnumerator()
			while enumerator.MoveNext():
				reference = enumerator.Current
				if requiredAssemblyFullName == reference.FullName:
					found = True
					break
			if found and self.AssemblyReferencesScopeType(assembly.AssemblyDefinition):

	def GetAssemblyAndAnyFriends(self, asm, ct):
		if asm.HasCustomAttributes:
			attributes = asm.CustomAttributes.Where()
			friendAssemblies = HashSet[str]()
			enumerator = attributes.GetEnumerator()
			while enumerator.MoveNext():
				attribute = enumerator.Current
				assemblyName = attribute.ConstructorArguments[0].Value
				assemblyName = assemblyName.Split(',')[0] # strip off any public key info
				friendAssemblies.Add(assemblyName)
			if friendAssemblies.Count > 0:
				assemblies = MainWindow.Instance.CurrentAssemblyList.GetAssemblies()
				enumerator = assemblies.GetEnumerator()
				while enumerator.MoveNext():
					assembly = enumerator.Current
					ct.ThrowIfCancellationRequested()
					if friendAssemblies.Contains(assembly.ShortName) and self.AssemblyReferencesScopeType(assembly.AssemblyDefinition):

	def AssemblyReferencesScopeType(self, asm):
		hasRef = False
		enumerator = asm.MainModule.GetTypeReferences().GetEnumerator()
		while enumerator.MoveNext():
			typeref = enumerator.Current
			if typeref.Name == typeScope.Name and typeref.Namespace == typeScope.Namespace:
				hasRef = True
				break
		return hasRef