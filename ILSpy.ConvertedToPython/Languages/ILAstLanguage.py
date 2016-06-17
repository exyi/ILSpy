import clr

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
from ICSharpCode.Decompiler import *
from ICSharpCode.Decompiler.Disassembler import *
from ICSharpCode.Decompiler.ILAst import *
from Mono.Cecil import *

class ILAstLanguage(Language):
	""" <summary>
	 Represents the ILAst "language" used for debugging purposes.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Represents the ILAst "language" used for debugging purposes.
		 </summary>
		"""
		self._inlineVariables = True

	def get_Name(self):
		return self._name

	Name = property(fget=get_Name)

	def DecompileMethod(self, method, output, options):
		if not method.HasBody:
			return 
		astBuilder = ILAstBuilder()
		ilMethod = ILBlock()
		context = DecompilerContext(method.ModuleCurrentType = method.DeclaringType, CurrentMethod = method)
		ilMethod.Body = astBuilder.Build(method, self._inlineVariables, context)
		if self._abortBeforeStep != None:
			ILAstOptimizer().Optimize(context, ilMethod, self._abortBeforeStep.Value)
		if context.CurrentMethodIsAsync:
			output.WriteLine("async/await")
		allVariables = ilMethod.GetSelfAndChildrenRecursive().Select().Where().Distinct()
		enumerator = allVariables.GetEnumerator()
		while enumerator.MoveNext():
			v = enumerator.Current
			output.WriteDefinition(v.Name, v)
			if v.Type != None:
				output.Write(" : ")
				if v.IsPinned:
					output.Write("pinned ")
				v.Type.WriteTo(output, ILNameSyntax.ShortTypeName)
			if v.IsGenerated:
				output.Write(" [generated]")
			output.WriteLine()
		output.WriteLine()
		enumerator = ilMethod.Body.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			node.WriteTo(output)
			output.WriteLine()

	def GetDebugLanguages():
		nextName = "ILAst (variable splitting)"
		enumerator = Enum.GetValues(clr.GetClrType(ILAstOptimizationStep)).GetEnumerator()
		while enumerator.MoveNext():
			step = enumerator.Current
			nextName = "ILAst (after " + step + ")"

	GetDebugLanguages = staticmethod(GetDebugLanguages)

	def get_FileExtension(self):
		return ".il"

	FileExtension = property(fget=get_FileExtension)

	def TypeToString(self, t, includeNamespace, attributeProvider):
		output = PlainTextOutput()
		t.WriteTo(output, ILNameSyntax.TypeName if includeNamespace else ILNameSyntax.ShortTypeName)
		return output.ToString()