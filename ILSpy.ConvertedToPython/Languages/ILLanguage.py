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
from ICSharpCode.Decompiler import *
from ICSharpCode.Decompiler.Disassembler import *
from Mono.Cecil import *

class ILLanguage(Language):
	""" <summary>
	 IL language support.
	 </summary>
	 <remarks>
	 Currently comes in two versions:
	 flat IL (detectControlStructure=false) and structured IL (detectControlStructure=true).
	 </remarks>
	"""
	def __init__(self, detectControlStructure):
		self._detectControlStructure = detectControlStructure

	def get_Name(self):
		return "IL"

	Name = property(fget=get_Name)

	def get_FileExtension(self):
		return ".il"

	FileExtension = property(fget=get_FileExtension)

	def DecompileMethod(self, method, output, options):
		dis = ReflectionDisassembler(output, self._detectControlStructure, options.CancellationToken)
		dis.DisassembleMethod(method)

	def DecompileField(self, field, output, options):
		dis = ReflectionDisassembler(output, self._detectControlStructure, options.CancellationToken)
		dis.DisassembleField(field)

	def DecompileProperty(self, property, output, options):
		rd = ReflectionDisassembler(output, self._detectControlStructure, options.CancellationToken)
		rd.DisassembleProperty(property)
		if property.GetMethod != None:
			output.WriteLine()
			rd.DisassembleMethod(property.GetMethod)
		if property.SetMethod != None:
			output.WriteLine()
			rd.DisassembleMethod(property.SetMethod)
		enumerator = property.OtherMethods.GetEnumerator()
		while enumerator.MoveNext():
			m = enumerator.Current
			output.WriteLine()
			rd.DisassembleMethod(m)

	def DecompileEvent(self, ev, output, options):
		rd = ReflectionDisassembler(output, self._detectControlStructure, options.CancellationToken)
		rd.DisassembleEvent(ev)
		if ev.AddMethod != None:
			output.WriteLine()
			rd.DisassembleMethod(ev.AddMethod)
		if ev.RemoveMethod != None:
			output.WriteLine()
			rd.DisassembleMethod(ev.RemoveMethod)
		enumerator = ev.OtherMethods.GetEnumerator()
		while enumerator.MoveNext():
			m = enumerator.Current
			output.WriteLine()
			rd.DisassembleMethod(m)

	def DecompileType(self, type, output, options):
		dis = ReflectionDisassembler(output, self._detectControlStructure, options.CancellationToken)
		dis.DisassembleType(type)

	def DecompileNamespace(self, nameSpace, types, output, options):
		ReflectionDisassembler(output, self._detectControlStructure, options.CancellationToken).DisassembleNamespace(nameSpace, types)

	def DecompileAssembly(self, assembly, output, options):
		output.WriteLine("// " + assembly.FileName)
		output.WriteLine()
		rd = ReflectionDisassembler(output, self._detectControlStructure, options.CancellationToken)
		if options.FullDecompilation:
			rd.WriteAssemblyReferences(assembly.ModuleDefinition)
		if assembly.AssemblyDefinition != None:
			rd.WriteAssemblyHeader(assembly.AssemblyDefinition)
		output.WriteLine()
		rd.WriteModuleHeader(assembly.ModuleDefinition)
		if options.FullDecompilation:
			output.WriteLine()
			output.WriteLine()
			rd.WriteModuleContents(assembly.ModuleDefinition)

	def TypeToString(self, t, includeNamespace, attributeProvider):
		output = PlainTextOutput()
		t.WriteTo(output, ILNameSyntax.TypeName if includeNamespace else ILNameSyntax.ShortTypeName)
		return output.ToString()