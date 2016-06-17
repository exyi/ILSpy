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
from ICSharpCode.Decompiler.Ast import *
from Mono.Cecil import *

class AnalyzedMethodOverridesTreeNode(AnalyzerSearchTreeNode):
	""" <summary>
	 Searches for overrides of the analyzed method.
	 </summary>
	"""
	def __init__(self, analyzedMethod):
		if analyzedMethod == None:
			raise ArgumentNullException("analyzedMethod")
		self._analyzedMethod = analyzedMethod

	def get_Text(self):
		return "Overridden By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedMethod, FindReferencesInType)
		return analyzer.PerformAnalysis(ct).OrderBy()

	def FindReferencesInType(self, type):
		newNode = None
		try:
			if not TypesHierarchyHelpers.IsBaseType(self._analyzedMethod.DeclaringType, type, resolveTypeArguments = False):
			enumerator = type.Methods.GetEnumerator()
			while enumerator.MoveNext():
				method = enumerator.Current
				if TypesHierarchyHelpers.IsBaseMethod(self._analyzedMethod, method):
					hidesParent = not method.IsVirtual ^ method.IsNewSlot
					newNode = AnalyzedMethodTreeNode(method, "(hides) " if hidesParent else "")
		except ReferenceResolvingException, :
		finally:
		# ignore this type definition. maybe add a notification about such cases.
		if newNode != None:
			newNode.Language = self._Language

	def CanShow(method):
		return method.IsVirtual and not method.IsFinal and not method.DeclaringType.IsSealed and not method.DeclaringType.IsInterface

	CanShow = staticmethod(CanShow)