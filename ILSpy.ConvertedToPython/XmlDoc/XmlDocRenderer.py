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
from System.Diagnostics import *
from System.IO import *
from System.Text import *
from System.Text.RegularExpressions import *
from System.Windows.Controls import *
from System.Xml import *

class XmlDocRenderer(object):
	""" <summary>
	 Renders XML documentation into a WPF <see cref="TextBlock"/>.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Renders XML documentation into a WPF <see cref="TextBlock"/>.
		 </summary>
		"""
		self._ret = StringBuilder()
		self._whitespace = Regex(@"\s+")

	def AppendText(self, text):
		self._ret.Append(text)

	def AddXmlDocumentation(self, xmlDocumentation):
		if xmlDocumentation == None:
			return 
		Debug.WriteLine(xmlDocumentation)
		try:
			r = XmlTextReader(StringReader("<docroot>" + xmlDocumentation + "</docroot>"))
			r.XmlResolver = None
			self.AddXmlDocumentation(r)
		except XmlException, :
		finally:

	def AddXmlDocumentation(self, xml):
		while xml.Read():
			if xml.NodeType == XmlNodeType.Element:
				elname = xml.Name.ToLowerInvariant()
				if elname == "filterpriority" or elname == "remarks":
					xml.Skip()
				elif elname == "example":
					self._ret.Append(Environment.NewLine)
					self._ret.Append("Example:")
					self._ret.Append(Environment.NewLine)
				elif elname == "exception":
					self._ret.Append(Environment.NewLine)
					self._ret.Append(self.GetCref(xml["cref"]))
					self._ret.Append(": ")
				elif elname == "returns":
					self._ret.Append(Environment.NewLine)
					self._ret.Append("Returns: ")
				elif elname == "see":
					self._ret.Append(self.GetCref(xml["cref"]))
					self._ret.Append(xml["langword"])
				elif elname == "seealso":
					self._ret.Append(Environment.NewLine)
					self._ret.Append("See also: ")
					self._ret.Append(self.GetCref(xml["cref"]))
				elif elname == "paramref":
					self._ret.Append(xml["name"])
				elif elname == "param":
					self._ret.Append(Environment.NewLine)
					self._ret.Append(self._whitespace.Replace(xml["name"].Trim(), " "))
					self._ret.Append(": ")
				elif elname == "typeparam":
					self._ret.Append(Environment.NewLine)
					self._ret.Append(self._whitespace.Replace(xml["name"].Trim(), " "))
					self._ret.Append(": ")
				elif elname == "value":
					self._ret.Append(Environment.NewLine)
					self._ret.Append("Value: ")
					self._ret.Append(Environment.NewLine)
				elif elname == "br" or elname == "para":
					self._ret.Append(Environment.NewLine)
			elif xml.NodeType == XmlNodeType.Text:
				self._ret.Append(self._whitespace.Replace(xml.Value, " "))

	def GetCref(cref):
		if cref == None or cref.Trim().Length == 0:
			return ""
		if cref.Length < 2:
			return cref
		if cref.Substring(1, 1) == ":":
			return cref.Substring(2, cref.Length - 2)
		return cref

	GetCref = staticmethod(GetCref)

	def CreateTextBlock(self):
		return TextBlock(Text = self._ret.ToString())