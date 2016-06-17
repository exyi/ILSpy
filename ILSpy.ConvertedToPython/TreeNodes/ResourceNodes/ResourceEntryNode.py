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
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.TextView import *
from Microsoft.Win32 import *

class ResourceEntryNode(ILSpyTreeNode):
	""" <summary>
	 Entry in a .resources file
	 </summary>
	"""
	def get_Text(self):
		return self._key

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.Resource

	Icon = property(fget=get_Icon)

	def get_Data(self):
		return self._data

	Data = property(fget=get_Data)

	def __init__(self, key, data):
		if key == None:
			raise ArgumentNullException("key")
		if data == None:
			raise ArgumentNullException("data")
		self._key = key
		self._data = data

	def Create(key, data):
		result = None
		enumerator = App.CompositionContainer.GetExportedValues().GetEnumerator()
		while enumerator.MoveNext():
			factory = enumerator.Current
			result = factory.CreateNode(key, data)
			if result != None:
				return result
		streamData = data
		if streamData != None:
			result = ResourceEntryNode(key, data)
		return result

	Create = staticmethod(Create)

	def Decompile(self, language, output, options):
		language.WriteCommentLine(output, str.Format("{0} = {1}", self._key, self._data))

	def Save(self, textView):
		dlg = SaveFileDialog()
		dlg.FileName = Path.GetFileName(DecompilerTextView.CleanUpName(self._key))
		if dlg.ShowDialog() == True:
			self._data.Position = 0
		return True