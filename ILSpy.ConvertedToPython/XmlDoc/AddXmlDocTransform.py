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
from System.IO import *
from ICSharpCode.NRefactory.CSharp import *
from Mono.Cecil import *

class AddXmlDocTransform(object):
	""" <summary>
	 Adds XML documentation for member definitions.
	 </summary>
	"""
	def Run(node):
		if :
			mr = node.Annotation()
			if mr != None and mr.Module != None:
				xmldoc = XmlDocLoader.LoadDocumentation(mr.Module)
				if xmldoc != None:
					doc = xmldoc.GetDocumentation(XmlDocKeyProvider.GetKey(mr))
					if doc != None:
						AddXmlDocTransform.InsertXmlDocumentation(node, StringReader(doc))
			if not ():
				return  # don't recurse into attributed nodes, except for type definitions
		enumerator = node.Children.GetEnumerator()
		while enumerator.MoveNext():
			child = enumerator.Current
			AddXmlDocTransform.Run(child)

	Run = staticmethod(Run)

	def InsertXmlDocumentation(node, r):
		# Find the first non-empty line:
		while str.IsNullOrWhiteSpace(firstLine):
			firstLine = r.ReadLine()
			if firstLine == None:
				return 
		indentation = firstLine.Substring(0, firstLine.Length - firstLine.TrimStart().Length)
		line = firstLine
		skippedWhitespaceLines = 0
		# Copy all lines from input to output, except for empty lines at the end.
		while line != None:
			if str.IsNullOrWhiteSpace(line):
				skippedWhitespaceLines += 1
			else:
				while skippedWhitespaceLines > 0:
					node.Parent.InsertChildBefore(node, Comment(str.Empty, CommentType.Documentation), Roles.Comment)
					skippedWhitespaceLines -= 1
				if line.StartsWith(indentation, StringComparison.Ordinal):
					line = line.Substring(indentation.Length)
				node.Parent.InsertChildBefore(node, Comment(" " + line, CommentType.Documentation), Roles.Comment)
			line = r.ReadLine()

	InsertXmlDocumentation = staticmethod(InsertXmlDocumentation)