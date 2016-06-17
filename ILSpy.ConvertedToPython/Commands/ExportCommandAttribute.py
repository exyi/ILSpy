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
from System.Windows.Input import *

class IToolbarCommandMetadata(object):
	def get_ToolbarIcon(self):

	ToolbarIcon = property(fget=get_ToolbarIcon)

	def get_ToolTip(self):

	ToolTip = property(fget=get_ToolTip)

	def get_ToolbarCategory(self):

	ToolbarCategory = property(fget=get_ToolbarCategory)

	def get_Tag(self):

	Tag = property(fget=get_Tag)

	def get_ToolbarOrder(self):

	ToolbarOrder = property(fget=get_ToolbarOrder)

class ExportToolbarCommandAttribute(ExportAttribute, IToolbarCommandMetadata):
	def __init__(self):
		pass
	def get_ToolTip(self):

	def set_ToolTip(self, value):

	ToolTip = property(fget=get_ToolTip, fset=set_ToolTip)

	def get_ToolbarIcon(self):

	def set_ToolbarIcon(self, value):

	ToolbarIcon = property(fget=get_ToolbarIcon, fset=set_ToolbarIcon)

	def get_ToolbarCategory(self):

	def set_ToolbarCategory(self, value):

	ToolbarCategory = property(fget=get_ToolbarCategory, fset=set_ToolbarCategory)

	def get_ToolbarOrder(self):

	def set_ToolbarOrder(self, value):

	ToolbarOrder = property(fget=get_ToolbarOrder, fset=set_ToolbarOrder)

	def get_Tag(self):

	def set_Tag(self, value):

	Tag = property(fget=get_Tag, fset=set_Tag)

class IMainMenuCommandMetadata(object):
	def get_MenuIcon(self):

	MenuIcon = property(fget=get_MenuIcon)

	def get_Header(self):

	Header = property(fget=get_Header)

	def get_Menu(self):

	Menu = property(fget=get_Menu)

	def get_MenuCategory(self):

	MenuCategory = property(fget=get_MenuCategory)

	def get_InputGestureText(self):

	InputGestureText = property(fget=get_InputGestureText)

	def get_IsEnabled(self):

	IsEnabled = property(fget=get_IsEnabled)

	def get_MenuOrder(self):

	MenuOrder = property(fget=get_MenuOrder)

class ExportMainMenuCommandAttribute(ExportAttribute, IMainMenuCommandMetadata):
	def __init__(self):
		self._isEnabled = True

	def get_MenuIcon(self):

	def set_MenuIcon(self, value):

	MenuIcon = property(fget=get_MenuIcon, fset=set_MenuIcon)

	def get_Header(self):

	def set_Header(self, value):

	Header = property(fget=get_Header, fset=set_Header)

	def get_Menu(self):

	def set_Menu(self, value):

	Menu = property(fget=get_Menu, fset=set_Menu)

	def get_MenuCategory(self):

	def set_MenuCategory(self, value):

	MenuCategory = property(fget=get_MenuCategory, fset=set_MenuCategory)

	def get_InputGestureText(self):

	def set_InputGestureText(self, value):

	InputGestureText = property(fget=get_InputGestureText, fset=set_InputGestureText)

	def get_IsEnabled(self):
		return self._isEnabled

	def set_IsEnabled(self, value):
		self._isEnabled = value

	IsEnabled = property(fget=get_IsEnabled, fset=set_IsEnabled)

	def get_MenuOrder(self):

	def set_MenuOrder(self, value):

	MenuOrder = property(fget=get_MenuOrder, fset=set_MenuOrder)