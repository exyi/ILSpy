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
from System.Windows.Media import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class FieldTreeNode(ILSpyTreeNode, IMemberTreeNode):
	""" <summary>
	 Represents a field in the TreeView.
	 </summary>
	"""
	def get_FieldDefinition(self):
		return self._field

	FieldDefinition = property(fget=get_FieldDefinition)

	def __init__(self, field):
		if field == None:
			raise ArgumentNullException("field")
		self._field = field

	def get_Text(self):
		return self.HighlightSearchMatch(field.Name, " : " + self._Language.TypeToString(field.FieldType, False, field) + field.MetadataToken.ToSuffixString())

	Text = property(fget=get_Text)

	def get_Icon(self):
		return self.GetIcon(field)

	Icon = property(fget=get_Icon)

	def GetIcon(field):
		if field.DeclaringType.IsEnum and not field.Attributes.HasFlag(FieldAttributes.SpecialName):
			return Images.GetIcon(MemberIcon.EnumValue, FieldTreeNode.GetOverlayIcon(field.Attributes), False)
		if field.IsLiteral:
			return Images.GetIcon(MemberIcon.Literal, FieldTreeNode.GetOverlayIcon(field.Attributes), False)
		elif field.IsInitOnly:
			if FieldTreeNode.IsDecimalConstant(field):
				return Images.GetIcon(MemberIcon.Literal, FieldTreeNode.GetOverlayIcon(field.Attributes), False)
			else:
				return Images.GetIcon(MemberIcon.FieldReadOnly, FieldTreeNode.GetOverlayIcon(field.Attributes), field.IsStatic)
		else:
			return Images.GetIcon(MemberIcon.Field, FieldTreeNode.GetOverlayIcon(field.Attributes), field.IsStatic)

	GetIcon = staticmethod(GetIcon)

	def IsDecimalConstant(field):
		fieldType = field.FieldType
		if fieldType.Name == "Decimal" and fieldType.Namespace == "System":
			if field.HasCustomAttributes:
				attrs = field.CustomAttributes
				i = 0
				while i < attrs.Count:
					attrType = attrs[i].AttributeType
					if attrType.Name == "DecimalConstantAttribute" and attrType.Namespace == "System.Runtime.CompilerServices":
						return True
					i += 1
		return False

	IsDecimalConstant = staticmethod(IsDecimalConstant)

	def GetOverlayIcon(fieldAttributes):
		if fieldAttributes & FieldAttributes.FieldAccessMask == FieldAttributes.Public:
			return AccessOverlayIcon.Public
		elif fieldAttributes & FieldAttributes.FieldAccessMask == FieldAttributes.Assembly or fieldAttributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamANDAssem:
			return AccessOverlayIcon.Internal
		elif fieldAttributes & FieldAttributes.FieldAccessMask == FieldAttributes.Family:
			return AccessOverlayIcon.Protected
		elif fieldAttributes & FieldAttributes.FieldAccessMask == FieldAttributes.FamORAssem:
			return AccessOverlayIcon.ProtectedInternal
		elif fieldAttributes & FieldAttributes.FieldAccessMask == FieldAttributes.Private:
			return AccessOverlayIcon.Private
		elif fieldAttributes & FieldAttributes.FieldAccessMask == FieldAttributes.CompilerControlled:
			return AccessOverlayIcon.CompilerControlled
		else:
			raise NotSupportedException()

	GetOverlayIcon = staticmethod(GetOverlayIcon)

	def Filter(self, settings):
		if settings.SearchTermMatches(self._field.Name) and settings.Language.ShowMember(self._field):
			return FilterResult.Match
		else:
			return FilterResult.Hidden

	def Decompile(self, language, output, options):
		language.DecompileField(self._field, output, options)

	def get_IsPublicAPI(self):
		return self._field.IsPublic or self._field.IsFamily or self._field.IsFamilyOrAssembly

	IsPublicAPI = property(fget=get_IsPublicAPI)

	def get_Member(self):
		return self._field

	Member = property(fget=get_Member)