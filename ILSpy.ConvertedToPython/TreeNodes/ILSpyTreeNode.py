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
from System.Collections.Specialized import *
from System.ComponentModel import *
from System.Linq import *
from ICSharpCode.Decompiler import *
from ICSharpCode.TreeView import *

class ILSpyTreeNode(SharpTreeNode):
	""" <summary>
	 Base class of all ILSpy tree nodes.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Base class of all ILSpy tree nodes.
		 </summary>
		"""

	def get_FilterSettings(self):
		return self._filterSettings

	def set_FilterSettings(self, value):
		if self._filterSettings != value:
			self._filterSettings = value
			self.OnFilterSettingsChanged()

	FilterSettings = property(fget=get_FilterSettings, fset=set_FilterSettings)

	def get_Language(self):
		return self._filterSettings.Language if self._filterSettings != None else Languages.AllLanguages[0]

	Language = property(fget=get_Language)

	def Filter(self, settings):
		if str.IsNullOrEmpty(settings.SearchTerm):
			return FilterResult.Match
		else:
			return FilterResult.Hidden

	def HighlightSearchMatch(text, suffix):
		# TODO: implement highlighting the search match
		return text + suffix

	HighlightSearchMatch = staticmethod(HighlightSearchMatch)

	def Decompile(self, language, output, options):
		pass

	def View(self, textView):
		""" <summary>
		 Used to implement special view logic for some items.
		 This method is called on the main thread when only a single item is selected.
		 If it returns false, normal decompilation is used to view the item.
		 </summary>
		"""
		return False

	def Save(self, textView):
		""" <summary>
		 Used to implement special save logic for some items.
		 This method is called on the main thread when only a single item is selected.
		 If it returns false, normal decompilation is used to save the item.
		 </summary>
		"""
		return False

	def OnChildrenChanged(self, e):
		if e.NewItems != None:
			if IsVisible:
				enumerator = e.NewItems.GetEnumerator()
				while enumerator.MoveNext():
					node = enumerator.Current
					self.ApplyFilterToChild(node)
			else:
				self._childrenNeedFiltering = True
		self.OnChildrenChanged(e)

	def ApplyFilterToChild(self, child):
		if self.FilterSettings == None:
			r = FilterResult.Match
		else:
			r = child.Filter(self.FilterSettings)
		if r == FilterResult.Hidden:
			child.IsHidden = True
		elif r == FilterResult.Match:
			child.FilterSettings = self.StripSearchTerm(self.FilterSettings)
			child.IsHidden = False
		elif r == FilterResult.Recurse:
			child.FilterSettings = self.FilterSettings
			child.EnsureChildrenFiltered()
			child.IsHidden = child.Children.All()
		elif r == FilterResult.MatchAndRecurse:
			child.FilterSettings = self.StripSearchTerm(self.FilterSettings)
			child.EnsureChildrenFiltered()
			child.IsHidden = child.Children.All()
		else:
			raise InvalidEnumArgumentException()

	def StripSearchTerm(filterSettings):
		if filterSettings == None:
			return None
		if not str.IsNullOrEmpty(filterSettings.SearchTerm):
			filterSettings = filterSettings.Clone()
			filterSettings.SearchTerm = None
		return filterSettings

	StripSearchTerm = staticmethod(StripSearchTerm)

	def OnFilterSettingsChanged(self):
		self.RaisePropertyChanged("Text")
		if IsVisible:
			enumerator = self._Children.OfType().GetEnumerator()
			while enumerator.MoveNext():
				node = enumerator.Current
				self.ApplyFilterToChild(node)
		else:
			self._childrenNeedFiltering = True

	def OnIsVisibleChanged(self):
		self.OnIsVisibleChanged()
		self.EnsureChildrenFiltered()

	def EnsureChildrenFiltered(self):
		self.EnsureLazyChildren()
		if self._childrenNeedFiltering:
			self._childrenNeedFiltering = False
			enumerator = self._Children.OfType().GetEnumerator()
			while enumerator.MoveNext():
				node = enumerator.Current
				self.ApplyFilterToChild(node)

	def get_IsPublicAPI(self):
		return True

	IsPublicAPI = property(fget=get_IsPublicAPI)

	def get_IsAutoLoaded(self):
		return False

	IsAutoLoaded = property(fget=get_IsAutoLoaded)

	def get_Foreground(self):
		if self.IsPublicAPI:
			if self.IsAutoLoaded:
				# HACK: should not be hard coded?
				return System.Windows.Media.Brushes.SteelBlue
			else:
				return self.Foreground
		else:
			return System.Windows.SystemColors.GrayTextBrush

	Foreground = property(fget=get_Foreground)