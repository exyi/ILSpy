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
from System.Threading.Tasks import *
from ICSharpCode.AvalonEdit.Highlighting import *
from ICSharpCode.ILSpy.TextView import *
from ICSharpCode.ILSpy.TreeNodes import *
from Mono.Cecil import *

class XmlResourceNodeFactory(IResourceNodeFactory):
	def __init__(self):
		self._xmlFileExtensions = 

	def CreateNode(self, resource):
		er = resource
		if er != None:
			return self.CreateNode(er.Name, er.GetResourceStream())
		return None

	def CreateNode(self, key, data):
		if not ():
			return None
		enumerator = xmlFileExtensions.GetEnumerator()
		while enumerator.MoveNext():
			fileExt = enumerator.Current
			if key.EndsWith(fileExt, StringComparison.OrdinalIgnoreCase):
				return XmlResourceEntryNode(key, data)
		return None

class XmlResourceEntryNode(ResourceEntryNode):
	def __init__(self, key, data):

	def get_Icon(self):
		text = Text
		if text.EndsWith(".xml", StringComparison.OrdinalIgnoreCase):
			return Images.ResourceXml
		elif text.EndsWith(".xsd", StringComparison.OrdinalIgnoreCase):
			return Images.ResourceXsd
		elif text.EndsWith(".xslt", StringComparison.OrdinalIgnoreCase):
			return Images.ResourceXslt
		else:
			return Images.Resource

	Icon = property(fget=get_Icon)

	def View(self, textView):
		output = AvalonEditTextOutput()
		highlighting = None
				# cache read XAML because stream will be closed after first read
textView.RunWithCancellation().Then().HandleExceptions()
		return True