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
from System.Collections import *
from System.Text import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Input import *

class ResourceStringTable(UserControl):
	""" <summary>
	 Interaction logic for ResourceStringTable.xaml
	 </summary>
	"""
	def __init__(self, strings, contentPresenter):
		self.InitializeComponent()
		# set size to fit decompiler window
		contentPresenter.SizeChanged += self.OnParentSizeChanged
		Width = contentPresenter.ActualWidth - 45
		MaxHeight = contentPresenter.ActualHeight
		resourceListView.ItemsSource = strings

	def OnParentSizeChanged(self, sender, e):
		if e.WidthChanged:
			Width = e.NewSize.Width - 45
		if e.HeightChanged:
			MaxHeight = e.NewSize.Height

	def ExecuteCopy(self, sender, args):
		sb = StringBuilder()
		enumerator = resourceListView.SelectedItems.GetEnumerator()
		while enumerator.MoveNext():
			item = enumerator.Current
			sb.AppendLine(item.ToString())
		Clipboard.SetText(sb.ToString())

	def CanExecuteCopy(self, sender, args):
		args.CanExecute = True