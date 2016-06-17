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
from ICSharpCode.Decompiler import *
from ICSharpCode.Decompiler.ILAst import *
from ICSharpCode.NRefactory.CSharp import *
from Mono.Cecil import *

class DecompileEventArgs(EventArgs):
	# <summary>
	# Decompilation event arguments.
	# </summary>
	# <summary>
	# Gets or sets the local variables.
	# </summary>
	def get_LocalVariables(self):

	def set_LocalVariables(self, value):

	LocalVariables = property(fget=get_LocalVariables, fset=set_LocalVariables)

	# <summary>
	# Gets the list of MembeReferences that are decompiled (TypeDefinitions, MethodDefinitions, etc)
	# </summary>
	def get_DecompiledMemberReferences(self):

	def set_DecompiledMemberReferences(self, value):

	DecompiledMemberReferences = property(fget=get_DecompiledMemberReferences, fset=set_DecompiledMemberReferences)

	# <summary>
	# Gets (or internal sets) the AST nodes.
	# </summary>
	def get_AstNodes(self):

	def set_AstNodes(self, value):

	AstNodes = property(fget=get_AstNodes, fset=set_AstNodes)