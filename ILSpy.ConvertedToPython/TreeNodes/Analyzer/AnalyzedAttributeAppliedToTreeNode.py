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
from ICSharpCode.NRefactory.Utils import *
from System.Collections.Concurrent import *

class AnalyzedAttributeAppliedToTreeNode(AnalyzerSearchTreeNode):
	def CanShow(type):
		return type.IsClass and type.IsCustomAttribute()

	CanShow = staticmethod(CanShow)

	def __init__(self, analyzedType):
		self._usage = AttributeTargets.All
		self._inherited = True
		if analyzedType == None:
			raise ArgumentNullException("analyzedType")
		self._analyzedType = analyzedType
		self._attributeName = self._analyzedType.FullName
		self.GetAttributeUsage()

	def GetAttributeUsage(self):
		if self._analyzedType.HasCustomAttributes:
			enumerator = self._analyzedType.CustomAttributes.GetEnumerator()
			while enumerator.MoveNext():
				ca = enumerator.Current
				t = ca.AttributeType
				if t.Name == "AttributeUsageAttribute" and t.Namespace == "System":
					self._usage = ca.ConstructorArguments[0].Value
					if ca.ConstructorArguments.Count > 1:
						self._allowMutiple = ca.ConstructorArguments[1].Value
						self._inherited = ca.ConstructorArguments[2].Value
					if ca.HasProperties:
						enumerator = ca.Properties.GetEnumerator()
						while enumerator.MoveNext():
							namedArgument = enumerator.Current
							if namedArgument.Name == "AllowMultiple":
								self._allowMutiple = namedArgument.Argument.Value
							elif namedArgument.Name == "Inherited":
								self._inherited = namedArgument.Argument.Value

	def get_Text(self):
		return "Applied To"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		self._foundMethods = ConcurrentDictionary[MethodDefinition, int]()
		#get the assemblies to search
		currentAssembly = self._analyzedType.Module.Assembly
		assemblies = self.GetReferencingAssemblies(currentAssembly, ct) if self._analyzedType.IsPublic else self.GetAssemblyAndAnyFriends(currentAssembly, ct)
		results = assemblies.AsParallel().WithCancellation(ct).SelectMany()
		enumerator = results.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			result = enumerator.Current
		self._foundMethods = None

	def FindReferencesInAssembly(self, module, tr, ct):
		#since we do not display modules as separate entities, coalesce the assembly and module searches
		foundInAssyOrModule = False
		if (self._usage & AttributeTargets.Assembly) != 0:
			asm = module.Assembly
			if asm != None and asm.HasCustomAttributes:
				enumerator = asm.CustomAttributes.GetEnumerator()
				while enumerator.MoveNext():
					attribute = enumerator.Current
					if attribute.AttributeType == tr:
						foundInAssyOrModule = True
						break
		if not foundInAssyOrModule:
			ct.ThrowIfCancellationRequested()
			#search module
			if (self._usage & AttributeTargets.Module) != 0:
				if module.HasCustomAttributes:
					enumerator = module.CustomAttributes.GetEnumerator()
					while enumerator.MoveNext():
						attribute = enumerator.Current
						if attribute.AttributeType == tr:
							foundInAssyOrModule = True
							break
		if foundInAssyOrModule:
		ct.ThrowIfCancellationRequested()
		enumerator = TreeTraversal.PreOrder(module.Types, ).OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			type = enumerator.Current
			ct.ThrowIfCancellationRequested()
			enumerator = self.FindReferencesWithinInType(type, tr).GetEnumerator()
			while enumerator.MoveNext():
				result = enumerator.Current
				ct.ThrowIfCancellationRequested()

	def FindReferencesWithinInType(self, type, attrTypeRef):
		searchRequired = (type.IsClass and self._usage.HasFlag(AttributeTargets.Class)) or (type.IsEnum and self._usage.HasFlag(AttributeTargets.Enum)) or (type.IsInterface and self._usage.HasFlag(AttributeTargets.Interface)) or (type.IsValueType and self._usage.HasFlag(AttributeTargets.Struct))
		if searchRequired:
			if type.HasCustomAttributes:
				enumerator = type.CustomAttributes.GetEnumerator()
				while enumerator.MoveNext():
					attribute = enumerator.Current
					if attribute.AttributeType == attrTypeRef:
						node = AnalyzedTypeTreeNode(type)
						node.Language = self._Language
						break
		if (self._usage & AttributeTargets.GenericParameter) != 0 and type.HasGenericParameters:
			enumerator = type.GenericParameters.GetEnumerator()
			while enumerator.MoveNext():
				parameter = enumerator.Current
				if parameter.HasCustomAttributes:
					enumerator = parameter.CustomAttributes.GetEnumerator()
					while enumerator.MoveNext():
						attribute = enumerator.Current
						if attribute.AttributeType == attrTypeRef:
							node = AnalyzedTypeTreeNode(type)
							node.Language = self._Language
							break
		if (self._usage & AttributeTargets.Field) != 0 and type.HasFields:
			enumerator = type.Fields.GetEnumerator()
			while enumerator.MoveNext():
				field = enumerator.Current
				if field.HasCustomAttributes:
					enumerator = field.CustomAttributes.GetEnumerator()
					while enumerator.MoveNext():
						attribute = enumerator.Current
						if attribute.AttributeType == attrTypeRef:
							node = AnalyzedFieldTreeNode(field)
							node.Language = self._Language
							break
		if ((self._usage & AttributeTargets.Property) != 0) and type.HasProperties:
			enumerator = type.Properties.GetEnumerator()
			while enumerator.MoveNext():
				property = enumerator.Current
				if property.HasCustomAttributes:
					enumerator = property.CustomAttributes.GetEnumerator()
					while enumerator.MoveNext():
						attribute = enumerator.Current
						if attribute.AttributeType == attrTypeRef:
							node = AnalyzedPropertyTreeNode(property)
							node.Language = self._Language
							break
		if ((self._usage & AttributeTargets.Event) != 0) and type.HasEvents:
			enumerator = type.Events.GetEnumerator()
			while enumerator.MoveNext():
				_event = enumerator.Current
				if _event.HasCustomAttributes:
					enumerator = _event.CustomAttributes.GetEnumerator()
					while enumerator.MoveNext():
						attribute = enumerator.Current
						if attribute.AttributeType == attrTypeRef:
							node = AnalyzedEventTreeNode(_event)
							node.Language = self._Language
							break
		if type.HasMethods:
			enumerator = type.Methods.GetEnumerator()
			while enumerator.MoveNext():
				method = enumerator.Current
				found = False
				if (self._usage & (AttributeTargets.Method | AttributeTargets.Constructor)) != 0:
					if method.HasCustomAttributes:
						enumerator = method.CustomAttributes.GetEnumerator()
						while enumerator.MoveNext():
							attribute = enumerator.Current
							if attribute.AttributeType == attrTypeRef:
								found = True
								break
				if not found and ((self._usage & AttributeTargets.ReturnValue) != 0) and method.MethodReturnType.HasCustomAttributes:
					enumerator = method.MethodReturnType.CustomAttributes.GetEnumerator()
					while enumerator.MoveNext():
						attribute = enumerator.Current
						if attribute.AttributeType == attrTypeRef:
							found = True
							break
				if not found and ((self._usage & AttributeTargets.Parameter) != 0) and method.HasParameters:
					enumerator = method.Parameters.GetEnumerator()
					while enumerator.MoveNext():
						parameter = enumerator.Current
						enumerator = parameter.CustomAttributes.GetEnumerator()
						while enumerator.MoveNext():
							attribute = enumerator.Current
							if attribute.AttributeType == attrTypeRef:
								found = True
								break
				if found:
					codeLocation = self._Language.GetOriginalCodeLocation(method)
					if codeLocation != None and not self.HasAlreadyBeenFound(codeLocation):
						node = AnalyzedMethodTreeNode(codeLocation)
						node.Language = self._Language

	def HasAlreadyBeenFound(self, method):
		return not self._foundMethods.TryAdd(method, 0)

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
			if found:
				typeref = self.GetScopeTypeReferenceInAssembly(assembly.AssemblyDefinition)
				if typeref != None:

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
					if friendAssemblies.Contains(assembly.ShortName):
						typeref = self.GetScopeTypeReferenceInAssembly(assembly.AssemblyDefinition)
						if typeref != None:

	def GetScopeTypeReferenceInAssembly(self, asm):
		enumerator = asm.MainModule.GetTypeReferences().GetEnumerator()
		while enumerator.MoveNext():
			typeref = enumerator.Current
			if typeref.Name == self._analyzedType.Name and typeref.Namespace == self._analyzedType.Namespace:
				return typeref
		return None

class ExtensionMethods(object):
	def HasCustomAttribute(member, attributeTypeName):
		return False

	HasCustomAttribute = staticmethod(HasCustomAttribute)