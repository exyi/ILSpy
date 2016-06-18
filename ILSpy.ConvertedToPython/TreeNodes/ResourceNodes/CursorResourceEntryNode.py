﻿# Copyright (c) 2011 AlphaSierraPapa for the SharpDevelop Team
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
from System.ComponentModel.Composition import *
from System.IO import *
from System.Windows.Controls import *
from System.Windows.Media.Imaging import *
from ICSharpCode.ILSpy.TextView import *
from Mono.Cecil import *

class CursorResourceNodeFactory(IResourceNodeFactory):
	def __init__(self):
		self._imageFileExtensions = 

	def CreateNode(self, resource):
		er = resource
		if er != None:
			return self.CreateNode(er.Name, er.GetResourceStream())
		return None

	def CreateNode(self, key, data):
		if not ():
			return None
		enumerator = imageFileExtensions.GetEnumerator()
		while enumerator.MoveNext():
			fileExt = enumerator.Current
			if key.EndsWith(fileExt, StringComparison.OrdinalIgnoreCase):
				return CursorResourceEntryNode(key, data)
		return None

class CursorResourceEntryNode(ResourceEntryNode):
	def __init__(self, key, data):
		pass
	def get_Icon(self):
		return Images.ResourceImage

	Icon = property(fget=get_Icon)

	def View(self, textView):
		try:
			output = AvalonEditTextOutput()
			Data.Position = 0
			image = BitmapImage()
			#HACK: windows imaging does not understand that .cur files have the same layout as .ico
			# so load to data, and modify the ResourceType in the header to make look like an icon...
			s = Data
			if None == s:
				# data was stored in another stream type (e.g. PinnedBufferedMemoryStream)
				s = MemoryStream()
				Data.CopyTo(s)
			curData = s.ToArray()
			curData[2] = 1
			output.AddUIElement()
			output.WriteLine()
			output.AddButton(Images.Save, "Save", )
			textView.ShowNode(output, self)
			return True
		except Exception, :
			return False
		finally: