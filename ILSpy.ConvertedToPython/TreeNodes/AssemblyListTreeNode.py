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
from System.Collections.ObjectModel import *
from System.Collections.Specialized import *
from System.Linq import *
from System.Windows import *
from ICSharpCode.Decompiler import *
from ICSharpCode.TreeView import *
from Mono.Cecil import *

class AssemblyListTreeNode(ILSpyTreeNode):
	""" <summary>
	 Represents a list of assemblies.
	 This is used as (invisible) root node of the tree view.
	 </summary>
	"""
	def get_AssemblyList(self):
		return self._assemblyList

	AssemblyList = property(fget=get_AssemblyList)

	def __init__(self, assemblyList):
		self._Select = 
		if assemblyList == None:
			raise ArgumentNullException("assemblyList")
		self._assemblyList = assemblyList
		self.BindToObservableCollection(assemblyList.assemblies)

	def get_Text(self):
		return assemblyList.ListName

	Text = property(fget=get_Text)

	def BindToObservableCollection(self, collection):
		self._Children.Clear()
		self._Children.AddRange(collection.Select())
		collection.CollectionChanged += 

	def CanDrop(self, e, index):
		e.Effects = DragDropEffects.Move
		if e.Data.GetDataPresent(AssemblyTreeNode.DataFormat):
			return True
		elif e.Data.GetDataPresent(DataFormats.FileDrop):
			return True
		else:
			e.Effects = DragDropEffects.None
			return False

	def Drop(self, e, index):
		files = e.Data.GetData(AssemblyTreeNode.DataFormat)
		if files == None:
			files = e.Data.GetData(DataFormats.FileDrop)
		if files != None:

	def Decompile(self, language, output, options):
		language.WriteCommentLine(output, "List: " + self._assemblyList.ListName)
		output.WriteLine()
		enumerator = self._Children.GetEnumerator()
		while enumerator.MoveNext():
			asm = enumerator.Current
			language.WriteCommentLine(output, System.String('-', 60))
			output.WriteLine()
			asm.Decompile(language, output, options)

	def FindResourceNode(self, resource):
		if resource == None:
			return None
		enumerator = self._Children.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			if node.LoadedAssembly.IsLoaded:
				node.EnsureLazyChildren()
				enumerator = node.Children.OfType().GetEnumerator()
				while enumerator.MoveNext():
					item = enumerator.Current
					founded = item.Children.OfType().Where().FirstOrDefault()
					if founded != None:
						return founded
					foundedResEntry = item.Children.OfType().Where().FirstOrDefault()
					if foundedResEntry != None:
						return foundedResEntry
		return None

	def FindAssemblyNode(self, module):
		if module == None:
			return None
		App.Current.Dispatcher.VerifyAccess()
		enumerator = self._Children.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			if node.LoadedAssembly.IsLoaded and node.LoadedAssembly.ModuleDefinition == module:
				return node
		return None

	def FindAssemblyNode(self, asm):
		if asm == None:
			return None
		App.Current.Dispatcher.VerifyAccess()
		enumerator = self._Children.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			if node.LoadedAssembly.IsLoaded and node.LoadedAssembly.AssemblyDefinition == asm:
				return node
		return None

	def FindAssemblyNode(self, asm):
		if asm == None:
			return None
		App.Current.Dispatcher.VerifyAccess()
		enumerator = self._Children.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			if node.LoadedAssembly == asm:
				return node
		return None

	def FindTypeNode(self, def):
		""" <summary>
		 Looks up the type node corresponding to the type definition.
		 Returns null if no matching node is found.
		 </summary>
		"""
		if def == None:
			return None
		if def.DeclaringType != None:
			decl = self.FindTypeNode(def.DeclaringType)
			if decl != None:
				decl.EnsureLazyChildren()
				return decl.Children.OfType().FirstOrDefault()
		else:
			asm = self.FindAssemblyNode(def.Module.Assembly)
			if asm != None:
				return asm.FindTypeNode(def)
		return None

	def FindMethodNode(self, def):
		""" <summary>
		 Looks up the method node corresponding to the method definition.
		 Returns null if no matching node is found.
		 </summary>
		"""
		if def == None:
			return None
		typeNode = self.FindTypeNode(def.DeclaringType)
		if typeNode == None:
			return None
		typeNode.EnsureLazyChildren()
		methodNode = typeNode.Children.OfType().FirstOrDefault()
		if methodNode != None:
			return methodNode
		enumerator = typeNode.Children.OfType().GetEnumerator()
		while enumerator.MoveNext():
			p = enumerator.Current
			if p.IsHidden:
				continue
			# method might be a child of a property or event
			if  or :
				p.EnsureLazyChildren()
				methodNode = p.Children.OfType().FirstOrDefault()
				if methodNode != None:
					# If the requested method is a property or event accessor, and accessors are
					# hidden in the UI, then return the owning property or event.
					if methodNode.IsHidden:
						return p
					else:
						return methodNode
		return None

	def FindFieldNode(self, def):
		""" <summary>
		 Looks up the field node corresponding to the field definition.
		 Returns null if no matching node is found.
		 </summary>
		"""
		if def == None:
			return None
		typeNode = self.FindTypeNode(def.DeclaringType)
		if typeNode == None:
			return None
		typeNode.EnsureLazyChildren()
		return typeNode.Children.OfType().FirstOrDefault()

	def FindPropertyNode(self, def):
		""" <summary>
		 Looks up the property node corresponding to the property definition.
		 Returns null if no matching node is found.
		 </summary>
		"""
		if def == None:
			return None
		typeNode = self.FindTypeNode(def.DeclaringType)
		if typeNode == None:
			return None
		typeNode.EnsureLazyChildren()
		return typeNode.Children.OfType().FirstOrDefault()

	def FindEventNode(self, def):
		""" <summary>
		 Looks up the event node corresponding to the event definition.
		 Returns null if no matching node is found.
		 </summary>
		"""
		if def == None:
			return None
		typeNode = self.FindTypeNode(def.DeclaringType)
		if typeNode == None:
			return None
		typeNode.EnsureLazyChildren()
		return typeNode.Children.OfType().FirstOrDefault()