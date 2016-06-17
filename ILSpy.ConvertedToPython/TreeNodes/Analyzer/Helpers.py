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
from System.Linq import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *
from Mono.Cecil.Cil import *

class Helpers(object):
	def IsReferencedBy(type, typeRef):
		# TODO: move it to a better place after adding support for more cases.
		if type == None:
			raise ArgumentNullException("type")
		if typeRef == None:
			raise ArgumentNullException("typeRef")
		if type == typeRef:
			return True
		if type.Name != typeRef.Name:
			return False
		if type.Namespace != typeRef.Namespace:
			return False
		if type.DeclaringType != None or typeRef.DeclaringType != None:
			if type.DeclaringType == None or typeRef.DeclaringType == None:
				return False
			if not Helpers.IsReferencedBy(type.DeclaringType, typeRef.DeclaringType):
				return False
		return True

	IsReferencedBy = staticmethod(IsReferencedBy)

	def GetOriginalCodeLocation(member):
		if :
			return Helpers.GetOriginalCodeLocation(member)
		return member

	GetOriginalCodeLocation = staticmethod(GetOriginalCodeLocation)

	def GetOriginalCodeLocation(method):
		if method.IsCompilerGenerated():
			return Helpers.FindMethodUsageInType(method.DeclaringType, method) == method
		typeUsage = Helpers.GetOriginalCodeLocation(method.DeclaringType)
		return typeUsage == method

	GetOriginalCodeLocation = staticmethod(GetOriginalCodeLocation)

	def GetOriginalCodeLocation(type):
		""" <summary>
		 Given a compiler-generated type, returns the method where that type is used.
		 Used to detect the 'parent method' for a lambda/iterator/async state machine.
		 </summary>
		"""
		if type != None and type.DeclaringType != None and type.IsCompilerGenerated():
			if type.IsValueType:
				# Value types might not have any constructor; but they must be stored in a local var
				# because 'initobj' (or 'call .ctor') expects a managed ref.
				return Helpers.FindVariableOfTypeUsageInType(type.DeclaringType, type)
			else:
				constructor = Helpers.GetTypeConstructor(type)
				if constructor == None:
					return None
				return Helpers.FindMethodUsageInType(type.DeclaringType, constructor)
		return None

	GetOriginalCodeLocation = staticmethod(GetOriginalCodeLocation)

	def GetTypeConstructor(type):
		return type.Methods.FirstOrDefault()

	GetTypeConstructor = staticmethod(GetTypeConstructor)

	def FindMethodUsageInType(type, analyzedMethod):
		name = analyzedMethod.Name
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			found = False
			if not method.HasBody:
				continue
			enumerator = method.Body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				instr = enumerator.Current
				mr = instr.Operand
				if mr != None and mr.Name == name and Helpers.IsReferencedBy(analyzedMethod.DeclaringType, mr.DeclaringType) and mr.Resolve() == analyzedMethod:
					found = True
					break
			method.Body = None
			if found:
				return method
		return None

	FindMethodUsageInType = staticmethod(FindMethodUsageInType)

	def FindVariableOfTypeUsageInType(type, variableType):
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			found = False
			if not method.HasBody:
				continue
			enumerator = method.Body.Variables.GetEnumerator()
			while enumerator.MoveNext():
				v = enumerator.Current
				if v.VariableType.ResolveWithinSameModule() == variableType:
					found = True
					break
			method.Body = None
			if found:
				return method
		return None

	FindVariableOfTypeUsageInType = staticmethod(FindVariableOfTypeUsageInType)