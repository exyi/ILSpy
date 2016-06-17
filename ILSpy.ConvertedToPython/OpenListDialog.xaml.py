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
from System.Windows import *
from System.Windows.Controls import *
from Mono.Cecil import *
from System.Windows.Input import *

class OpenListDialog(Window):
	""" <summary>
	 Interaction logic for OpenListDialog.xaml
	 </summary>
	"""
	def __init__(self):
		self._DotNet4List = ".NET 4 (WPF)"
		self._DotNet35List = ".NET 3.5"
		self._ASPDotNetMVC3List = "ASP.NET (MVC3)"
		self.InitializeComponent()
		self._manager = MainWindow.Instance.assemblyListManager

	def listView_Loaded(self, sender, e):
		listView.ItemsSource = self._manager.AssemblyLists
		self.CreateDefaultAssemblyLists()

	def ListView_SelectionChanged(self, sender, e):
		okButton.IsEnabled = listView.SelectedItem != None
		removeButton.IsEnabled = listView.SelectedItem != None

	def OKButton_Click(self, sender, e):
		self._DialogResult = True

	def get_SelectedListName(self):
		return listView.SelectedItem.ToString()

	SelectedListName = property(fget=get_SelectedListName)

	def CreateDefaultAssemblyLists(self):
		if not self._manager.AssemblyLists.Contains(self._DotNet4List):
			dotnet4 = AssemblyList(self._DotNet4List)
			self.AddToList(dotnet4, "mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "System.Core, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "System.Data, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "System.Data.DataSetExtensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "System.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "System.Xml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "System.Xml.Linq, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet4, "Microsoft.CSharp, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")
			self.AddToList(dotnet4, "PresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(dotnet4, "PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(dotnet4, "WindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			if dotnet4.assemblies.Count > 0:
				self._manager.CreateList(dotnet4)
		if not self._manager.AssemblyLists.Contains(self._DotNet35List):
			dotnet35 = AssemblyList(self._DotNet35List)
			self.AddToList(dotnet35, "mscorlib, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet35, "System, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet35, "System.Core, Version=3.5.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet35, "System.Data, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet35, "System.Data.DataSetExtensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet35, "System.Xml, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet35, "System.Xml.Linq, Version=3.5.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(dotnet35, "PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(dotnet35, "PresentationFramework, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(dotnet35, "WindowsBase, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			if dotnet35.assemblies.Count > 0:
				self._manager.CreateList(dotnet35)
		if not self._manager.AssemblyLists.Contains(self._ASPDotNetMVC3List):
			mvc = AssemblyList(self._ASPDotNetMVC3List)
			self.AddToList(mvc, "mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System.ComponentModel.DataAnnotations, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Configuration, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")
			self.AddToList(mvc, "System.Core, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System.Data, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System.Data.DataSetExtensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System.Data.Entity, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System.Drawing, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")
			self.AddToList(mvc, "System.EnterpriseServices, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")
			self.AddToList(mvc, "System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")
			self.AddToList(mvc, "System.Web.Abstractions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Web.ApplicationServices, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Web.DynamicData, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Web.Entity, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Web.Mvc, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Web.Routing, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Web.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")
			self.AddToList(mvc, "System.Web.WebPages, Version=1.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Web.Helpers, Version=1.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
			self.AddToList(mvc, "System.Xml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "System.Xml.Linq, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
			self.AddToList(mvc, "Microsoft.CSharp, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")
			if mvc.assemblies.Count > 0:
				self._manager.CreateList(mvc)

	def AddToList(self, list, FullName):
		reference = AssemblyNameReference.Parse(FullName)
		file = GacInterop.FindAssemblyInNetGac(reference)
		if file != None:
			list.OpenAssembly(file)

	def CreateButton_Click(self, sender, e):
		dlg = CreateListDialog()
		dlg.Owner = self
		dlg.Closing += 
		if dlg.ShowDialog() == True:
			self._manager.CreateList(AssemblyList(dlg.NewListName))

	def RemoveButton_Click(self, sender, e):
		if listView.SelectedItem != None:
			self._manager.DeleteList(listView.SelectedItem.ToString())

	def listView_MouseDoubleClick(self, sender, e):
		if e.ChangedButton == MouseButton.Left and listView.SelectedItem != None:
			self._DialogResult = True