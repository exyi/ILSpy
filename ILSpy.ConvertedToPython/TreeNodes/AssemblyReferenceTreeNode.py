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
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class AssemblyReferenceTreeNode(ILSpyTreeNode):
	""" <summary>
	 Node within assembly reference list.
	 </summary>
	"""
	def __init__(self, r, parentAssembly):
		if parentAssembly == None:
			raise ArgumentNullException("parentAssembly")
		if r == None:
			raise ArgumentNullException("r")
		self._r = r
		self._parentAssembly = parentAssembly
		self._LazyLoading = True

	def get_AssemblyNameReference(self):
		return r

	AssemblyNameReference = property(fget=get_AssemblyNameReference)

	def get_Text(self):
		return r.Name + r.MetadataToken.ToSuffixString()

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.Assembly

	Icon = property(fget=get_Icon)

	def get_ShowExpander(self):
		if r.Name == "mscorlib":
			self.EnsureLazyChildren() # likely doesn't have any children
		return self.ShowExpander

	ShowExpander = property(fget=get_ShowExpander)

	def ActivateItem(self, e):
		assemblyListNode = self._parentAssembly.Parent
		if assemblyListNode != None:
			assemblyListNode.Select(assemblyListNode.FindAssemblyNode(self._parentAssembly.LoadedAssembly.LookupReferencedAssembly(self._r)))
			e.Handled = True

	def LoadChildren(self):
		assemblyListNode = self._parentAssembly.Parent
		if assemblyListNode != None:
			refNode = assemblyListNode.FindAssemblyNode(self._parentAssembly.LoadedAssembly.LookupReferencedAssembly(self._r))
			if refNode != None:
				module = refNode.LoadedAssembly.ModuleDefinition
				if module != None:
					enumerator = module.AssemblyReferences.GetEnumerator()
					while enumerator.MoveNext():
						childRef = enumerator.Current
						self._Children.Add(AssemblyReferenceTreeNode(childRef, refNode))

	def Decompile(self, language, output, options):
		if self._r.IsWindowsRuntime:
			language.WriteCommentLine(output, self._r.Name + " [WinRT]")
		else:
			language.WriteCommentLine(output, self._r.FullName)