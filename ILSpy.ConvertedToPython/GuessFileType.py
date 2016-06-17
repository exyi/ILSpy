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
from System.Text import *
from System.Xml import *

class GuessFileType(object):
	""" <summary>
	 Static methods for determining the type of a file.
	 </summary>
	"""
	def DetectFileType(stream):
		if stream.Length >= 2:
			firstByte = stream.ReadByte()
			secondByte = stream.ReadByte() # UTF-16 LE BOM / UTF-32 LE BOM
			if (firstByte << 8) | secondByte == 0xfffe or (firstByte << 8) | secondByte == 0xfeff: # UTF-16 BE BOM
				stream.Position -= 
				reader = StreamReader(stream, detectEncodingFromByteOrderMarks = True)
			elif (firstByte << 8) | secondByte == 0xefbb: # start of UTF-8 BOM
				if stream.ReadByte() == 0xbf:
					reader = StreamReader(stream, Encoding.UTF8)
					break
				else:
					return FileType.Binary
			else:
				if GuessFileType.IsUTF8(stream, firstByte, secondByte):
					stream.Position = 0
					reader = StreamReader(stream, Encoding.UTF8)
					break
				else:
					return FileType.Binary
		else:
			return FileType.Binary
		# Now we got a StreamReader with the correct encoding
		# Check for XML now
		try:
			xmlReader = XmlTextReader(reader)
			xmlReader.XmlResolver = None
			xmlReader.MoveToContent()
			return FileType.Xml
		except XmlException, :
			return FileType.Text
		finally:

	DetectFileType = staticmethod(DetectFileType)

	def IsUTF8(fs, firstByte, secondByte):
		max = Math.Min(fs.Length, 500000) # look at max. 500 KB
		ASCII = 0
		Error = 1
		UTF8 = 2
		UTF8Sequence = 3
		state = ASCII
		sequenceLength = 0
		i = 0
		while i < max:
			if i == 0:
				b = firstByte
			elif i == 1:
				b = secondByte
			else:
				b = fs.ReadByte()
			if b < 0x80:
				# normal ASCII character
				if state == UTF8Sequence:
					state = Error
					break
			elif b < 0xc0:
				# 10xxxxxx : continues UTF8 byte sequence
				if state == UTF8Sequence:
					sequenceLength -= 1
					if sequenceLength < 0:
						state = Error
						break
					elif sequenceLength == 0:
						state = UTF8
				else:
					state = Error
					break
			elif b >= 0xc2 and b < 0xf5:
				# beginning of byte sequence
				if state == UTF8 or state == ASCII:
					state = UTF8Sequence
					if b < 0xe0:
						sequenceLength = 1 # one more byte following
					elif b < 0xf0:
						sequenceLength = 2
					else: # two more bytes following
						sequenceLength = 3
				else: # three more bytes following
					state = Error
					break
			else:
				# 0xc0, 0xc1, 0xf5 to 0xff are invalid in UTF-8 (see RFC 3629)
				state = Error
				break
			i += 1
		return state != Error

	IsUTF8 = staticmethod(IsUTF8)

class FileType(object):
	def __init__(self):