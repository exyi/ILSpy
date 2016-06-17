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

class PropertyTreeNode(ILSpyTreeNode, IMemberTreeNode):
	""" <summary>
	 Represents a property in the TreeView.
	 </summary>
	"""
	def __init__(self, property):
		if property == None:
			raise ArgumentNullException("property")
		self._property = property
		if property.GetMethod != None:
			self._Children.Add(MethodTreeNode(property.GetMethod))
		if property.SetMethod != None:
			self._Children.Add(MethodTreeNode(property.SetMethod))
		if property.HasOtherMethods:
			enumerator = property.OtherMethods.GetEnumerator()
			while enumerator.MoveNext():
				m = enumerator.Current
				self._Children.Add(MethodTreeNode(m))

	def get_PropertyDefinition(self):
		return property

	PropertyDefinition = property(fget=get_PropertyDefinition)

	def get_Text(self):
		return self.GetText(property, Language, self._isIndexer) + property.MetadataToken.ToSuffixString()

	Text = property(fget=get_Text)

	def GetText(property, language, isIndexer):
		name = language.FormatPropertyName(property, isIndexer)
		b = System.Text.StringBuilder()
		if property.HasParameters:
			b.Append('(')
			i = 0
			while i < property.Parameters.Count:
				if i > 0:
					b.Append(", ")
				b.Append(language.TypeToString(property.Parameters[i].ParameterType, False, property.Parameters[i]))
				i += 1
			method = property.GetMethod == property.SetMethod
			if method.CallingConvention == MethodCallingConvention.VarArg:
				if property.HasParameters:
					b.Append(", ")
				b.Append("...")
			b.Append(") : ")
		else:
			b.Append(" : ")
		b.Append(language.TypeToString(property.PropertyType, False, property))
		b.Append(property.MetadataToken.ToSuffixString())
		return PropertyTreeNode.HighlightSearchMatch(name, b.ToString())

	GetText = staticmethod(GetText)

	def get_Icon(self):
		return self.GetIcon(property)

	Icon = property(fget=get_Icon)

	def GetIcon(property, isIndexer):
		icon = MemberIcon.Indexer if isIndexer else MemberIcon.Property
		attributesOfMostAccessibleMethod = PropertyTreeNode.GetAttributesOfMostAccessibleMethod(property)
		isStatic = (attributesOfMostAccessibleMethod & MethodAttributes.Static) != 0
		return Images.GetIcon(icon, PropertyTreeNode.GetOverlayIcon(attributesOfMostAccessibleMethod), isStatic)

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

	def GetAttributesOfMostAccessibleMethod(property):
		# There should always be at least one method from which to
		# obtain the result, but the compiler doesn't know this so
		# initialize the result with a default value
		result = 0
		# Method access is defined from inaccessible (lowest) to public (highest)
		# in numeric order, so we can do an integer comparison of the masked attribute
		accessLevel = 0
		if property.GetMethod != None:
			methodAccessLevel = (property.GetMethod.Attributes & MethodAttributes.MemberAccessMask)
			if accessLevel < methodAccessLevel:
				accessLevel = methodAccessLevel
				result = property.GetMethod.Attributes
		if property.SetMethod != None:
			methodAccessLevel = (property.SetMethod.Attributes & MethodAttributes.MemberAccessMask)
			if accessLevel < methodAccessLevel:
				accessLevel = methodAccessLevel
				result = property.SetMethod.Attributes
		if property.HasOtherMethods:
			enumerator = property.OtherMethods.GetEnumerator()
			while enumerator.MoveNext():
				m = enumerator.Current
				methodAccessLevel = (m.Attributes & MethodAttributes.MemberAccessMask)
				if accessLevel < methodAccessLevel:
					accessLevel = methodAccessLevel
					result = m.Attributes
		return result

	GetAttributesOfMostAccessibleMethod = staticmethod(GetAttributesOfMostAccessibleMethod)

	def Filter(self, settings):
		if settings.SearchTermMatches(self._property.Name) and settings.Language.ShowMember(self._property):
			return FilterResult.Match
		else:
			return FilterResult.Hidden

	def Decompile(self, language, output, options):
		language.DecompileProperty(self._property, output, options)

	def get_IsPublicAPI(self):
		if self.GetAttributesOfMostAccessibleMethod(self._property) & MethodAttributes.MemberAccessMask == MethodAttributes.Public or self.GetAttributesOfMostAccessibleMethod(self._property) & MethodAttributes.MemberAccessMask == MethodAttributes.Family or self.GetAttributesOfMostAccessibleMethod(self._property) & MethodAttributes.MemberAccessMask == MethodAttributes.FamORAssem:
			return True
		else:
			return False

	IsPublicAPI = property(fget=get_IsPublicAPI)

	def get_Member(self):
		return self._property

	Member = property(fget=get_Member)