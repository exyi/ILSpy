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
from System.Windows.Input import *
from ICSharpCode.AvalonEdit.Document import *
from ICSharpCode.AvalonEdit.Rendering import *
from ICSharpCode.ILSpy.TreeNodes.Analyzer import *
from Mono.Cecil import *

class ReferenceElementGenerator(VisualLineElementGenerator):
	""" <summary>
	 Creates hyperlinks in the text view.
	 </summary>
	"""
	# <summary>
	# The collection of references (hyperlinks).
	# </summary>
	def get_References(self):

	def set_References(self, value):

	References = property(fget=get_References, fset=set_References)

	def __init__(self, referenceClicked, isLink):
		if referenceClicked == None:
			raise ArgumentNullException("referenceClicked")
		if isLink == None:
			raise ArgumentNullException("isLink")
		self._referenceClicked = referenceClicked
		self._isLink = isLink

	def GetFirstInterestedOffset(self, startOffset):
		if self.References == None:
			return -1
		# inform AvalonEdit about the next position where we want to build a hyperlink
		segment = self.References.FindFirstSegmentWithStartAfter(startOffset)
		return segment.StartOffset if segment != None else -1

	def ConstructElement(self, offset):
		if self.References == None:
			return None
		enumerator = self.References.FindSegmentsContaining(offset).GetEnumerator()
		while enumerator.MoveNext():
			segment = enumerator.Current
			# skip all non-links
			if not self.isLink(segment):
				continue
			# ensure that hyperlinks don't span several lines (VisualLineElements can't contain line breaks)
			endOffset = Math.Min(segment.EndOffset, CurrentContext.VisualLine.LastDocumentLine.EndOffset)
			# don't create hyperlinks with length 0
			if offset < endOffset:
				return VisualLineReferenceText(CurrentContext.VisualLine, endOffset - offset, self, segment)
		return None

	def JumpToReference(self, referenceSegment, jumpToSource):
		self.referenceClicked(referenceSegment, jumpToSource)

class VisualLineReferenceText(VisualLineText):
	""" <summary>
	 VisualLineElement that represents a piece of text and is a clickable link.
	 </summary>
	"""
	def __init__(self, parentVisualLine, length, parent, referenceSegment):
		""" <summary>
		 Creates a visual line text element with the specified length.
		 It uses the <see cref="ITextRunConstructionContext.VisualLine"/> and its
		 <see cref="VisualLineElement.RelativeTextOffset"/> to find the actual text string.
		 </summary>
		"""
		self._parent = parent
		self._referenceSegment = referenceSegment

	def OnQueryCursor(self, e):
		""" <inheritdoc/>"""
		e.Handled = True
		e.Cursor = Cursors.Arrow if self._referenceSegment.IsLocal else Cursors.Hand

	def OnMouseDown(self, e):
		""" <inheritdoc/>"""
		if e.ChangedButton == MouseButton.Left and not e.Handled:
			self._parent.JumpToReference(self._referenceSegment, (Keyboard.IsKeyDown(Key.LeftCtrl) or Keyboard.IsKeyDown(Key.RightCtrl) or e.ClickCount > 1))
			if not self._referenceSegment.IsLocal:
				e.Handled = True
		elif e.ChangedButton == MouseButton.Right and e.ClickCount > 1 and not e.Handled:
			# open analyze window on double right click
			r = self._referenceSegment.Reference
			if r != None:
				AnalyzeContextMenuEntry.Analyze(r)

	def CreateInstance(self, length):
		""" <inheritdoc/>"""
		return VisualLineReferenceText(ParentVisualLine, length, self._parent, self._referenceSegment)