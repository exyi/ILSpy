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
from System.Collections import *
from System.Collections.Generic import *
from System.Linq import *
from System.Threading import *
from Mono.Cecil import *
from Mono.Cecil.Cil import *

class AnalyzedFieldAccessTreeNode(AnalyzerSearchTreeNode): # true: show writes; false: show read access
	def __init__(self, analyzedField, showWrites):
		self._hashLock = System.Object()
		if analyzedField == None:
			raise ArgumentNullException("analyzedField")
		self._analyzedField = analyzedField
		self._showWrites = showWrites

	def get_Text(self):
		return "Assigned By" if showWrites else "Read By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		self._foundMethods = Lazy[Hashtable](LazyThreadSafetyMode.ExecutionAndPublication)
		analyzer = ScopedWhereUsedAnalyzer[AnalyzerTreeNode](self._analyzedField, FindReferencesInType)
		enumerator = analyzer.PerformAnalysis(ct).OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			child = enumerator.Current
		self._foundMethods = None

	def FindReferencesInType(self, type):
		name = self._analyzedField.Name
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			found = False
			if not method.HasBody:
				continue
			enumerator = method.Body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				instr = enumerator.Current
				if self.CanBeReference(instr.OpCode.Code):
					fr = instr.Operand
					if fr != None and fr.Name == name and Helpers.IsReferencedBy(self._analyzedField.DeclaringType, fr.DeclaringType) and fr.Resolve() == self._analyzedField:
						found = True
						break
			method.Body = None
			if found:
				codeLocation = self._Language.GetOriginalCodeLocation(method)
				if codeLocation != None and not self.HasAlreadyBeenFound(codeLocation):
					node = AnalyzedMethodTreeNode(codeLocation)
					node.Language = self._Language

	def CanBeReference(self, code):
		if code == Code.Ldfld or code == Code.Ldsfld:
			return not self._showWrites
		elif code == Code.Stfld or code == Code.Stsfld:
			return self._showWrites
		elif code == Code.Ldflda or code == Code.Ldsflda:
			return True
		else: # always show address-loading
			return False

	def HasAlreadyBeenFound(self, method):
		hashtable = self._foundMethods.Value