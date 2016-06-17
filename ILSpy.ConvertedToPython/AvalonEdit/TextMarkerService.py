# Copyright (c) 2014 AlphaSierraPapa for the SharpDevelop Team
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
from System.Windows import *
from System.Windows.Media import *
from System.Windows.Threading import *
from ICSharpCode.AvalonEdit.Document import *
from ICSharpCode.AvalonEdit.Rendering import *
from TextView import *

class TextMarkerService(DocumentColorizingTransformer, IBackgroundRenderer, ITextMarkerService):
	""" <summary>
	 Handles the text markers for a code editor.
	 </summary>
	"""
	def __init__(self, textView):
		if textView == None:
			raise ArgumentNullException("textView")
		self._textView = textView
		textView.DocumentChanged += self.OnDocumentChanged
		self.OnDocumentChanged(None, None)

	def OnDocumentChanged(self, sender, e):
		if self._textView.Document != None:
			self._markers = TextSegmentCollection[TextMarker](self._textView.Document)
		else:
			self._markers = None

	def Create(self, startOffset, length):
		if self._markers == None:
			raise InvalidOperationException("Cannot create a marker when not attached to a document")
		textLength = self._textView.Document.TextLength
		if startOffset < 0 or startOffset > textLength:
			raise ArgumentOutOfRangeException("startOffset", startOffset, "Value must be between 0 and " + textLength)
		if length < 0 or startOffset + length > textLength:
			raise ArgumentOutOfRangeException("length", length, "length must not be negative and startOffset+length must not be after the end of the document")
		m = TextMarker(self, startOffset, length)
		self._markers.Add(m)
		# no need to mark segment for redraw: the text marker is invisible until a property is set
		return m

	def GetMarkersAtOffset(self, offset):
		if self._markers == None:
			return Enumerable.Empty()
		else:
			return self._markers.FindSegmentsContaining(offset)

	def get_TextMarkers(self):
		return self._markers == Enumerable.Empty()

	TextMarkers = property(fget=get_TextMarkers)

	def RemoveAll(self, predicate):
		if predicate == None:
			raise ArgumentNullException("predicate")
		if self._markers != None:
			enumerator = self._markers.ToArray().GetEnumerator()
			while enumerator.MoveNext():
				m = enumerator.Current
				if self.predicate(m):
					self.Remove(m)

	def Remove(self, marker):
		if marker == None:
			raise ArgumentNullException("marker")
		m = marker
		if self._markers != None and self._markers.Remove(m):
			self.Redraw(m)
			m.OnDeleted()

	def Redraw(self, segment):
		""" <summary>
		 Redraws the specified text segment.
		 </summary>
		"""
		self._textView.Redraw(segment, DispatcherPriority.Normal)
		if RedrawRequested != None:
			self.RedrawRequested(self, EventArgs.Empty)

	def ColorizeLine(self, line):
		if self._markers == None:
			return 
		lineStart = line.Offset
		lineEnd = lineStart + line.Length
		enumerator = self._markers.FindOverlappingSegments(lineStart, line.Length).GetEnumerator()
		while enumerator.MoveNext():
			marker = enumerator.Current
			foregroundBrush = None
			if marker.ForegroundColor != None:
				foregroundBrush = SolidColorBrush(marker.ForegroundColor.Value)
				foregroundBrush.Freeze()
			self.ChangeLinePart(Math.Max(marker.StartOffset, lineStart), Math.Min(marker.EndOffset, lineEnd), )

	def get_Layer(self):
		# draw behind selection
		return KnownLayer.Selection

	Layer = property(fget=get_Layer)

	def Draw(self, textView, drawingContext):
		if textView == None:
			raise ArgumentNullException("textView")
		if drawingContext == None:
			raise ArgumentNullException("drawingContext")
		if self._markers == None or not textView.VisualLinesValid:
			return 
		visualLines = textView.VisualLines
		if visualLines.Count == 0:
			return 
		viewStart = visualLines.First().FirstDocumentLine.Offset
		viewEnd = visualLines.Last().LastDocumentLine.EndOffset
		enumerator = self._markers.FindOverlappingSegments(viewStart, viewEnd - viewStart).GetEnumerator()
		while enumerator.MoveNext():
			marker = enumerator.Current
			if marker.BackgroundColor != None:
				geoBuilder = BackgroundGeometryBuilder()
				geoBuilder.AlignToWholePixels = True
				geoBuilder.CornerRadius = 3
				geoBuilder.AddSegment(textView, marker)
				geometry = geoBuilder.CreateGeometry()
				if geometry != None:
					color = marker.BackgroundColor.Value
					brush = SolidColorBrush(color)
					brush.Freeze()
					drawingContext.DrawGeometry(brush, None, geometry)
			underlineMarkerTypes = TextMarkerTypes.SquigglyUnderline | TextMarkerTypes.NormalUnderline | TextMarkerTypes.DottedUnderline
			if (marker.MarkerTypes & underlineMarkerTypes) != 0:
				enumerator = BackgroundGeometryBuilder.GetRectsForSegment(textView, marker).GetEnumerator()
				while enumerator.MoveNext():
					r = enumerator.Current
					startPoint = r.BottomLeft
					endPoint = r.BottomRight
					usedBrush = SolidColorBrush(marker.MarkerColor)
					usedBrush.Freeze()
					if (marker.MarkerTypes & TextMarkerTypes.SquigglyUnderline) != 0:
						offset = 2.5
						count = Math.Max(((endPoint.X - startPoint.X) / offset) + 1, 4)
						geometry = StreamGeometry()
						geometry.Freeze()
						usedPen = Pen(usedBrush, 1)
						usedPen.Freeze()
						drawingContext.DrawGeometry(Brushes.Transparent, usedPen, geometry)
					if (marker.MarkerTypes & TextMarkerTypes.NormalUnderline) != 0:
						usedPen = Pen(usedBrush, 1)
						usedPen.Freeze()
						drawingContext.DrawLine(usedPen, startPoint, endPoint)
					if (marker.MarkerTypes & TextMarkerTypes.DottedUnderline) != 0:
						usedPen = Pen(usedBrush, 1)
						usedPen.DashStyle = DashStyles.Dot
						usedPen.Freeze()
						drawingContext.DrawLine(usedPen, startPoint, endPoint)

	def CreatePoints(self, start, end, offset, count):
		i = 0
		while i < count:
			i += 1

class TextMarker(TextSegment, ITextMarker):
	def __init__(self, service, startOffset, length):
		if service == None:
			raise ArgumentNullException("service")
		self._service = service
		self._StartOffset = startOffset
		self._Length = length
		self._markerTypes = TextMarkerTypes.None

	def get_IsDeleted(self):
		return not self._IsConnectedToCollection

	IsDeleted = property(fget=get_IsDeleted)

	def Delete(self):
		self._service.Remove(self)

	def OnDeleted(self):
		if Deleted != None:
			self.Deleted(self, EventArgs.Empty)

	def Redraw(self):
		self._service.Redraw(self)

	def get_BackgroundColor(self):
		return self._backgroundColor

	def set_BackgroundColor(self, value):
		if self._backgroundColor != value:
			self._backgroundColor = value
			self.Redraw()

	BackgroundColor = property(fget=get_BackgroundColor, fset=set_BackgroundColor)

	def get_ForegroundColor(self):
		return self._foregroundColor

	def set_ForegroundColor(self, value):
		if self._foregroundColor != value:
			self._foregroundColor = value
			self.Redraw()

	ForegroundColor = property(fget=get_ForegroundColor, fset=set_ForegroundColor)

	def get_FontWeight(self):
		return self._fontWeight

	def set_FontWeight(self, value):
		if self._fontWeight != value:
			self._fontWeight = value
			self.Redraw()

	FontWeight = property(fget=get_FontWeight, fset=set_FontWeight)

	def get_FontStyle(self):
		return self._fontStyle

	def set_FontStyle(self, value):
		if self._fontStyle != value:
			self._fontStyle = value
			self.Redraw()

	FontStyle = property(fget=get_FontStyle, fset=set_FontStyle)

	def get_Tag(self):

	def set_Tag(self, value):

	Tag = property(fget=get_Tag, fset=set_Tag)

	def get_MarkerTypes(self):
		return self._markerTypes

	def set_MarkerTypes(self, value):
		if self._markerTypes != value:
			self._markerTypes = value
			self.Redraw()

	MarkerTypes = property(fget=get_MarkerTypes, fset=set_MarkerTypes)

	def get_MarkerColor(self):
		return self._markerColor

	def set_MarkerColor(self, value):
		if self._markerColor != value:
			self._markerColor = value
			self.Redraw()

	MarkerColor = property(fget=get_MarkerColor, fset=set_MarkerColor)

	def get_ToolTip(self):

	def set_ToolTip(self, value):

	ToolTip = property(fget=get_ToolTip, fset=set_ToolTip)