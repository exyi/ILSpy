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
from System.Diagnostics import *
from System.Linq import *
from System.Text import *
from System.Windows import *
from ICSharpCode.AvalonEdit.Document import *
from ICSharpCode.AvalonEdit.Folding import *
from ICSharpCode.AvalonEdit.Rendering import *
from ICSharpCode.Decompiler import *

class ReferenceSegment(TextSegment):
	""" <summary>
	 A text segment that references some object. Used for hyperlinks in the editor.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 A text segment that references some object. Used for hyperlinks in the editor.
		 </summary>
		"""

class DefinitionLookup(object):
	""" <summary>
	 Stores the positions of the definitions that were written to the text output.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Stores the positions of the definitions that were written to the text output.
		 </summary>
		"""
		self._definitions = Dictionary[Object, int]()

	def GetDefinitionPosition(self, definition):
		if self._definitions.TryGetValue(definition, ):
			return val
		else:
			return -1

	def AddDefinition(self, definition, offset):
		self._definitions[definition] = offset

class AvalonEditTextOutput(ISmartTextOutput):
	""" <summary>
	 Text output implementation for AvalonEdit.
	 </summary>
	"""
	# <summary>Current indentation level</summary>
	# <summary>Whether indentation should be inserted on the next write</summary>
	# <summary>List of all references that were written to the output</summary>
	# <summary>Stack of the fold markers that are open but not closed yet</summary>
	# <summary>List of all foldings that were written to the output</summary>
	# <summary>Embedded UIElements, see <see cref="UIElementGenerator"/>.</summary>
	def __init__(self):
		self._lastLineStart = 0
		self._lineNumber = 1
		self._b = StringBuilder()
		self._elementGenerators = List[VisualLineElementGenerator]()
		self._references = TextSegmentCollection[ReferenceSegment]()
		self._openFoldings = Stack[NewFolding]()
		self._Foldings = List[NewFolding]()
		self._DefinitionLookup = DefinitionLookup()
		self._UIElements = List[KeyValuePair]()
		self._DebuggerMemberMappings = List[MethodDebugSymbols]()
		# <summary>
		# Gets the list of references (hyperlinks).
		# </summary>
		# <summary>
		# Controls the maximum length of the text.
		# When this length is exceeded, an <see cref="OutputLengthExceededException"/> will be thrown,
		# thus aborting the decompilation.
		# </summary>
		self._LengthLimit = int.MaxValue

	def get_References(self):
		return self._references

	References = property(fget=get_References)

	def AddVisualLineElementGenerator(self, elementGenerator):
		self._elementGenerators.Add(elementGenerator)

	def get_TextLength(self):
		return self._b.Length

	TextLength = property(fget=get_TextLength)

	def get_Location(self):
		return ICSharpCode.NRefactory.TextLocation(self._lineNumber, self._b.Length - self._lastLineStart + 1 + (self._indent if self._needsIndent else 0))

	Location = property(fget=get_Location)

	def PrepareDocument(self):
		""" <summary>
		 Prepares the TextDocument.
		 This method may be called by the background thread writing to the output.
		 Once the document is prepared, it can no longer be written to.
		 </summary>
		 <remarks>
		 Calling this method on the background thread ensures the TextDocument's line tokenization
		 runs in the background and does not block the GUI.
		 </remarks>
		"""
		if self._textDocument == None:
			self._textDocument = TextDocument(self._b.ToString())
			self._textDocument.SetOwnerThread(None)
 # release ownership
	def GetDocument(self):
		""" <summary>
		 Retrieves the TextDocument.
		 Once the document is retrieved, it can no longer be written to.
		 </summary>
		"""
		self.PrepareDocument()
		self._textDocument.SetOwnerThread(System.Threading.Thread.CurrentThread) # acquire ownership
		return self._textDocument

	def Indent(self):
		self._indent += 1

	def Unindent(self):
		self._indent -= 1

	def WriteIndent(self):
		Debug.Assert(self._textDocument == None)
		if self._needsIndent:
			self._needsIndent = False
			i = 0
			while i < self._indent:
				self._b.Append('\t')
				i += 1

	def Write(self, ch):
		self.WriteIndent()
		self._b.Append(ch)

	def Write(self, text):
		self.WriteIndent()
		self._b.Append(text)

	def WriteLine(self):
		Debug.Assert(self._textDocument == None)
		self._b.AppendLine()
		self._needsIndent = True
		self._lastLineStart = self._b.Length
		self._lineNumber += 1
		if self.TextLength > self._LengthLimit:
			raise OutputLengthExceededException()

	def WriteDefinition(self, text, definition, isLocal):
		self.WriteIndent()
		start = self.TextLength
		self._b.Append(text)
		end = self.TextLength
		self._DefinitionLookup.AddDefinition(definition, self.TextLength)
		self._references.Add(ReferenceSegment(StartOffset = start, EndOffset = end, Reference = definition, IsLocal = isLocal, IsLocalTarget = True))

	def WriteReference(self, text, reference, isLocal):
		self.WriteIndent()
		start = self.TextLength
		self._b.Append(text)
		end = self.TextLength
		self._references.Add(ReferenceSegment(StartOffset = start, EndOffset = end, Reference = reference, IsLocal = isLocal))

	def MarkFoldStart(self, collapsedText, defaultCollapsed):
		self.WriteIndent()
		self._openFoldings.Push(NewFolding(StartOffset = self.TextLength, Name = collapsedText, DefaultClosed = defaultCollapsed))

	def MarkFoldEnd(self):
		f = self._openFoldings.Pop()
		f.EndOffset = self.TextLength
		self._Foldings.Add(f)

	def AddUIElement(self, element):
		if element != None:
			if self._UIElements.Count > 0 and self._UIElements.Last().Key == self.TextLength:
				raise InvalidOperationException("Only one UIElement is allowed for each position in the document")
			self._UIElements.Add(KeyValuePair[int, Lazy](self.TextLength, Lazy[UIElement](element)))

	def AddDebugSymbols(self, methodDebugSymbols):
		self._DebuggerMemberMappings.Add(methodDebugSymbols)