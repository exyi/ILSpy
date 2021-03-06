﻿# Copyright (c) 2011 AlphaSierraPapa for the SharpDevelop Team
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
from Mono.Cecil import *
from Mono.Cecil.Cil import *

class AnalyzedMethodUsesTreeNode(AnalyzerSearchTreeNode):
	""" <summary>
	 Shows the methods that are used by this method.
	 </summary>
	"""
	def __init__(self, analyzedMethod):
		if analyzedMethod == None:
			raise ArgumentNullException("analyzedMethod")
		self._analyzedMethod = analyzedMethod

	def get_Text(self):
		return "Uses"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		enumerator = self.GetUsedFields().Distinct().GetEnumerator()
		while enumerator.MoveNext():
			f = enumerator.Current
			node = AnalyzedFieldTreeNode(f)
			node.Language = self._Language
		enumerator = self.GetUsedMethods().Distinct().GetEnumerator()
		while enumerator.MoveNext():
			m = enumerator.Current
			node = AnalyzedMethodTreeNode(m)
			node.Language = self._Language

	def GetUsedMethods(self):
		enumerator = self._analyzedMethod.Body.Instructions.GetEnumerator()
		while enumerator.MoveNext():
			instr = enumerator.Current
			mr = instr.Operand
			if mr != None:
				def = mr.Resolve()
				if def != None:

	def GetUsedFields(self):
		enumerator = self._analyzedMethod.Body.Instructions.GetEnumerator()
		while enumerator.MoveNext():
			instr = enumerator.Current
			fr = instr.Operand
			if fr != None:
				def = fr.Resolve()
				if def != None: