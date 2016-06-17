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
from System.Threading import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class DerivedTypesEntryNode(ILSpyTreeNode, IMemberTreeNode):
	def __init__(self, type, assemblies):
		self._type = type
		self._assemblies = assemblies
		self._LazyLoading = True
		self._threading = ThreadingSupport()

	def get_ShowExpander(self):
		return not type.IsSealed and self.ShowExpander

	ShowExpander = property(fget=get_ShowExpander)

	def get_Text(self):
		return self._Language.TypeToString(type, True) + type.MetadataToken.ToSuffixString()

	Text = property(fget=get_Text)

	def get_Icon(self):
		return TypeTreeNode.GetIcon(type)

	Icon = property(fget=get_Icon)

	def Filter(self, settings):
		if not settings.ShowInternalApi and not IsPublicAPI:
			return FilterResult.Hidden
		if settings.SearchTermMatches(self._type.Name):
			if self._type.IsNested and not settings.Language.ShowMember(self._type):
				return FilterResult.Hidden
			else:
				return FilterResult.Match
		else:
			return FilterResult.Recurse

	def get_IsPublicAPI(self):
		if self._type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.Public or self._type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedPublic or self._type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamily or self._type.Attributes & TypeAttributes.VisibilityMask == TypeAttributes.NestedFamORAssem:
			return True
		else:
			return False

	IsPublicAPI = property(fget=get_IsPublicAPI)

	def LoadChildren(self):
		self._threading.LoadChildren(self, FetchChildren)

	def FetchChildren(self, ct):
		# FetchChildren() runs on the main thread; but the enumerator will be consumed on a background thread
		return DerivedTypesTreeNode.FindDerivedTypes(self._type, self._assemblies, ct)

	def ActivateItem(self, e):
		e.Handled = BaseTypesEntryNode.ActivateItem(self, self._type)

	def Decompile(self, language, output, options):
		language.WriteCommentLine(output, language.TypeToString(self._type, True))

	def get_Member(self):
		return self._type

	Member = property(fget=get_Member)