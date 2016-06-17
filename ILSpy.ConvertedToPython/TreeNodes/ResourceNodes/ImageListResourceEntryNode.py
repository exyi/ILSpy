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
from System.ComponentModel.Composition import *
from System.Drawing import *
from System.Linq import *
from System.Text import *
from System.Windows.Forms import *
from ICSharpCode.Decompiler import *

class ImageListResourceEntryNodeFactory(IResourceNodeFactory):
	def CreateNode(self, resource):
		return None

	def CreateNode(self, key, data):
		if :
			return ImageListResourceEntryNode(key, data)
		return None

class ImageListResourceEntryNode(ILSpyTreeNode):
	def __init__(self, key, data):
		self._LazyLoading = True
		self._key = key
		self._data = ImageList()
		self._data.ImageStream = data

	def get_Text(self):
		return key

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.ResourceImage

	Icon = property(fget=get_Icon)

	def LoadChildren(self):
		i = 0
		enumerator = self._data.Images.GetEnumerator()
		while enumerator.MoveNext():
			image = enumerator.Current
			node = ResourceEntryNode.Create("Image" + i.ToString(), image)
			if node != None:
				Children.Add(node)
			i += 1

	def Decompile(self, language, output, options):
		self.EnsureLazyChildren()