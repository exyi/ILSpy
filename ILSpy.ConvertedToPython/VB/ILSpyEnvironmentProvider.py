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
from ICSharpCode.Decompiler import *
from ICSharpCode.Decompiler.Ast import *
from ICSharpCode.NRefactory.TypeSystem import *
from ICSharpCode.NRefactory.VB.Visitors import *
from Mono.Cecil import *

class ILSpyEnvironmentProvider(IEnvironmentProvider):
	def get_RootNamespace(self):
		return ""

	RootNamespace = property(fget=get_RootNamespace)

	#readonly CecilLoader loader = new CecilLoader();
	def GetTypeNameForAttribute(self, attribute):
		return attribute.Type.Annotations.OfType().First().FullName

	def ResolveType(self, type, entity):
		# 
		# var annotation = type.Annotation<TypeReference>();
		# if (annotation == null )
		# return null;
		# 
		# IEntity current = null;
		# if (entity != null) {
		# var typeInfo = entity.Annotation<TypeReference>();
		# current = loader.ReadTypeReference(typeInfo).Resolve(context).GetDefinition();
		# }
		# 
		# return loader.ReadTypeReference(annotation, entity: current).Resolve(context);
		return SpecialType.UnknownType

	def GetTypeKindForAstType(self, type):
		annotation = type.Annotation()
		if annotation == None:
			return TypeKind.Unknown
		definition = annotation.ResolveOrThrow()
		if definition.IsClass:
			return TypeKind.Class
		if definition.IsInterface:
			return TypeKind.Interface
		if definition.IsEnum:
			return TypeKind.Enum
		if definition.IsFunctionPointer:
			return TypeKind.Delegate
		if definition.IsValueType:
			return TypeKind.Struct
		return TypeKind.Unknown

	def ResolveExpression(self, expression):
		annotation = expression.Annotations.OfType().FirstOrDefault()
		if annotation == None or annotation.InferredType == None:
			return TypeCode.Object
		definition = annotation.InferredType.Resolve()
		if definition == None:
			return TypeCode.Object
		if definition.FullName == "System.String":
			return TypeCode.String
		else:
			pass
		return TypeCode.Object

	def IsReferenceType(self, expression):
		if :
			return True
		annotation = expression.Annotations.OfType().FirstOrDefault()
		if annotation == None or annotation.InferredType == None:
			return None
		definition = annotation.InferredType.Resolve()
		if definition == None:
			return None
		return not definition.IsValueType

	def CreateMemberSpecifiersForInterfaces(self, interfaces):
		enumerator = interfaces.GetEnumerator()
		while enumerator.MoveNext():
			type = enumerator.Current
			def = type.Annotation().Resolve()
			if def == None:
				continue
			enumerator = def.Methods.Where().GetEnumerator()
			while enumerator.MoveNext():
				method = enumerator.Current
			enumerator = def.Properties.GetEnumerator()
			while enumerator.MoveNext():
				property = enumerator.Current

	def HasEvent(self, expression):
		return expression.Annotation() != None

	def IsMethodGroup(self, expression):
		methodInfo =  if expression.Annotation() else