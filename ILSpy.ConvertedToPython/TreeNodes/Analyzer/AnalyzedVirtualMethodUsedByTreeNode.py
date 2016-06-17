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
from System.Collections.Concurrent import *
from System.Collections.Generic import *
from System.Linq import *
from System.Threading import *
from Mono.Cecil import *
from Mono.Cecil.Cil import *
from ICSharpCode.Decompiler.Ast import *

class AnalyzedVirtualMethodUsedByTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedMethod):
		if analyzedMethod == None:
			raise ArgumentNullException("analyzedMethod")
		self._analyzedMethod = analyzedMethod

	def get_Text(self):
		return "Used By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		self.InitializeAnalyzer()
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedMethod, FindReferencesInType)
		enumerator = analyzer.PerformAnalysis(ct).OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			child = enumerator.Current
		self.ReleaseAnalyzer()

	def InitializeAnalyzer(self):
		self._foundMethods = ConcurrentDictionary[MethodDefinition, int]()
		baseMethods = TypesHierarchyHelpers.FindBaseMethods(self._analyzedMethod).ToArray()
		if baseMethods.Length > 0:
			self._baseMethod = baseMethods[baseMethods.Length - 1]
		else:
			self._baseMethod = self._analyzedMethod
		self._possibleTypes = List[TypeReference]()
		type = self._analyzedMethod.DeclaringType.BaseType
		while type != None:
			self._possibleTypes.Add(type)
			type = type.Resolve().BaseType

	def ReleaseAnalyzer(self):
		self._foundMethods = None
		self._baseMethod = None

	def FindReferencesInType(self, type):
		name = self._analyzedMethod.Name
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			found = False
			prefix = str.Empty
			if not method.HasBody:
				continue
			enumerator = method.Body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				instr = enumerator.Current
				mr = instr.Operand
				if mr != None and mr.Name == name:
					# explicit call to the requested method 
					if instr.OpCode.Code == Code.Call and Helpers.IsReferencedBy(self._analyzedMethod.DeclaringType, mr.DeclaringType) and mr.Resolve() == self._analyzedMethod:
						found = True
						prefix = "(as base) "
						break
					# virtual call to base method
					if instr.OpCode.Code == Code.Callvirt:
						md = mr.Resolve()
						if md == None:
							# cannot resolve the operand, so ignore this method
							break
						if md == self._baseMethod:
							found = True
							break
			method.Body = None
			if found:
				codeLocation = self._Language.GetOriginalCodeLocation(method)
				if codeLocation != None and not self.HasAlreadyBeenFound(codeLocation):
					node = AnalyzedMethodTreeNode(codeLocation)
					node.Language = self._Language

	def HasAlreadyBeenFound(self, method):
		return not self._foundMethods.TryAdd(method, 0)