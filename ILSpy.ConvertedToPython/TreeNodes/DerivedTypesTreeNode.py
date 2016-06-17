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
from System.Threading import *
from ICSharpCode.Decompiler import *
from ICSharpCode.NRefactory.Utils import *
from Mono.Cecil import *

class DerivedTypesTreeNode(ILSpyTreeNode):
	""" <summary>
	 Lists the super types of a class.
	 </summary>
	"""
	def __init__(self, list, type):
		self._list = list
		self._type = type
		self._LazyLoading = True
		self._threading = ThreadingSupport()

	def get_Text(self):
		return "Derived Types"

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.SubTypes

	Icon = property(fget=get_Icon)

	def LoadChildren(self):
		self._threading.LoadChildren(self, FetchChildren)

	def FetchChildren(self, cancellationToken):
		# FetchChildren() runs on the main thread; but the enumerator will be consumed on a background thread
		assemblies = self._list.GetAssemblies().Select().Where().ToArray()
		return self.FindDerivedTypes(self._type, assemblies, cancellationToken)

	def FindDerivedTypes(type, assemblies, cancellationToken):
		enumerator = assemblies.GetEnumerator()
		while enumerator.MoveNext():
			module = enumerator.Current
			enumerator = TreeTraversal.PreOrder(module.Types, ).GetEnumerator()
			while enumerator.MoveNext():
				td = enumerator.Current
				cancellationToken.ThrowIfCancellationRequested()
				if type.IsInterface and td.HasInterfaces:
					enumerator = td.Interfaces.GetEnumerator()
					while enumerator.MoveNext():
						typeRef = enumerator.Current
						if DerivedTypesTreeNode.IsSameType(typeRef, type):
				elif not type.IsInterface and td.BaseType != None and DerivedTypesTreeNode.IsSameType(td.BaseType, type):

	FindDerivedTypes = staticmethod(FindDerivedTypes)

	def IsSameType(typeRef, type):
		if typeRef.FullName == type.FullName:
			return True
		if typeRef.Name != type.Name or type.Namespace != typeRef.Namespace:
			return False
		if typeRef.IsNested or type.IsNested:
			if not typeRef.IsNested or not type.IsNested or not DerivedTypesTreeNode.IsSameType(typeRef.DeclaringType, type.DeclaringType):
				return False
		gTypeRef = typeRef
		if gTypeRef != None or type.HasGenericParameters:
			if gTypeRef == None or not type.HasGenericParameters or gTypeRef.GenericArguments.Count != type.GenericParameters.Count:
				return False
		return True

	IsSameType = staticmethod(IsSameType)

	def Decompile(self, language, output, options):
		self._threading.Decompile(language, output, options, EnsureLazyChildren)