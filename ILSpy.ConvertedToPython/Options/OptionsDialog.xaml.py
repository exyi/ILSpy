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
from System.ComponentModel.Composition import *
from System.Linq import *
from System.Windows import *
from System.Windows.Controls import *
from System.Xml.Linq import *

class OptionsDialog(Window):
	""" <summary>
	 Interaction logic for OptionsDialog.xaml
	 </summary>
	"""
	def __init__(self):
		self._optionPages = None
		self.InitializeComponent()
		App.CompositionContainer.ComposeParts(self)
		settings = ILSpySettings.Load()
		enumerator = self._optionPages.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			optionPage = enumerator.Current
			tabItem = TabItem()
			tabItem.Header = optionPage.Metadata.Title
			tabItem.Content = optionPage.Value
			tabControl.Items.Add(tabItem)
			page = optionPage.Value
			if page != None:
				page.Load(settings)

	def OKButton_Click(self, sender, e):
		ILSpySettings.Update()
		self._DialogResult = True
		self.Close()

class IOptionsMetadata(object):
	def get_Title(self):

	Title = property(fget=get_Title)

	def get_Order(self):

	Order = property(fget=get_Order)

class IOptionPage(object):
	def Load(self, settings):
		pass

	def Save(self, root):
		pass

class ExportOptionPageAttribute(ExportAttribute):
	def __init__(self):
		pass
	def get_Title(self):

	def set_Title(self, value):

	Title = property(fget=get_Title, fset=set_Title)

	def get_Order(self):

	def set_Order(self, value):

	Order = property(fget=get_Order, fset=set_Order)

class ShowOptionsCommand(SimpleCommand):
	def Execute(self, parameter):
		dlg = OptionsDialog()
		dlg.Owner = MainWindow.Instance
		if dlg.ShowDialog() == True:
			RefreshCommand().Execute(parameter)