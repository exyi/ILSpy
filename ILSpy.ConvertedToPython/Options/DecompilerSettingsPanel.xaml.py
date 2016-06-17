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
from System.Windows.Controls import *
from System.Xml.Linq import *
from ICSharpCode.Decompiler import *

class DecompilerSettingsPanel(UserControl, IOptionPage):
	def __init__(self):
		""" <summary>
		 Interaction logic for DecompilerSettingsPanel.xaml
		 </summary>
		"""
		self.InitializeComponent()

	def Load(self, settings):
		self._DataContext = self.LoadDecompilerSettings(settings)

	def get_CurrentDecompilerSettings(self):
		return self._currentDecompilerSettings == (self._currentDecompilerSettings = self.LoadDecompilerSettings(ILSpySettings.Load()))

	CurrentDecompilerSettings = property(fget=get_CurrentDecompilerSettings)

	def LoadDecompilerSettings(settings):
		e = settings["DecompilerSettings"]
		s = DecompilerSettings()
		s.AnonymousMethods = e.Attribute("anonymousMethods") == s.AnonymousMethods
		s.YieldReturn = e.Attribute("yieldReturn") == s.YieldReturn
		s.AsyncAwait = e.Attribute("asyncAwait") == s.AsyncAwait
		s.QueryExpressions = e.Attribute("queryExpressions") == s.QueryExpressions
		s.ExpressionTrees = e.Attribute("expressionTrees") == s.ExpressionTrees
		s.UseDebugSymbols = e.Attribute("useDebugSymbols") == s.UseDebugSymbols
		s.ShowXmlDocumentation = e.Attribute("xmlDoc") == s.ShowXmlDocumentation
		s.FoldBraces = e.Attribute("foldBraces") == s.FoldBraces
		return s

	LoadDecompilerSettings = staticmethod(LoadDecompilerSettings)

	def Save(self, root):
		s = self._DataContext
		section = XElement("DecompilerSettings")
		section.SetAttributeValue("anonymousMethods", s.AnonymousMethods)
		section.SetAttributeValue("yieldReturn", s.YieldReturn)
		section.SetAttributeValue("asyncAwait", s.AsyncAwait)
		section.SetAttributeValue("queryExpressions", s.QueryExpressions)
		section.SetAttributeValue("expressionTrees", s.ExpressionTrees)
		section.SetAttributeValue("useDebugSymbols", s.UseDebugSymbols)
		section.SetAttributeValue("xmlDoc", s.ShowXmlDocumentation)
		section.SetAttributeValue("foldBraces", s.FoldBraces)
		existingElement = root.Element("DecompilerSettings")
		if existingElement != None:
			existingElement.ReplaceWith(section)
		else:
			root.Add(section)
		self._currentDecompilerSettings = None