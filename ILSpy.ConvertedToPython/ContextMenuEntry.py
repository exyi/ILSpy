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
from ICSharpCode.AvalonEdit import *
from ICSharpCode.ILSpy.TextView import *
from ICSharpCode.TreeView import *

class IContextMenuEntry(object):
	def IsVisible(self, context):
		pass

	def IsEnabled(self, context):
		pass

	def Execute(self, context):
		pass

class TextViewContext(object):
	# <summary>
	# Returns the selected nodes in the tree view.
	# Returns null, if context menu does not belong to a tree view.
	# </summary>
	def get_SelectedTreeNodes(self):

	def set_SelectedTreeNodes(self, value):

	SelectedTreeNodes = property(fget=get_SelectedTreeNodes, fset=set_SelectedTreeNodes)

	# <summary>
	# Returns the tree view the context menu is assigned to.
	# Returns null, if context menu is not assigned to a tree view.
	# </summary>
	def get_TreeView(self):

	def set_TreeView(self, value):

	TreeView = property(fget=get_TreeView, fset=set_TreeView)

	# <summary>
	# Returns the text view the context menu is assigned to.
	# Returns null, if context menu is not assigned to a text view.
	# </summary>
	def get_TextView(self):

	def set_TextView(self, value):

	TextView = property(fget=get_TextView, fset=set_TextView)

	# <summary>
	# Returns the list box the context menu is assigned to.
	# Returns null, if context menu is not assigned to a list box.
	# </summary>
	def get_ListBox(self):

	def set_ListBox(self, value):

	ListBox = property(fget=get_ListBox, fset=set_ListBox)

	# <summary>
	# Returns the reference the mouse cursor is currently hovering above.
	# Returns null, if there was no reference found.
	# </summary>
	def get_Reference(self):

	def set_Reference(self, value):

	Reference = property(fget=get_Reference, fset=set_Reference)

	# <summary>
	# Returns the position in TextView the mouse cursor is currently hovering above.
	# Returns null, if TextView returns null;
	# </summary>
	def get_Position(self):

	def set_Position(self, value):

	Position = property(fget=get_Position, fset=set_Position)

	def Create(treeView, textView, listBox):
		if textView != None:
			reference = textView.GetReferenceSegmentAtMousePosition()
		elif listBox != None:
			reference = ReferenceSegment(Reference = (listBox.SelectedItem).Member)
		else:
			reference = None
		position = textView.GetPositionFromMousePosition() if textView != None else None
		selectedTreeNodes = treeView.GetTopLevelSelection().ToArray() if treeView != None else None
		return TextViewContext(TreeView = treeView, SelectedTreeNodes = selectedTreeNodes, TextView = textView, Reference = reference, Position = position)

	Create = staticmethod(Create)

class IContextMenuEntryMetadata(object):
	def get_Icon(self):

	Icon = property(fget=get_Icon)

	def get_Header(self):

	Header = property(fget=get_Header)

	def get_Category(self):

	Category = property(fget=get_Category)

	def get_Order(self):

	Order = property(fget=get_Order)

class ExportContextMenuEntryAttribute(ExportAttribute, IContextMenuEntryMetadata):
	def __init__(self):
		# entries default to end of menu unless given specific order position
		self.Order = Double.MaxValue

	def get_Icon(self):

	def set_Icon(self, value):

	Icon = property(fget=get_Icon, fset=set_Icon)

	def get_Header(self):

	def set_Header(self, value):

	Header = property(fget=get_Header, fset=set_Header)

	def get_Category(self):

	def set_Category(self, value):

	Category = property(fget=get_Category, fset=set_Category)

	def get_Order(self):

	def set_Order(self, value):

	Order = property(fget=get_Order, fset=set_Order)

class ContextMenuProvider(object):
	def Add(treeView, textView):
		""" <summary>
		 Enables extensible context menu support for the specified tree view.
		 </summary>
		"""
		provider = ContextMenuProvider(treeView, textView)
		treeView.ContextMenuOpening += provider.treeView_ContextMenuOpening
		# Context menu is shown only when the ContextMenu property is not null before the
		# ContextMenuOpening event handler is called.
		treeView.ContextMenu = ContextMenu()
		if textView != None:
			textView.ContextMenuOpening += provider.textView_ContextMenuOpening
			# Context menu is shown only when the ContextMenu property is not null before the
			# ContextMenuOpening event handler is called.
			textView.ContextMenu = ContextMenu()

	Add = staticmethod(Add)

	def Add(listBox):
		provider = ContextMenuProvider(listBox)
		listBox.ContextMenuOpening += provider.listBox_ContextMenuOpening
		listBox.ContextMenu = ContextMenu()

	Add = staticmethod(Add)

	def __init__(self, listBox):
		self._entries = None
		self._listBox = listBox
		App.CompositionContainer.ComposeParts(self)

	def __init__(self, listBox):
		self._entries = None
		self._listBox = listBox
		App.CompositionContainer.ComposeParts(self)

	def treeView_ContextMenuOpening(self, sender, e):
		context = TextViewContext.Create(self._treeView)
		if context.SelectedTreeNodes.Length == 0:
			e.Handled = True # don't show the menu
			return 
		if self.ShowContextMenu(context, ):
			self._treeView.ContextMenu = menu
		else:
			# hide the context menu.
			e.Handled = True

	def textView_ContextMenuOpening(self, sender, e):
		context = TextViewContext.Create(textView = self._textView)
		if self.ShowContextMenu(context, ):
			self._textView.ContextMenu = menu
		else:
			# hide the context menu.
			e.Handled = True

	def listBox_ContextMenuOpening(self, sender, e):
		context = TextViewContext.Create(listBox = self._listBox)
		if self.ShowContextMenu(context, ):
			self._listBox.ContextMenu = menu
		else:
			# hide the context menu.
			e.Handled = True

	def ShowContextMenu(self, context, menu):
		menu = ContextMenu()
		enumerator = self._entries.OrderBy().GroupBy().GetEnumerator()
		while enumerator.MoveNext():
			category = enumerator.Current
			needSeparatorForCategory = menu.Items.Count > 0
			enumerator = category.GetEnumerator()
			while enumerator.MoveNext():
				entryPair = enumerator.Current
				entry = entryPair.Value
				if entry.IsVisible(context):
					if needSeparatorForCategory:
						menu.Items.Add(Separator())
						needSeparatorForCategory = False
					menuItem = MenuItem()
					menuItem.Header = entryPair.Metadata.Header
					if not str.IsNullOrEmpty(entryPair.Metadata.Icon):
						menuItem.Icon = Image(Width = 16, Height = 16, Source = Images.LoadImage(entry, entryPair.Metadata.Icon))
					if entryPair.Value.IsEnabled(context):
						menuItem.Click += 
					else:
						menuItem.IsEnabled = False
					menu.Items.Add(menuItem)
		return menu.Items.Count > 0