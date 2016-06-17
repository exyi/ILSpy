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
from System.ComponentModel.Composition import *
from System.IO import *
from System.Windows.Controls import *
from System.Windows.Media.Imaging import *
from ICSharpCode.ILSpy.TextView import *
from Mono.Cecil import *

class IconResourceNodeFactory(IResourceNodeFactory):
	def CreateNode(self, resource):
		er = resource
		if er != None:
			return self.CreateNode(er.Name, er.GetResourceStream())
		return None

	def CreateNode(self, key, data):
		if :
			s = MemoryStream()
			(data).Save(s)
			return IconResourceEntryNode(key, s)
		if  and key.EndsWith(".ico", StringComparison.OrdinalIgnoreCase):
			return IconResourceEntryNode(key, data)
		return None

class IconResourceEntryNode(ResourceEntryNode):
	def __init__(self, key, data):
		pass
	def get_Icon(self):
		return Images.ResourceImage

	Icon = property(fget=get_Icon)

	def View(self, textView):
		try:
			output = AvalonEditTextOutput()
			Data.Position = 0
			decoder = IconBitmapDecoder(Data, BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.None)
			enumerator = decoder.Frames.GetEnumerator()
			while enumerator.MoveNext():
				frame = enumerator.Current
				output.Write(String.Format("{0}x{1}, {2} bit: ", frame.PixelHeight, frame.PixelWidth, frame.Thumbnail.Format.BitsPerPixel))
				self.AddIcon(output, frame)
				output.WriteLine()
			output.AddButton(Images.Save, "Save", )
			textView.ShowNode(output, self)
			return True
		except Exception, :
			return False
		finally:

	def AddIcon(output, frame):
		output.AddUIElement()

	AddIcon = staticmethod(AddIcon)