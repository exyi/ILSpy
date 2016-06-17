import clr

		import clr

		import clr

		import clr

		import clr

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
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Data import *

class SortableGridViewColumn(GridViewColumn):
	""" <summary>
	 Allows to automatically sort a grid view.
	 </summary>
	"""
	# This class was copied from ICSharpCode.Core.Presentation.
	def __init__(self):
		self._headerTemplateKey = ComponentResourceKey(clr.GetClrType(SortableGridViewColumn), "ColumnHeaderTemplate")
		self._SortDirectionProperty = DependencyProperty.RegisterAttached("SortDirection", clr.GetClrType(ColumnSortDirection), clr.GetClrType(SortableGridViewColumn), FrameworkPropertyMetadata(ColumnSortDirection.None, OnSortDirectionChanged))
		self._CurrentSortColumnProperty = DependencyProperty.RegisterAttached("CurrentSortColumn", clr.GetClrType(SortableGridViewColumn), clr.GetClrType(SortableGridViewColumn), FrameworkPropertyMetadata(OnCurrentSortColumnChanged))
		self._SortModeProperty = DependencyProperty.RegisterAttached("SortMode", clr.GetClrType(ListViewSortMode), clr.GetClrType(SortableGridViewColumn), FrameworkPropertyMetadata(ListViewSortMode.None, OnSortModeChanged))
		self.SetValueToExtension(HeaderTemplateProperty, DynamicResourceExtension(self._headerTemplateKey))

	def get_SortBy(self):
		return self._sortBy

	def set_SortBy(self, value):
		if self._sortBy != value:
			self._sortBy = value
			self.OnPropertyChanged(PropertyChangedEventArgs("SortBy"))

	SortBy = property(fget=get_SortBy, fset=set_SortBy)

	def get_SortDirection(self):
		return self.GetValue(self._SortDirectionProperty)

	def set_SortDirection(self, value):
		self.SetValue(self._SortDirectionProperty, value)

	SortDirection = property(fget=get_SortDirection, fset=set_SortDirection)

	def GetSortDirection(listView):
		return listView.GetValue(self._SortDirectionProperty)

	GetSortDirection = staticmethod(GetSortDirection)

	def SetSortDirection(listView, value):
		listView.SetValue(self._SortDirectionProperty, value)

	SetSortDirection = staticmethod(SetSortDirection)

	def OnSortDirectionChanged(sender, args):
		grid = sender
		if grid != None:
			col = SortableGridViewColumn.GetCurrentSortColumn(grid)
			if col != None:
				col.SortDirection = args.NewValue
			SortableGridViewColumn.Sort(grid)

	OnSortDirectionChanged = staticmethod(OnSortDirectionChanged)

	def GetCurrentSortColumn(listView):
		return listView.GetValue(self._CurrentSortColumnProperty)

	GetCurrentSortColumn = staticmethod(GetCurrentSortColumn)

	def SetCurrentSortColumn(listView, value):
		listView.SetValue(self._CurrentSortColumnProperty, value)

	SetCurrentSortColumn = staticmethod(SetCurrentSortColumn)

	def OnCurrentSortColumnChanged(sender, args):
		grid = sender
		if grid != None:
			oldColumn = args.OldValue
			if oldColumn != None:
				oldColumn.SortDirection = ColumnSortDirection.None
			newColumn = args.NewValue
			if newColumn != None:
				newColumn.SortDirection = SortableGridViewColumn.GetSortDirection(grid)
			SortableGridViewColumn.Sort(grid)

	OnCurrentSortColumnChanged = staticmethod(OnCurrentSortColumnChanged)

	def GetSortMode(listView):
		return listView.GetValue(self._SortModeProperty)

	GetSortMode = staticmethod(GetSortMode)

	def SetSortMode(listView, value):
		listView.SetValue(self._SortModeProperty, value)

	SetSortMode = staticmethod(SetSortMode)

	def OnSortModeChanged(sender, args):
		grid = sender
		if grid != None:
			if args.NewValue != ListViewSortMode.None:
				grid.AddHandler(GridViewColumnHeader.ClickEvent, RoutedEventHandler(GridViewColumnHeaderClickHandler))
			else:
				grid.RemoveHandler(GridViewColumnHeader.ClickEvent, RoutedEventHandler(GridViewColumnHeaderClickHandler))

	OnSortModeChanged = staticmethod(OnSortModeChanged)

	def GridViewColumnHeaderClickHandler(sender, e):
		grid = sender
		headerClicked = e.OriginalSource
		if grid != None and headerClicked != None and headerClicked.Role != GridViewColumnHeaderRole.Padding:
			if headerClicked.Column == SortableGridViewColumn.GetCurrentSortColumn(grid):
				if SortableGridViewColumn.GetSortDirection(grid) == ColumnSortDirection.Ascending:
					SortableGridViewColumn.SetSortDirection(grid, ColumnSortDirection.Descending)
				else:
					SortableGridViewColumn.SetSortDirection(grid, ColumnSortDirection.Ascending)
			else:
				SortableGridViewColumn.SetSortDirection(grid, ColumnSortDirection.Ascending)
				SortableGridViewColumn.SetCurrentSortColumn(grid, headerClicked.Column)

	GridViewColumnHeaderClickHandler = staticmethod(GridViewColumnHeaderClickHandler)

	def Sort(grid):
		currentDirection = SortableGridViewColumn.GetSortDirection(grid)
		column = SortableGridViewColumn.GetCurrentSortColumn(grid)
		if column != None and SortableGridViewColumn.GetSortMode(grid) == ListViewSortMode.Automatic and currentDirection != ColumnSortDirection.None:
			dataView = CollectionViewSource.GetDefaultView(grid.ItemsSource)
			sortBy = column.SortBy
			if self._sortBy == None:
				binding = column.DisplayMemberBinding
				if binding != None and binding.Path != None:
					self._sortBy = binding.Path.Path
			dataView.SortDescriptions.Clear()
			if self._sortBy != None:
				if currentDirection == ColumnSortDirection.Descending:
					direction = ListSortDirection.Descending
				else:
					direction = ListSortDirection.Ascending
				dataView.SortDescriptions.Add(SortDescription(self._sortBy, direction))
			dataView.Refresh()

	Sort = staticmethod(Sort)

class ColumnSortDirection(object):
	def __init__(self):

class ListViewSortMode(object):
	def __init__(self):

	# <summary>
	# Disable automatic sorting when sortable columns are clicked.
	# </summary>
	# <summary>
	# Fully automatic sorting.
	# </summary>
	# <summary>
	# Automatically update SortDirection and CurrentSortColumn properties,
	# but do not actually sort the data.
	# </summary>
class ColumnSortDirectionToVisibilityConverter(IValueConverter):
	def Convert(self, value, targetType, parameter, culture):
		return Visibility.Visible if self.Equals(value, parameter) else Visibility.Collapsed

	def ConvertBack(self, value, targetType, parameter, culture):
		raise NotSupportedException()