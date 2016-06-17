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
from System.Diagnostics import *
from System.Linq import *
from System.Text import *
from Mono.Cecil import *

class XmlDocKeyProvider(object):
	""" <summary>
	 Provides XML documentation tags.
	 </summary>
	"""
	def GetKey(member):
		b = StringBuilder()
		if :
			b.Append("T:")
			XmlDocKeyProvider.AppendTypeName(b, member)
		else:
			if :
				b.Append("F:")
			elif :
				b.Append("P:")
			elif :
				b.Append("E:")
			elif :
				b.Append("M:")
			XmlDocKeyProvider.AppendTypeName(b, member.DeclaringType)
			b.Append('.')
			b.Append(member.Name.Replace('.', '#'))
			explicitReturnType = None
			if :
				parameters = (member).Parameters
			elif :
				mr = member
				if mr.HasGenericParameters:
					b.Append("``")
					b.Append(mr.GenericParameters.Count)
				parameters = mr.Parameters
				if mr.Name == "op_Implicit" or mr.Name == "op_Explicit":
					explicitReturnType = mr.ReturnType
			else:
				parameters = None
			if parameters != None and parameters.Count > 0:
				b.Append('(')
				i = 0
				while i < parameters.Count:
					if i > 0:
						b.Append(',')
					XmlDocKeyProvider.AppendTypeName(b, parameters[i].ParameterType)
					i += 1
				b.Append(')')
			if explicitReturnType != None:
				b.Append('~')
				XmlDocKeyProvider.AppendTypeName(b, explicitReturnType)
		return b.ToString()

	GetKey = staticmethod(GetKey)

	def AppendTypeName(b, type):
		if type == None:
			# could happen when a TypeSpecification has no ElementType; e.g. function pointers in C++/CLI assemblies
			return 
		if :
			giType = type
			XmlDocKeyProvider.AppendTypeNameWithArguments(b, giType.ElementType, giType.GenericArguments)
		elif :
			XmlDocKeyProvider.AppendTypeName(b, (type).ElementType)
			arrayType = type
			if arrayType != None:
				b.Append('[')
				i = 0
				while i < arrayType.Dimensions.Count:
					if i > 0:
						b.Append(',')
					ad = arrayType.Dimensions[i]
					if ad.IsSized:
						b.Append(ad.LowerBound)
						b.Append(':')
						b.Append(ad.UpperBound)
					i += 1
				b.Append(']')
			refType = type
			if refType != None:
				b.Append('@')
			ptrType = type
			if ptrType != None:
				b.Append('*')
		else:
			gp = type
			if gp != None:
				b.Append('`')
				if gp.Owner.GenericParameterType == GenericParameterType.Method:
					b.Append('`')
				b.Append(gp.Position)
			elif type.DeclaringType != None:
				XmlDocKeyProvider.AppendTypeName(b, type.DeclaringType)
				b.Append('.')
				b.Append(type.Name)
			else:
				b.Append(type.FullName)

	AppendTypeName = staticmethod(AppendTypeName)

	def AppendTypeNameWithArguments(b, type, genericArguments):
		outerTypeParameterCount = 0
		if type.DeclaringType != None:
			declType = type.DeclaringType
			outerTypeParameterCount = XmlDocKeyProvider.AppendTypeNameWithArguments(b, declType, genericArguments)
			b.Append('.')
		elif not str.IsNullOrEmpty(type.Namespace):
			b.Append(type.Namespace)
			b.Append('.')
		localTypeParameterCount = 0
		b.Append(NRefactory.TypeSystem.ReflectionHelper.SplitTypeParameterCountFromReflectionName(type.Name, ))
		if localTypeParameterCount > 0:
			totalTypeParameterCount = outerTypeParameterCount + localTypeParameterCount
			b.Append('{')
			i = outerTypeParameterCount
			while i < totalTypeParameterCount and i < genericArguments.Count:
				if i > outerTypeParameterCount:
					b.Append(',')
				XmlDocKeyProvider.AppendTypeName(b, genericArguments[i])
				i += 1
			b.Append('}')
		return outerTypeParameterCount + localTypeParameterCount

	AppendTypeNameWithArguments = staticmethod(AppendTypeNameWithArguments)

	def FindMemberByKey(module, key):
		if module == None:
			raise ArgumentNullException("module")
		if key == None or key.Length < 2 or key[1] != ':':
			return None
		if key[0] == 'T':
			return XmlDocKeyProvider.FindType(module, key.Substring(2))
		elif key[0] == 'F':
			return XmlDocKeyProvider.FindMember(module, key, )
		elif key[0] == 'P':
			return XmlDocKeyProvider.FindMember(module, key, )
		elif key[0] == 'E':
			return XmlDocKeyProvider.FindMember(module, key, )
		elif key[0] == 'M':
			return XmlDocKeyProvider.FindMember(module, key, )
		else:
			return None

	FindMemberByKey = staticmethod(FindMemberByKey)

	def FindMember(module, key, memberSelector):
		Debug.WriteLine("Looking for member " + key)
		parenPos = key.IndexOf('(')
		if parenPos > 0:
			dotPos = key.LastIndexOf('.', parenPos - 1, parenPos)
		else:
			dotPos = key.LastIndexOf('.')
		if dotPos < 0:
			return None
		type = XmlDocKeyProvider.FindType(module, key.Substring(2, dotPos - 2))
		if type == None:
			return None
		if parenPos > 0:
			shortName = key.Substring(dotPos + 1, parenPos - (dotPos + 1))
		else:
			shortName = key.Substring(dotPos + 1)
		Debug.WriteLine("Searching in type {0} for {1}", type.FullName, shortName)
		shortNameMatch = None
		enumerator = XmlDocKeyProvider.memberSelector(type).GetEnumerator()
		while enumerator.MoveNext():
			member = enumerator.Current
			memberKey = XmlDocKeyProvider.GetKey(member)
			Debug.WriteLine(memberKey)
			if memberKey == key:
				return member
			if shortName == member.Name.Replace('.', '#'):
				shortNameMatch = member
		# if there's no match by ID string (key), return the match by name.
		return shortNameMatch

	FindMember = staticmethod(FindMember)

	def FindType(module, name):
		pos = name.LastIndexOf('.')
		if pos >= 0:
			ns = name.Substring(0, pos)
			name = name.Substring(pos + 1)
		else:
			ns = str.Empty
		if str.IsNullOrEmpty(name):
			return None
		type = module.GetType(ns, name)
		if type == None and ns.Length > 0:
			# try if this is a nested type
			type = XmlDocKeyProvider.FindType(module, ns)
			if type != None:
				type = type.NestedTypes.FirstOrDefault()
		return type

	FindType = staticmethod(FindType)