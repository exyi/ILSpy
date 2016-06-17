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
from System.Windows.Media import *

class DisplaySettings(INotifyPropertyChanged):
	""" <summary>
	 Description of DisplaySettings.
	 </summary>
	"""
	def __init__(self):

	def OnPropertyChanged(self, e):
		if PropertyChanged != None:
			self.PropertyChanged(self, e)

	def OnPropertyChanged(self, propertyName):
		self.OnPropertyChanged(PropertyChangedEventArgs(propertyName))

	def get_SelectedFont(self):
		return self._selectedFont

	def set_SelectedFont(self, value):
		if self._selectedFont != value:
			self._selectedFont = value
			self.OnPropertyChanged("SelectedFont")

	SelectedFont = property(fget=get_SelectedFont, fset=set_SelectedFont)

	def get_SelectedFontSize(self):
		return self._selectedFontSize

	def set_SelectedFontSize(self, value):
		if self._selectedFontSize != value:
			self._selectedFontSize = value
			self.OnPropertyChanged("SelectedFontSize")

	SelectedFontSize = property(fget=get_SelectedFontSize, fset=set_SelectedFontSize)

	def get_ShowLineNumbers(self):
		return self._showLineNumbers

	def set_ShowLineNumbers(self, value):
		if self._showLineNumbers != value:
			self._showLineNumbers = value
			self.OnPropertyChanged("ShowLineNumbers")

	ShowLineNumbers = property(fget=get_ShowLineNumbers, fset=set_ShowLineNumbers)

	def get_ShowMetadataTokens(self):
		return self._showMetadataTokens

	def set_ShowMetadataTokens(self, value):
		if self._showMetadataTokens != value:
			self._showMetadataTokens = value
			self.OnPropertyChanged("ShowMetadataTokens")

	ShowMetadataTokens = property(fget=get_ShowMetadataTokens, fset=set_ShowMetadataTokens)

	def get_EnableWordWrap(self):
		return self._enableWordWrap

	def set_EnableWordWrap(self, value):
		if self._enableWordWrap != value:
			self._enableWordWrap = value
			self.OnPropertyChanged("EnableWordWrap")

	EnableWordWrap = property(fget=get_EnableWordWrap, fset=set_EnableWordWrap)

	def CopyValues(self, s):
		self.SelectedFont = s.selectedFont
		self.SelectedFontSize = s.selectedFontSize
		self.ShowLineNumbers = s.showLineNumbers
		self.ShowMetadataTokens = s.showMetadataTokens
		self.EnableWordWrap = s.enableWordWrap