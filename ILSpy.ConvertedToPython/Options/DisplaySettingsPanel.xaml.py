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
from System.Linq import *
from System.Threading.Tasks import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Data import *
from System.Windows.Media import *
from System.Windows.Threading import *
from System.Xml.Linq import *

class DisplaySettingsPanel(UserControl, IOptionPage):
	def __init__(self):
		""" <summary>
		 Interaction logic for DisplaySettingsPanel.xaml
		 </summary>
		"""
		self.InitializeComponent()
		task = Task[Array[FontFamily]](FontLoader)
		task.Start()
		task.ContinueWith()

	def Load(self, settings):
		self._DataContext = self.LoadDisplaySettings(settings)

	def get_CurrentDisplaySettings(self):
		return self._currentDisplaySettings == (self._currentDisplaySettings = self.LoadDisplaySettings(ILSpySettings.Load()))

	CurrentDisplaySettings = property(fget=get_CurrentDisplaySettings)

	def IsSymbolFont(fontFamily):
		enumerator = fontFamily.GetTypefaces().GetEnumerator()
		while enumerator.MoveNext():
			tf = enumerator.Current
			try:
				if tf.TryGetGlyphTypeface():
					return glyph.Symbol
			except Exception, :
				return True
			finally:
		return False

	IsSymbolFont = staticmethod(IsSymbolFont)

	def FontLoader():
		return Fonts.SystemFontFamilies.Where().OrderBy().ToArray()

	FontLoader = staticmethod(FontLoader)

	def LoadDisplaySettings(settings):
		e = settings["DisplaySettings"]
		s = DisplaySettings()
		s.SelectedFont = FontFamily(e.Attribute("Font") == "Consolas")
		s.SelectedFontSize = e.Attribute("FontSize") == 10.0 * 4 / 3
		s.ShowLineNumbers = e.Attribute("ShowLineNumbers") == False
		s.ShowMetadataTokens = e.Attribute("ShowMetadataTokens") == False
		s.EnableWordWrap = e.Attribute("EnableWordWrap") == False
		return s

	LoadDisplaySettings = staticmethod(LoadDisplaySettings)

	def Save(self, root):
		s = self._DataContext
		self._currentDisplaySettings.CopyValues(s)
		section = XElement("DisplaySettings")
		section.SetAttributeValue("Font", s.SelectedFont.Source)
		section.SetAttributeValue("FontSize", s.SelectedFontSize)
		section.SetAttributeValue("ShowLineNumbers", s.ShowLineNumbers)
		section.SetAttributeValue("ShowMetadataTokens", s.ShowMetadataTokens)
		section.SetAttributeValue("EnableWordWrap", s.EnableWordWrap)
		existingElement = root.Element("DisplaySettings")
		if existingElement != None:
			existingElement.ReplaceWith(section)
		else:
			root.Add(section)

class FontSizeConverter(IValueConverter):
	def Convert(self, value, targetType, parameter, culture):
		if :
			return Math.Round(value / 4 * 3)
		raise NotImplementedException()

	def ConvertBack(self, value, targetType, parameter, culture):
		if :
			if Double.TryParse(value, ):
				return d * 4 / 3
			return 11 * 4 / 3
		raise NotImplementedException()