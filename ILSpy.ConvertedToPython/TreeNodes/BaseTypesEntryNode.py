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
from ICSharpCode.TreeView import *
from Mono.Cecil import *

class BaseTypesEntryNode(ILSpyTreeNode, IMemberTreeNode):
	def __init__(self, tr, isInterface):
		if tr == None:
			raise ArgumentNullException("tr")
		self._tr = tr
		self._def = tr.Resolve()
		self._isInterface = isInterface
		self._LazyLoading = True

	def get_ShowExpander(self):
		return self._def != None and (self._def.BaseType != None or self._def.HasInterfaces)

	ShowExpander = property(fget=get_ShowExpander)

	def get_Text(self):
		return self._Language.TypeToString(tr, True) + tr.MetadataToken.ToSuffixString()

	Text = property(fget=get_Text)

	def get_Icon(self):
		if self._def != None:
			return TypeTreeNode.GetIcon(self._def)
		else:
			return Images.Interface if isInterface else Images.Class

	Icon = property(fget=get_Icon)

	def LoadChildren(self):
		if self._def != None:
			BaseTypesTreeNode.AddBaseTypes(self._Children, self._def)

	def ActivateItem(self, e):
		# on item activation, try to resolve once again (maybe the user loaded the assembly in the meantime)
		if self._def == None:
			self._def = self._tr.Resolve()
			if self._def != None:
				self._LazyLoading = True
		# re-load children
		e.Handled = self.ActivateItem(self, self._def)

	def ActivateItem(node, def):
		if def != None:
			assemblyListNode = node.Ancestors().OfType().FirstOrDefault()
			if assemblyListNode != None:
				assemblyListNode.Select(assemblyListNode.FindTypeNode(def))
				return True
		return False

	ActivateItem = staticmethod(ActivateItem)

	def Decompile(self, language, output, options):
		language.WriteCommentLine(output, language.TypeToString(self._tr, True))

	def get_Member(self):
		return self._tr

	Member = property(fget=get_Member)