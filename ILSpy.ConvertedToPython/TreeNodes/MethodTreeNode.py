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
from System.Text import *
from System.Windows.Media import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class MethodTreeNode(ILSpyTreeNode, IMemberTreeNode):
	""" <summary>
	 Tree Node representing a field, method, property, or event.
	 </summary>
	"""
	def get_MethodDefinition(self):
		return self._method

	MethodDefinition = property(fget=get_MethodDefinition)

	def __init__(self, method):
		if method == None:
			raise ArgumentNullException("method")
		self._method = method

	def get_Text(self):
		return self.GetText(method, Language)

	Text = property(fget=get_Text)

	def GetText(method, language):
		b = StringBuilder()
		b.Append('(')
		i = 0
		while i < method.Parameters.Count:
			if i > 0:
				b.Append(", ")
			b.Append(language.TypeToString(method.Parameters[i].ParameterType, False, method.Parameters[i]))
			i += 1
		if method.CallingConvention == MethodCallingConvention.VarArg:
			if method.HasParameters:
				b.Append(", ")
			b.Append("...")
		b.Append(") : ")
		b.Append(language.TypeToString(method.ReturnType, False, method.MethodReturnType))
		b.Append(method.MetadataToken.ToSuffixString())
		return MethodTreeNode.HighlightSearchMatch(language.FormatMethodName(method), b.ToString())

	GetText = staticmethod(GetText)

	def get_Icon(self):
		return self.GetIcon(method)

	Icon = property(fget=get_Icon)

	def GetIcon(method):
		if method.IsSpecialName and method.Name.StartsWith("op_", StringComparison.Ordinal):
			return Images.GetIcon(MemberIcon.Operator, MethodTreeNode.GetOverlayIcon(method.Attributes), False)
		if method.IsStatic and method.HasCustomAttributes:
			enumerator = method.CustomAttributes.GetEnumerator()
			while enumerator.MoveNext():
				ca = enumerator.Current
				if ca.AttributeType.FullName == "System.Runtime.CompilerServices.ExtensionAttribute":
					return Images.GetIcon(MemberIcon.ExtensionMethod, MethodTreeNode.GetOverlayIcon(method.Attributes), False)
		if method.IsSpecialName and (method.Name == ".ctor" or method.Name == ".cctor"):
			return Images.GetIcon(MemberIcon.Constructor, MethodTreeNode.GetOverlayIcon(method.Attributes), method.IsStatic)
		if method.HasPInvokeInfo:
			return Images.GetIcon(MemberIcon.PInvokeMethod, MethodTreeNode.GetOverlayIcon(method.Attributes), True)
		showAsVirtual = method.IsVirtual and not (method.IsNewSlot and method.IsFinal) and not method.DeclaringType.IsInterface
		return Images.GetIcon(MemberIcon.VirtualMethod if showAsVirtual else MemberIcon.Method, MethodTreeNode.GetOverlayIcon(method.Attributes), method.IsStatic)

	GetIcon = staticmethod(GetIcon)

	def GetOverlayIcon(methodAttributes):
		if methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Public:
			return AccessOverlayIcon.Public
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Assembly or methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.FamANDAssem:
			return AccessOverlayIcon.Internal
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Family:
			return AccessOverlayIcon.Protected
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.FamORAssem:
			return AccessOverlayIcon.ProtectedInternal
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Private:
			return AccessOverlayIcon.Private
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.CompilerControlled:
			return AccessOverlayIcon.CompilerControlled
		else:
			raise NotSupportedException()

	GetOverlayIcon = staticmethod(GetOverlayIcon)

	def Decompile(self, language, output, options):
		language.DecompileMethod(self._method, output, options)

	def Filter(self, settings):
		if settings.SearchTermMatches(self._method.Name) and settings.Language.ShowMember(self._method):
			return FilterResult.Match
		else:
			return FilterResult.Hidden

	def get_IsPublicAPI(self):
		return self._method.IsPublic or self._method.IsFamily or self._method.IsFamilyOrAssembly

	IsPublicAPI = property(fget=get_IsPublicAPI)

	def get_Member(self):
		return self._method

	Member = property(fget=get_Member)