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
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Input import *

class DockedPane(Control):
	def __init__():
		self._TitleProperty = DependencyProperty.Register("Title", clr.GetClrType(str), clr.GetClrType(DockedPane))
		self._ContentProperty = DependencyProperty.Register("Content", clr.GetClrType(Object), clr.GetClrType(DockedPane))
		DefaultStyleKeyProperty.OverrideMetadata(clr.GetClrType(DockedPane), FrameworkPropertyMetadata(clr.GetClrType(DockedPane)))

	def get_Title(self):
		return self.GetValue(self._TitleProperty)

	def set_Title(self, value):
		self.SetValue(self._TitleProperty, value)

	Title = property(fget=get_Title, fset=set_Title)

	def get_Content(self):
		return self.GetValue(self._ContentProperty)

	def set_Content(self, value):
		self.SetValue(self._ContentProperty, value)

	Content = property(fget=get_Content, fset=set_Content)

	def OnApplyTemplate(self):
		self.OnApplyTemplate()
		closeButton = self._Template.FindName("PART_Close", self)
		if closeButton != None:
			closeButton.Click += self.closeButton_Click

	def closeButton_Click(self, sender, e):
		if CloseButtonClicked != None:
			self.CloseButtonClicked(self, e)

	def OnKeyDown(self, e):
		self.OnKeyDown(e)
		if e.Key == Key.F4 and e.KeyboardDevice.Modifiers == ModifierKeys.Control or e.Key == Key.Escape:
			if CloseButtonClicked != None:
				self.CloseButtonClicked(self, e)
			e.Handled = True