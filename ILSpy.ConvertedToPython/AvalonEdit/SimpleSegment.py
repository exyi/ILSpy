from ICSharpCode.AvalonEdit.Document import *
from System import *
from System.Collections.Generic import *
from System.Diagnostics import *
from System.Globalization import *
from System.Linq import *
from System.Text import *

class SimpleSegment(IEquatable, ISegment):
	""" <summary>
	 Represents a simple segment (Offset,Length pair) that is not automatically updated
	 on document changes.
	 </summary>
	"""
	def GetOverlap(segment1, segment2):
		""" <summary>
		 Gets the overlapping portion of the segments.
		 Returns SimpleSegment.Invalid if the segments don't overlap.
		 </summary>
		"""
		start = Math.Max(segment1.Offset, segment2.Offset)
		end = Math.Min(segment1.EndOffset, segment2.EndOffset)
		if end < start:
			return SimpleSegment.Invalid
		else:
			return SimpleSegment(start, end - start)

	GetOverlap = staticmethod(GetOverlap)

	def get_Offset(self):
		return self._Offset

	Offset = property(fget=get_Offset)

	def get_Length(self):
		return self._Length

	Length = property(fget=get_Length)

	def get_EndOffset(self):
		return self._Offset + self._Length

	EndOffset = property(fget=get_EndOffset)

	def __init__(self, segment):
		self._Invalid = SimpleSegment(-1, -1)
		Debug.Assert(segment != None)
		self.Offset = segment.Offset
		self.Length = segment.Length

	def __init__(self, segment):
		self._Invalid = SimpleSegment(-1, -1)
		Debug.Assert(segment != None)
		self.Offset = segment.Offset
		self.Length = segment.Length

	def GetHashCode(self):

	def Equals(self, obj):
		return () and self.Equals(obj)

	def Equals(self, other):
		return self.Offset == other.Offset and self.Length == other.Length

	def ToString(self):
		""" <inheritdoc/>"""
		return "[Offset=" + self._Offset.ToString(CultureInfo.InvariantCulture) + ", Length=" + self._Length.ToString(CultureInfo.InvariantCulture) + "]"