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
from System.Xml.Linq import *

class FilterSettings(INotifyPropertyChanged):
	""" <summary>
	 Represents the filters applied to the tree view.
	 </summary>
	 <remarks>
	 This class is mutable; but the ILSpyTreeNode filtering assumes that filter settings are immutable.
	 Thus, the main window will use one mutable instance (for data-binding), and will assign a new
	 clone to the ILSpyTreeNodes whenever the main mutable instance changes.
	 </remarks>
	"""
	def __init__(self, element):
		self._ShowInternalApi = element.Element("ShowInternalAPI") == True
		self._Language = Languages.GetLanguage(element.Element("Language"))

	def SaveAsXml(self):
		return XElement("FilterSettings", XElement("ShowInternalAPI", self._ShowInternalApi), XElement("Language", self._Language.Name))

	# <summary>
	# Gets/Sets the search term.
	# Only tree nodes containing the search term will be shown.
	# </summary>
	def get_SearchTerm(self):
		return self._searchTerm

	def set_SearchTerm(self, value):
		if self._searchTerm != value:
			self._searchTerm = value
			self.OnPropertyChanged("SearchTerm")

	SearchTerm = property(fget=get_SearchTerm, fset=set_SearchTerm)

	def SearchTermMatches(self, text):
		""" <summary>
		 Gets whether a node with the specified text is matched by the current search term.
		 </summary>
		"""
		if str.IsNullOrEmpty(self._searchTerm):
			return True
		return text.IndexOf(self._searchTerm, StringComparison.OrdinalIgnoreCase) >= 0

	# <summary>
	# Gets/Sets whether internal API members should be shown.
	# </summary>
	def get_ShowInternalApi(self):
		return self._showInternalApi

	def set_ShowInternalApi(self, value):
		if self._showInternalApi != value:
			self._showInternalApi = value
			self.OnPropertyChanged("ShowInternalAPI")

	ShowInternalApi = property(fget=get_ShowInternalApi, fset=set_ShowInternalApi)

	# <summary>
	# Gets/Sets the current language.
	# </summary>
	# <remarks>
	# While this isn't related to filtering, having it as part of the FilterSettings
	# makes it easy to pass it down into all tree nodes.
	# </remarks>
	def get_Language(self):
		return self._language

	def set_Language(self, value):
		if self._language != value:
			self._language = value
			self.OnPropertyChanged("Language")

	Language = property(fget=get_Language, fset=set_Language)

	def OnPropertyChanged(self, propertyName):
		if PropertyChanged != None:
			self.PropertyChanged(self, PropertyChangedEventArgs(propertyName))

	def Clone(self):
		f = self.MemberwiseClone()
		f.PropertyChanged = None
		return f