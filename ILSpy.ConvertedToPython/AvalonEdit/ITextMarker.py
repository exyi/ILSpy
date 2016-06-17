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
from System.Windows import *
from System.Windows.Media import *

class ITextMarker(object):
	""" <summary>
	 Represents a text marker.
	 </summary>
	"""
	# <summary>
	# Gets the start offset of the marked text region.
	# </summary>
	def get_StartOffset(self):

	StartOffset = property(fget=get_StartOffset)

	# <summary>
	# Gets the end offset of the marked text region.
	# </summary>
	def get_EndOffset(self):

	EndOffset = property(fget=get_EndOffset)

	# <summary>
	# Gets the length of the marked region.
	# </summary>
	def get_Length(self):

	Length = property(fget=get_Length)

	def Delete(self):
		""" <summary>
		 Deletes the text marker.
		 </summary>
		"""
		pass

	# <summary>
	# Gets whether the text marker was deleted.
	# </summary>
	def get_IsDeleted(self):

	IsDeleted = property(fget=get_IsDeleted)

	# <summary>
	# Event that occurs when the text marker is deleted.
	# </summary>
	# <summary>
	# Gets/Sets the background color.
	# </summary>
	def get_BackgroundColor(self):

	def set_BackgroundColor(self, value):

	BackgroundColor = property(fget=get_BackgroundColor, fset=set_BackgroundColor)

	# <summary>
	# Gets/Sets the foreground color.
	# </summary>
	def get_ForegroundColor(self):

	def set_ForegroundColor(self, value):

	ForegroundColor = property(fget=get_ForegroundColor, fset=set_ForegroundColor)

	# <summary>
	# Gets/Sets the font weight.
	# </summary>
	def get_FontWeight(self):

	def set_FontWeight(self, value):

	FontWeight = property(fget=get_FontWeight, fset=set_FontWeight)

	# <summary>
	# Gets/Sets the font style.
	# </summary>
	def get_FontStyle(self):

	def set_FontStyle(self, value):

	FontStyle = property(fget=get_FontStyle, fset=set_FontStyle)

	# <summary>
	# Gets/Sets the type of the marker. Use TextMarkerType.None for normal markers.
	# </summary>
	def get_MarkerTypes(self):

	def set_MarkerTypes(self, value):

	MarkerTypes = property(fget=get_MarkerTypes, fset=set_MarkerTypes)

	# <summary>
	# Gets/Sets the color of the marker.
	# </summary>
	def get_MarkerColor(self):

	def set_MarkerColor(self, value):

	MarkerColor = property(fget=get_MarkerColor, fset=set_MarkerColor)

	# <summary>
	# Gets/Sets an object with additional data for this text marker.
	# </summary>
	def get_Tag(self):

	def set_Tag(self, value):

	Tag = property(fget=get_Tag, fset=set_Tag)

	# <summary>
	# Gets/Sets an object that will be displayed as tooltip in the text editor.
	# </summary>
	def get_ToolTip(self):

	def set_ToolTip(self, value):

	ToolTip = property(fget=get_ToolTip, fset=set_ToolTip)

class TextMarkerTypes(object):
	def __init__(self):
		self._None = 		# <summary>
		# Use no marker
		# </summary>
0x0000
		self._SquigglyUnderline = 		# <summary>
		# Use squiggly underline marker
		# </summary>
0x001
		self._NormalUnderline = 		# <summary>
		# Normal underline.
		# </summary>
0x002
		self._DottedUnderline = 		# <summary>
		# Dotted underline.
		# </summary>
0x004
		self._LineInScrollBar = 		# <summary>
		# Horizontal line in the scroll bar.
		# </summary>
0x0100
		self._ScrollBarRightTriangle = 		# <summary>
		# Small triangle in the scroll bar, pointing to the right.
		# </summary>
0x0400
		self._ScrollBarLeftTriangle = 		# <summary>
		# Small triangle in the scroll bar, pointing to the left.
		# </summary>
0x0800
		self._CircleInScrollBar = 		# <summary>
		# Small circle in the scroll bar.
		# </summary>
0x1000

class ITextMarkerService(object):
	def Create(self, startOffset, length):
		""" <summary>
		 Creates a new text marker. The text marker will be invisible at first,
		 you need to set one of the Color properties to make it visible.
		 </summary>
		"""
		pass

	# <summary>
	# Gets the list of text markers.
	# </summary>
	def get_TextMarkers(self):

	TextMarkers = property(fget=get_TextMarkers)

	def Remove(self, marker):
		""" <summary>
		 Removes the specified text marker.
		 </summary>
		"""
		pass

	def RemoveAll(self, predicate):
		""" <summary>
		 Removes all text markers that match the condition.
		 </summary>
		"""
		pass

	def GetMarkersAtOffset(self, offset):
		""" <summary>
		 Finds all text markers at the specified offset.
		 </summary>
		"""
		pass