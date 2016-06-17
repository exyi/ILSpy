import clr

			import clr

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
from System.ComponentModel import *
from System.Globalization import *
from System.Linq import *
from System.Text import *
from System.Text.RegularExpressions import *
from System.Windows import *
from System.Xml.Linq import *

class SessionSettings(INotifyPropertyChanged):
	""" <summary>
	 Per-session setting:
	 Loaded at startup; saved at exit.
	 </summary>
	"""
	def __init__(self, spySettings):
		self._WindowState = WindowState.Normal
		self._DefaultWindowBounds = Rect(10, 10, 750, 550)
		# <summary>
		# position of the left/right splitter
		# </summary>
		self._regex = Regex("\\\\x(?<num>[0-9A-f]{4})")
		doc = spySettings["SessionSettings"]
		filterSettings = doc.Element("FilterSettings")
		if filterSettings == None:
			filterSettings = XElement("FilterSettings")
		self._FilterSettings = FilterSettings(filterSettings)
		self._ActiveAssemblyList = doc.Element("ActiveAssemblyList")
		activeTreeViewPath = doc.Element("ActiveTreeViewPath")
		if activeTreeViewPath != None:
			self._ActiveTreeViewPath = activeTreeViewPath.Elements().Select().ToArray()
		self._ActiveAutoLoadedAssembly = doc.Element("ActiveAutoLoadedAssembly")
		self._WindowState = self.FromString(doc.Element("WindowState"), self._WindowState.Normal)
		self._WindowBounds = self.FromString(doc.Element("WindowBounds"), self._DefaultWindowBounds)
		self._SplitterPosition = self.FromString(doc.Element("SplitterPosition"), 0.4)
		self._TopPaneSplitterPosition = self.FromString(doc.Element("TopPaneSplitterPosition"), 0.3)
		self._BottomPaneSplitterPosition = self.FromString(doc.Element("BottomPaneSplitterPosition"), 0.3)

	def OnPropertyChanged(self, propertyName):
		if PropertyChanged != None:
			self.PropertyChanged(self, PropertyChangedEventArgs(propertyName))

	def get_FilterSettings(self):

	def set_FilterSettings(self, value):

	FilterSettings = property(fget=get_FilterSettings, fset=set_FilterSettings)

	def Save(self):
		doc = XElement("SessionSettings")
		doc.Add(self.FilterSettings.SaveAsXml())
		if self._ActiveAssemblyList != None:
			doc.Add(XElement("ActiveAssemblyList", self._ActiveAssemblyList))
		if self._ActiveTreeViewPath != None:
			doc.Add(XElement("ActiveTreeViewPath", self._ActiveTreeViewPath.Select()))
		if self._ActiveAutoLoadedAssembly != None:
			doc.Add(XElement("ActiveAutoLoadedAssembly", self._ActiveAutoLoadedAssembly))
		doc.Add(XElement("WindowState", self.ToString(self._WindowState)))
		doc.Add(XElement("WindowBounds", self.ToString(self._WindowBounds)))
		doc.Add(XElement("SplitterPosition", self.ToString(self._SplitterPosition)))
		doc.Add(XElement("TopPaneSplitterPosition", self.ToString(self._TopPaneSplitterPosition)))
		doc.Add(XElement("BottomPaneSplitterPosition", self.ToString(self._BottomPaneSplitterPosition)))
		ILSpySettings.SaveSettings(doc)

	def Escape(p):
		sb = StringBuilder()
		enumerator = p.GetEnumerator()
		while enumerator.MoveNext():
			ch = enumerator.Current
			if Char.IsLetterOrDigit(ch):
				sb.Append(ch)
			else:
				sb.AppendFormat("\\x{0:X4}", ch)
		return sb.ToString()

	Escape = staticmethod(Escape)

	def Unescape(p):
		return self._regex.Replace(p, )

	Unescape = staticmethod(Unescape)

	def FromString(s, defaultValue):
		if s == None:
			return defaultValue
		try:
			c = TypeDescriptor.GetConverter(clr.GetClrType(T))
			return c.ConvertFromInvariantString(s)
		except FormatException, :
			return defaultValue
		finally:

	FromString = staticmethod(FromString)

	def ToString(obj):
		c = TypeDescriptor.GetConverter(clr.GetClrType(T))
		return c.ConvertToInvariantString(obj)

	ToString = staticmethod(ToString)