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
from System.ComponentModel import *
from System.ComponentModel.Composition import *
from System.Diagnostics import *
from System.IO import *
from System.Linq import *
from System.Threading import *
from System.Threading.Tasks import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Data import *
from System.Windows.Input import *
from System.Windows.Media import *
from System.Windows.Media.Animation import *
from System.Windows.Threading import *
from System.Xml import *
from ICSharpCode.AvalonEdit import *
from ICSharpCode.AvalonEdit.Document import *
from ICSharpCode.AvalonEdit.Editing import *
from ICSharpCode.AvalonEdit.Folding import *
from ICSharpCode.AvalonEdit.Highlighting import *
from ICSharpCode.AvalonEdit.Highlighting.Xshd import *
from ICSharpCode.AvalonEdit.Rendering import *
from ICSharpCode.AvalonEdit.Search import *
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.AvalonEdit import *
from ICSharpCode.ILSpy.Options import *
from ICSharpCode.ILSpy.TreeNodes import *
from ICSharpCode.ILSpy.XmlDoc import *
from ICSharpCode.NRefactory.Documentation import *
from Microsoft.Win32 import *
from Mono.Cecil import *
from ICSharpCode.Decompiler.ILAst import *
from ICSharpCode.Decompiler.Ast import *

class DecompilerTextView(UserControl, IDisposable):
	# <summary>
	# Manages the TextEditor showing the decompiled code.
	# Contains all the threading logic that makes the decompiler work in the background.
	# </summary>
	def __init__(self, Reference):
		self._activeCustomElementGenerators = List[VisualLineElementGenerator]()
		self._localReferenceMarks = List[ITextMarker]()
		# SearchPanel
		# Bookmarks context menu
		# add marker service & margin
		# lenghten containing spans
		self._renaming = False

	def Document_TextChanged(self, sender, e):
		self._references.UpdateOffsets(e)
		if e.RemovalLength == 0:
			enumerator = self._references.FindSegmentsContaining(e.Offset).GetEnumerator()
			while enumerator.MoveNext():
				containingSegment = enumerator.Current
				if containingSegment.EndOffset == e.Offset:
					containingSegment.Length += e.InsertionLength
			enumerator = self._references.FindSegmentsContaining(e.Offset + e.InsertionLength).GetEnumerator()
			while enumerator.MoveNext():
				containingSegment = enumerator.Current
				if containingSegment.StartOffset == e.Offset + e.InsertionLength:
					containingSegment.StartOffset -= e.InsertionLength
					containingSegment.Length += e.InsertionLength
		if not self._renaming:
			Dispatcher.BeginInvoke(Action())

	def TextArea_TextEntering(self, sender, e):
		if not e.Text.All():
			e.Handled = True
			return 
		r = self._references.FindSegmentsContaining(textEditor.CaretOffset).SingleOrDefault()
		if r == None or not r.IsLocal:
			e.Handled = True

	def RenameReference(self, e):
		if self._renaming:
			return 
		self.RenameReference(e.Offset, e.RemovalLength, e.InsertedText.Text)

	def RenameReference(self, offset, removeLen, insert):
		if self._renaming:
			return 
		r = self._references.FindSegmentsContaining(offset).Where().SingleOrDefault()
		if r != None:
			self.RenameReference(r, textEditor.Document.GetText(r))

	def RenameReference(self, segment, newName):
		if self._renaming:
			return 
		try:
			self._renaming = True
			enumerator = references.GetEnumerator()
			while enumerator.MoveNext():
				r = enumerator.Current
				if r.Reference.Equals(segment.Reference) and r != segment:
					textEditor.Document.Replace(r, newName)
		finally:
			self._renaming = False
		v = segment.Reference
		if v != None:
			method =  if self._decompiledNodes.SelectMany().FirstOrDefault( if .Body else ).Variables else 

	def __init__(self, Reference):
		self._activeCustomElementGenerators = List[VisualLineElementGenerator]()
		self._localReferenceMarks = List[ITextMarker]()
		self._renaming = False