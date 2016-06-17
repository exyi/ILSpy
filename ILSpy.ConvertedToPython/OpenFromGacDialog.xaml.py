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
from System.Collections.Generic import *
from System.Collections.ObjectModel import *
from System.ComponentModel import *
from System.Linq import *
from System.Text import *
from System.Threading import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Threading import *
from ICSharpCode.ILSpy.Controls import *
from Mono.Cecil import *

class OpenFromGacDialog(Window):
	""" <summary>
	 Interaction logic for OpenFromGacDialog.xaml
	 </summary>
	"""
	def __init__(self):
		self._gacEntries = ObservableCollection[GacEntry]()
		self._filteredEntries = ObservableCollection[GacEntry]()
		self._filterMethod = 
		self.InitializeComponent()
		listView.ItemsSource = self._filteredEntries
		SortableGridViewColumn.SetCurrentSortColumn(listView, nameColumn)
		SortableGridViewColumn.SetSortDirection(listView, ColumnSortDirection.Ascending)
		Thread(ThreadStart(FetchGacContents)).Start()

	def OnClosing(self, e):
		self.OnClosing(e)
		self._cancelFetchThread = True

	class GacEntry(object):
		def __init__(self, r, fileName):
			self._r = r
			self._fileName = fileName

		def get_FullName(self):
			return r.FullName

		FullName = property(fget=get_FullName)

		def get_ShortName(self):
			return r.Name

		ShortName = property(fget=get_ShortName)

		def get_FileName(self):
			return fileName

		FileName = property(fget=get_FileName)

		def get_Version(self):
			return r.Version

		Version = property(fget=get_Version)

		def get_FormattedVersion(self):
			if self._formattedVersion == None:
				self._formattedVersion = self.Version.ToString()
			return self._formattedVersion

		FormattedVersion = property(fget=get_FormattedVersion)

		def get_Culture(self):
			return r.Culture

		Culture = property(fget=get_Culture)

		def get_PublicKeyToken(self):
			s = StringBuilder()
			enumerator = r.PublicKeyToken.GetEnumerator()
			while enumerator.MoveNext():
				b = enumerator.Current
				s.Append(b.ToString("x2"))
			return s.ToString()

		PublicKeyToken = property(fget=get_PublicKeyToken)

		def ToString(self):
			return self._r.FullName

	def FetchGacContents(self):
		fullNames = HashSet[str]()
		self.UpdateProgressBar()
		list = GacInterop.GetGacAssemblyFullNames().TakeWhile().ToList()
		self.UpdateProgressBar()
		enumerator = list.GetEnumerator()
		while enumerator.MoveNext():
			r = enumerator.Current
			if cancelFetchThread:
				break
			if fullNames.Add(self._r.FullName): # filter duplicates
				file = GacInterop.FindAssemblyInNetGac(self._r)
				if file != None:
					entry = GacEntry(self._r, file)
					self.UpdateProgressBar()
		self.UpdateProgressBar()

	def UpdateProgressBar(self, updateAction):
		Dispatcher.BeginInvoke(DispatcherPriority.Normal, ())

	def AddNewEntry(self, entry):
		gacEntries.Add(entry)
		if self.filterMethod(entry):
			filteredEntries.Add(entry)

	def FilterTextBox_TextChanged(self, sender, e):
		filterString = filterTextBox.Text.Trim()
		if filterString.Length == 0:
			filterMethod = 
		else:
			elements = filterString.Split(Array[Char]((' ')), StringSplitOptions.RemoveEmptyEntries)
			filterMethod = 
		filteredEntries.Clear()
		filteredEntries.AddRange(gacEntries.Where())

	def Contains(s, subString):
		return s.IndexOf(subString, StringComparison.OrdinalIgnoreCase) >= 0

	Contains = staticmethod(Contains)

	def ListView_SelectionChanged(self, sender, e):
		okButton.IsEnabled = listView.SelectedItems.Count > 0

	def OKButton_Click(self, sender, e):
		self._DialogResult = True
		self.Close()

	def get_SelectedFileNames(self):
		return listView.SelectedItems.OfType().Select().ToArray()

	SelectedFileNames = property(fget=get_SelectedFileNames)