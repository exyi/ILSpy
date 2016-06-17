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
from ICSharpCode.Decompiler.ILAst import *
from ICSharpCode.NRefactory.VB import *
from ICSharpCode.NRefactory.VB.Ast import *
from Mono.Cecil import *

class VBTextOutputFormatter(IOutputFormatter):
	""" <summary>
	 Description of VBTextOutputFormatter.
	 </summary>
	"""
	def __init__(self, output):
		self._nodeStack = Stack[AstNode]()
		if output == None:
			raise ArgumentNullException("output")
		self._output = output

	def StartNode(self, node):
		#			var ranges = node.Annotation<List<ILRange>>();
		#			if (ranges != null && ranges.Count > 0)
		#			{
		#				// find the ancestor that has method mapping as annotation
		#				if (node.Ancestors != null && node.Ancestors.Count() > 0)
		#				{
		#					var n = node.Ancestors.FirstOrDefault(a => a.Annotation<MemberMapping>() != null);
		#					if (n != null) {
		#						MemberMapping mapping = n.Annotation<MemberMapping>();
		#
		#						// add all ranges
		#						foreach (var range in ranges) {
		#							mapping.MemberCodeMappings.Add(new SourceCodeMapping {
		#							                               	ILInstructionOffset = range,
		#							                               	SourceCodeLine = output.CurrentLine,
		#							                               	MemberMapping = mapping
		#							                               });
		#						}
		#					}
		#				}
		#			}
		if self._nodeStack.Count == 0:
			if :
				self._firstImport = not ()
				self._lastImport = not ()
			else:
				self._firstImport = False
				self._lastImport = False
		self._nodeStack.Push(node)

	def EndNode(self, node):
		if self._nodeStack.Pop() != node:
			raise InvalidOperationException()

	def WriteIdentifier(self, identifier):
		definition = self.GetCurrentDefinition()
		if definition != None:
			self._output.WriteDefinition(identifier, definition)
			return 
		memberRef = self.GetCurrentMemberReference()
		if memberRef != None:
			self._output.WriteReference(identifier, memberRef)
			return 
		definition = self.GetCurrentLocalDefinition()
		if definition != None:
			self._output.WriteDefinition(identifier, definition)
			return 
		memberRef = self.GetCurrentLocalReference()
		if memberRef != None:
			self._output.WriteReference(identifier, memberRef, True)
			return 
		if self._firstImport:
			self._output.MarkFoldStart(defaultCollapsed = True)
			self._firstImport = False
		self._output.Write(identifier)

	def GetCurrentMemberReference(self):
		node = self._nodeStack.Peek()
		memberRef = node.Annotation()
		if memberRef == None and node.Role == AstNode.Roles.TargetExpression and ( or ):
			memberRef = node.Parent.Annotation()
		return memberRef

	def GetCurrentLocalReference(self):
		node = self._nodeStack.Peek()
		variable = node.Annotation()
		if variable != None:
			if variable.OriginalParameter != None:
				return variable.OriginalParameter
			#if (variable.OriginalVariable != null)
			#    return variable.OriginalVariable;
			return variable
		return None

	def GetCurrentLocalDefinition(self):
		node = self._nodeStack.Peek()
		parameterDef = node.Annotation()
		if parameterDef != None:
			return parameterDef
		if  or  or :
			variable = node.Annotation()
			if variable != None:
				if variable.OriginalParameter != None:
					return variable.OriginalParameter
				#if (variable.OriginalVariable != null)
				#    return variable.OriginalVariable;
				return variable
			else:
		return None

	def GetCurrentDefinition(self):
		if self._nodeStack == None or self._nodeStack.Count == 0:
			return None
		node = self._nodeStack.Peek()
		if self.IsDefinition(node):
			return node.Annotation()
		node = node.Parent
		if self.IsDefinition(node):
			return node.Annotation()
		return None

	def WriteKeyword(self, keyword):
		self._output.Write(keyword)

	def WriteToken(self, token):
		# Attach member reference to token only if there's no identifier in the current node.
		memberRef = self.GetCurrentMemberReference()
		if memberRef != None and self._nodeStack.Peek().GetChildByRole(AstNode.Roles.Identifier).IsNull:
			self._output.WriteReference(token, memberRef)
		else:
			self._output.Write(token)

	def Space(self):
		self._output.Write(' ')

	def Indent(self):
		self._output.Indent()

	def Unindent(self):
		self._output.Unindent()

	def NewLine(self):
		if self._lastImport:
			self._output.MarkFoldEnd()
			self._lastImport = False
		self._output.WriteLine()

	def WriteComment(self, isDocumentation, content):
		if isDocumentation:
			self._output.Write("'''")
		else:
			self._output.Write("'")
		self._output.WriteLine(content)

	def MarkFoldStart(self):
		self._output.MarkFoldStart()

	def MarkFoldEnd(self):
		self._output.MarkFoldEnd()

	def IsDefinition(node):
		return  or  or  or  or  or  or 

	IsDefinition = staticmethod(IsDefinition)