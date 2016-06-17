import clr

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
from System.Windows.Media import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class TypeTreeNode(ILSpyTreeNode, IMemberTreeNode):
	def __init__(self, type, parentAssemblyNode):
		if parentAssemblyNode == None:
			raise ArgumentNullException("parentAssemblyNode")
		if type == None:
			raise ArgumentNullException("type")
		self._type = type
		self._parentAssemblyNode = parentAssemblyNode
		self._LazyLoading = True

	def get_TypeDefinition(self):
		return type

	TypeDefinition = property(fget=get_TypeDefinition)

	def get_ParentAssemblyNode(self):
		return parentAssemblyNode

	ParentAssemblyNode = property(fget=get_ParentAssemblyNode)

	def get_Name(self):
		return type.Name

	Name = property(fget=get_Name)

	def get_Namespace(self):
		return type.Namespace

	Namespace = property(fget=get_Namespace)

	def get_Text(self):
		return self.HighlightSearchMatch(self._Language.FormatTypeName(type), type.MetadataToken.ToSuffixString())

	Text = property(fget=get_Text)

	def get_IsPublicAPI(self):
		if type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.Public or type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedPublic or type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamily or type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamORAssem:
			return True
		else:
			return False

	IsPublicAPI = property(fget=get_IsPublicAPI)

	def Filter(self, settings):
		if not settings.ShowInternalApi and not self.IsPublicAPI:
			return FilterResult.Hidden
		if settings.SearchTermMatches(self._type.Name):
			if settings.Language.ShowMember(self._type):
				return FilterResult.Match
			else:
				return FilterResult.Hidden
		else:
			return FilterResult.Recurse

	def LoadChildren(self):
		if self._type.BaseType != None or self._type.HasInterfaces:
			self._Children.Add(BaseTypesTreeNode(self._type))
		if not self._type.IsSealed:
			self._Children.Add(DerivedTypesTreeNode(self._parentAssemblyNode.AssemblyList, self._type))
		enumerator = self._type.NestedTypes.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			nestedType = enumerator.Current
			self._Children.Add(TypeTreeNode(nestedType, self._parentAssemblyNode))
		enumerator = self._type.Fields.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			field = enumerator.Current
			self._Children.Add(FieldTreeNode(field))
		enumerator = self._type.Properties.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			property = enumerator.Current
			self._Children.Add(PropertyTreeNode(property))
		enumerator = self._type.Events.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			ev = enumerator.Current
			self._Children.Add(EventTreeNode(ev))
		accessorMethods = self._type.GetAccessorMethods()
		enumerator = self._type.Methods.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			if not accessorMethods.Contains(method):
				self._Children.Add(MethodTreeNode(method))

	def get_CanExpandRecursively(self):
		return True

	CanExpandRecursively = property(fget=get_CanExpandRecursively)

	def Decompile(self, language, output, options):
		language.DecompileType(self._type, output, options)

	def get_Icon(self):
		return self.GetIcon(self._type)

	Icon = property(fget=get_Icon)

	def GetIcon(type):
		typeIcon = TypeTreeNode.GetTypeIcon(type)
		overlayIcon = TypeTreeNode.GetOverlayIcon(type)
		return Images.GetIcon(typeIcon, overlayIcon)

	GetIcon = staticmethod(GetIcon)

	def GetTypeIcon(type):
		if type.IsValueType:
			if type.IsEnum:
				return TypeIcon.Enum
			else:
				return TypeIcon.Struct
		else:
			if type.IsInterface:
				return TypeIcon.Interface
			elif TypeTreeNode.IsDelegate(type):
				return TypeIcon.Delegate
			elif TypeTreeNode.IsStaticClass(type):
				return TypeIcon.StaticClass
			else:
				return TypeIcon.Class

	GetTypeIcon = staticmethod(GetTypeIcon)

	def GetOverlayIcon(type):
		if type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.Public or type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedPublic:
			overlay = AccessOverlayIcon.Public
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NotPublic or type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedAssembly or type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamANDAssem:
			overlay = AccessOverlayIcon.Internal
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamily or type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamORAssem:
			overlay = AccessOverlayIcon.Protected
		elif type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedPrivate:
			overlay = AccessOverlayIcon.Private
		else:
			raise NotSupportedException()
		return overlay

	GetOverlayIcon = staticmethod(GetOverlayIcon)

	def IsDelegate(type):
		return type.BaseType != None and type.BaseType.FullName == clr.GetClrType(MulticastDelegate).FullName

	IsDelegate = staticmethod(IsDelegate)

	def IsStaticClass(type):
		return type.IsSealed and type.IsAbstract

	IsStaticClass = staticmethod(IsStaticClass)

	def get_Member(self):
		return type

	Member = property(fget=get_Member)