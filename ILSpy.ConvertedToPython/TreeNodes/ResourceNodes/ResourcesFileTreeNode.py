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
from System.Collections import *
from System.Collections.Generic import *
from System.Collections.ObjectModel import *
from System.ComponentModel.Composition import *
from System.IO import *
from System.Linq import *
from System.Resources import *
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.Controls import *
from Mono.Cecil import *

class ResourcesFileTreeNodeFactory(IResourceNodeFactory):
	def CreateNode(self, resource):
		er = resource
		if er != None and er.Name.EndsWith(".resources", StringComparison.OrdinalIgnoreCase):
			return ResourcesFileTreeNode(er)
		return None

	def CreateNode(self, key, data):
		return None

class ResourcesFileTreeNode(ResourceTreeNode):
	def __init__(self, er):
		self._stringTableEntries = ObservableCollection[KeyValuePair]()
		self._otherEntries = ObservableCollection[SerializedObjectRepresentation]()
		self._LazyLoading = True

	def get_Icon(self):
		return Images.ResourceResourcesFile

	Icon = property(fget=get_Icon)

	def LoadChildren(self):
		er = self._Resource
		if er != None:
			s = er.GetResourceStream()
			s.Position = 0
			try:
				reader = ResourceReader(s)
			except ArgumentException, :
				return 
			finally:
			enumerator = reader.Cast().OrderBy().GetEnumerator()
			while enumerator.MoveNext():
				entry = enumerator.Current
				self.ProcessResourceEntry(entry)

	def ProcessResourceEntry(self, entry):
		keyString = entry.Key.ToString()
		if :
			self._stringTableEntries.Add(KeyValuePair[str, str](keyString, entry.Value))
			return 
		if :
			Children.Add(ResourceEntryNode.Create(keyString, MemoryStream(entry.Value)))
			return 
		node = ResourceEntryNode.Create(keyString, entry.Value)
		if node != None:
			Children.Add(node)
			return 
		entryType = entry.Value.GetType().FullName
		if :
			self._otherEntries.Add(SerializedObjectRepresentation(keyString, entryType, (entry.Value).DisplayName))
		else:
			self._otherEntries.Add(SerializedObjectRepresentation(keyString, entryType, entry.Value.ToString()))

	def Decompile(self, language, output, options):
		self.EnsureLazyChildren()
		self.Decompile(language, output, options)
		if self._stringTableEntries.Count != 0:
			smartOutput = output
			if None != smartOutput:
				smartOutput.AddUIElement()
			output.WriteLine()
			output.WriteLine()
		if self._otherEntries.Count != 0:
			smartOutput = output
			if None != smartOutput:
				smartOutput.AddUIElement()
			output.WriteLine()

	class SerializedObjectRepresentation(object):
		def __init__(self, key, type, value):
			self._Key = key
			self._Type = type
			self._Value = value

		def get_Key(self):

		def set_Key(self, value):

		Key = property(fget=get_Key, fset=set_Key)

		def get_Type(self):

		def set_Type(self, value):

		Type = property(fget=get_Type, fset=set_Type)

		def get_Value(self):

		def set_Value(self, value):

		Value = property(fget=get_Value, fset=set_Value)