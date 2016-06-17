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
from System.Windows.Threading import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class ReferenceFolderTreeNode(ILSpyTreeNode):
	""" <summary>
	 References folder.
	 </summary>
	"""
	def __init__(self, module, parentAssembly):
		self._module = module
		self._parentAssembly = parentAssembly
		self._LazyLoading = True

	def get_Text(self):
		return "References"

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.ReferenceFolderClosed

	Icon = property(fget=get_Icon)

	def get_ExpandedIcon(self):
		return Images.ReferenceFolderOpen

	ExpandedIcon = property(fget=get_ExpandedIcon)

	def LoadChildren(self):
		enumerator = self._module.AssemblyReferences.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			r = enumerator.Current
			self._Children.Add(AssemblyReferenceTreeNode(r, self._parentAssembly))
		enumerator = self._module.ModuleReferences.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			r = enumerator.Current
			self._Children.Add(ModuleReferenceTreeNode(r))

	def Decompile(self, language, output, options):
		App.Current.Dispatcher.Invoke(DispatcherPriority.Normal, Action(EnsureLazyChildren))
		# Show metadata order of references
		enumerator = self._module.AssemblyReferences.GetEnumerator()
		while enumerator.MoveNext():
			r = enumerator.Current
			AssemblyReferenceTreeNode(r, self._parentAssembly).Decompile(language, output, options)
		enumerator = self._module.ModuleReferences.GetEnumerator()
		while enumerator.MoveNext():
			r = enumerator.Current
			language.WriteCommentLine(output, r.Name)