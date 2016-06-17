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
from System.Collections.Generic import *
from System.Collections.ObjectModel import *
from System.Collections.Specialized import *
from System.ComponentModel import *
from System.Linq import *
from System.Text.RegularExpressions import *
from System.Threading import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Input import *
from System.Windows.Media import *
from System.Windows.Threading import *
from ICSharpCode.ILSpy.TreeNodes import *
from ICSharpCode.NRefactory.CSharp import *
from ICSharpCode.NRefactory.Utils import *
from Mono.Cecil import *
from Mono.Cecil.Cil import *

class SearchPane(UserControl, IPane):
	""" <summary>
	 Search pane
	 </summary>
	"""
	def get_Instance(self):
		if self._instance == None:
			App.Current.VerifyAccess()
			self._instance = SearchPane()
		return self._instance

	Instance = property(fget=get_Instance)

	def __init__(self):
		self._SearchTermProperty = DependencyProperty.Register("SearchTerm", clr.GetClrType(str), clr.GetClrType(SearchPane), FrameworkPropertyMetadata(str.Empty, OnSearchTermChanged))
		self.InitializeComponent()
		searchModeComboBox.Items.Add((Image = Images.Library, Name = "Types and Members"))
		searchModeComboBox.Items.Add((Image = Images.Class, Name = "Type"))
		searchModeComboBox.Items.Add((Image = Images.Property, Name = "Member"))
		searchModeComboBox.Items.Add((Image = Images.Method, Name = "Method"))
		searchModeComboBox.Items.Add((Image = Images.Field, Name = "Field"))
		searchModeComboBox.Items.Add((Image = Images.Property, Name = "Property"))
		searchModeComboBox.Items.Add((Image = Images.Event, Name = "Event"))
		searchModeComboBox.Items.Add((Image = Images.Literal, Name = "Constant"))
		searchModeComboBox.SelectedIndex = SearchMode.TypeAndMember
		ContextMenuProvider.Add(listBox)
		MainWindow.Instance.CurrentAssemblyListChanged += self.MainWindow_Instance_CurrentAssemblyListChanged

	def MainWindow_Instance_CurrentAssemblyListChanged(self, sender, e):
		if IsVisible:
			self.StartSearch(self._SearchTerm)
		else:
			self.StartSearch(None)
			self._runSearchOnNextShow = True

	def Show(self):
		if not IsVisible:
			MainWindow.Instance.ShowInTopPane("Search", self)
			if self._runSearchOnNextShow:
				self._runSearchOnNextShow = False
				self.StartSearch(self._SearchTerm)
		Dispatcher.BeginInvoke(DispatcherPriority.Background, Action())

	def get_SearchTerm(self):
		return self.GetValue(self._SearchTermProperty)

	def set_SearchTerm(self, value):
		self.SetValue(self._SearchTermProperty, value)

	SearchTerm = property(fget=get_SearchTerm, fset=set_SearchTerm)

	def OnSearchTermChanged(o, e):
		(o).StartSearch(e.NewValue)

	OnSearchTermChanged = staticmethod(OnSearchTermChanged)

	def SearchModeComboBox_SelectionChanged(self, sender, e):
		self.StartSearch(self.SearchTerm)

	def StartSearch(self, searchTerm):
		if self._currentSearch != None:
			self._currentSearch.Cancel()
		if str.IsNullOrEmpty(searchTerm):
			self._currentSearch = None
			listBox.ItemsSource = None
		else:
			mainWindow = MainWindow.Instance
			self._currentSearch = RunningSearch(mainWindow.CurrentAssemblyList.GetAssemblies(), searchTerm, searchModeComboBox.SelectedIndex, mainWindow.CurrentLanguage)
			listBox.ItemsSource = self._currentSearch.Results
			Thread(self._currentSearch.Run).Start()

	def Closed(self):
		self.SearchTerm = str.Empty

	def ListBox_MouseDoubleClick(self, sender, e):
		self.JumpToSelectedItem()
		e.Handled = True

	def ListBox_KeyDown(self, sender, e):
		if e.Key == Key.Return:
			e.Handled = True
			self.JumpToSelectedItem()

	def JumpToSelectedItem(self):
		result = listBox.SelectedItem
		if result != None:
			MainWindow.Instance.JumpToReference(result.Member)

	def OnKeyDown(self, e):
		self.OnKeyDown(e)
		if e.Key == Key.T and e.KeyboardDevice.Modifiers == ModifierKeys.Control:
			searchModeComboBox.SelectedIndex = SearchMode.Type
			e.Handled = True
		elif e.Key == Key.M and e.KeyboardDevice.Modifiers == ModifierKeys.Control:
			searchModeComboBox.SelectedIndex = SearchMode.Member
			e.Handled = True
		elif e.Key == Key.S and e.KeyboardDevice.Modifiers == ModifierKeys.Control:
			searchModeComboBox.SelectedIndex = SearchMode.Literal
			e.Handled = True

	def SearchBox_PreviewKeyDown(self, sender, e):
		if e.Key == Key.Down and listBox.HasItems:
			e.Handled = True
			listBox.MoveFocus(TraversalRequest(FocusNavigationDirection.First))
			listBox.SelectedIndex = 0

	class RunningSearch(object):
		def __init__(self, assemblies, searchTerm, searchMode, language):
			self._cts = CancellationTokenSource()
			self._Results = ObservableCollection[SearchResult]()
			self._dispatcher = Dispatcher.CurrentDispatcher
			self._assemblies = assemblies
			self._searchTerm = searchTerm.Split(Array[Char]((' ')), StringSplitOptions.RemoveEmptyEntries)
			self._language = language
			self._searchMode = searchMode
			self._Results.Add(SearchResult(Name = "Searching..."))

		def Cancel(self):
			self._cts.Cancel()

		def Run(self):
			try:
				searcher = self.GetSearchStrategy(self._searchMode, self._searchTerm)
				enumerator = assemblies.GetEnumerator()
				while enumerator.MoveNext():
					loadedAssembly = enumerator.Current
					module = loadedAssembly.ModuleDefinition
					if module == None:
						continue
					cancellationToken = self._cts.Token
					enumerator = module.Types.GetEnumerator()
					while enumerator.MoveNext():
						type = enumerator.Current
						cancellationToken.ThrowIfCancellationRequested()
						searcher.Search(type, self._language, AddResult)
			except OperationCanceledException, :
			finally:
			# ignore cancellation
			# remove the 'Searching...' entry
			self._dispatcher.BeginInvoke(DispatcherPriority.Normal, Action())

		def AddResult(self, result):
			if self._resultCount += 1 == 1000:
				result = SearchResult(Name = "Search aborted, more than 1000 results found.")
				self._cts.Cancel()
			self._dispatcher.BeginInvoke(DispatcherPriority.Normal, Action())
			self._cts.Token.ThrowIfCancellationRequested()

		def GetSearchStrategy(self, mode, terms):
			if terms.Length == 1:
				if terms[0].StartsWith("tm:", StringComparison.Ordinal):
					return TypeAndMemberSearchStrategy(terms[0].Substring(3))
				if terms[0].StartsWith("t:", StringComparison.Ordinal):
					return TypeSearchStrategy(terms[0].Substring(2))
				if terms[0].StartsWith("m:", StringComparison.Ordinal):
					return MemberSearchStrategy(terms[0].Substring(2))
				if terms[0].StartsWith("md:", StringComparison.Ordinal):
					return MemberSearchStrategy(terms[0].Substring(3), MemberSearchKind.Method)
				if terms[0].StartsWith("f:", StringComparison.Ordinal):
					return MemberSearchStrategy(terms[0].Substring(2), MemberSearchKind.Field)
				if terms[0].StartsWith("p:", StringComparison.Ordinal):
					return MemberSearchStrategy(terms[0].Substring(2), MemberSearchKind.Property)
				if terms[0].StartsWith("e:", StringComparison.Ordinal):
					return MemberSearchStrategy(terms[0].Substring(2), MemberSearchKind.Event)
				if terms[0].StartsWith("c:", StringComparison.Ordinal):
					return LiteralSearchStrategy(terms[0].Substring(2))
			if mode == SearchMode.TypeAndMember:
				return TypeAndMemberSearchStrategy(terms)
			elif mode == SearchMode.Type:
				return TypeSearchStrategy(terms)
			elif mode == SearchMode.Member:
				return MemberSearchStrategy(terms)
			elif mode == SearchMode.Literal:
				return LiteralSearchStrategy(terms)
			elif mode == SearchMode.Method:
				return MemberSearchStrategy(terms, MemberSearchKind.Method)
			elif mode == SearchMode.Field:
				return MemberSearchStrategy(terms, MemberSearchKind.Field)
			elif mode == SearchMode.Property:
				return MemberSearchStrategy(terms, MemberSearchKind.Property)
			elif mode == SearchMode.Event:
				return MemberSearchStrategy(terms, MemberSearchKind.Event)
			return None

class SearchResult(INotifyPropertyChanged, IMemberTreeNode):
	def get_Member(self):

	def set_Member(self, value):

	Member = property(fget=get_Member, fset=set_Member)

	def get_Location(self):

	def set_Location(self, value):

	Location = property(fget=get_Location, fset=set_Location)

	def get_Name(self):

	def set_Name(self, value):

	Name = property(fget=get_Name, fset=set_Name)

	def get_Image(self):

	def set_Image(self, value):

	Image = property(fget=get_Image, fset=set_Image)

	def get_LocationImage(self):

	def set_LocationImage(self, value):

	LocationImage = property(fget=get_LocationImage, fset=set_LocationImage)

	def ToString(self):
		return self.Name

class ShowSearchCommand(CommandWrapper):
	def __init__(self):
		NavigationCommands.Search.InputGestures.Clear()
		NavigationCommands.Search.InputGestures.Add(KeyGesture(Key.F, ModifierKeys.Control | ModifierKeys.Shift))
		NavigationCommands.Search.InputGestures.Add(KeyGesture(Key.E, ModifierKeys.Control))

class SearchMode(object):
	def __init__(self):