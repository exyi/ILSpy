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

class AnalyzedMethodUsedByTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedMethod):
		if analyzedMethod == None:
			raise ArgumentNullException("analyzedMethod")
		self._analyzedMethod = analyzedMethod

	def get_Text(self):
		return "Used By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		self._foundMethods = ConcurrentDictionary[MethodDefinition, int]()
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedMethod, FindReferencesInType)
		enumerator = analyzer.PerformAnalysis(ct).OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			child = enumerator.Current
		self._foundMethods = None

	def FindReferencesInType(self, type):
		name = self._analyzedMethod.Name
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			found = False
			if not method.HasBody:
				continue
			enumerator = method.Body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				instr = enumerator.Current
				mr = instr.Operand
				if mr != None and mr.Name == name and Helpers.IsReferencedBy(self._analyzedMethod.DeclaringType, mr.DeclaringType) and mr.Resolve() == self._analyzedMethod:
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