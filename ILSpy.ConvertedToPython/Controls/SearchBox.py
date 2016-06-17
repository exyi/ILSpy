import clr

		import clr

		import clr

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
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Input import *
from System.Windows.Media import *
from System.Windows.Threading import *

class SearchBox(TextBox):
	def __init__():
		self._WatermarkTextProperty = DependencyProperty.Register("WatermarkText", clr.GetClrType(str), clr.GetClrType(SearchBox))
		self._WatermarkColorProperty = DependencyProperty.Register("WatermarkColor", clr.GetClrType(Brush), clr.GetClrType(SearchBox))
		self._HasTextProperty = DependencyProperty.Register("HasText", clr.GetClrType(Boolean), clr.GetClrType(SearchBox))
		self._UpdateDelayProperty = DependencyProperty.Register("UpdateDelay", clr.GetClrType(TimeSpan), clr.GetClrType(SearchBox), FrameworkPropertyMetadata(TimeSpan.FromMilliseconds(200)))
		DefaultStyleKeyProperty.OverrideMetadata(clr.GetClrType(SearchBox), FrameworkPropertyMetadata(clr.GetClrType(SearchBox)))

	def get_WatermarkText(self):
		return self.GetValue(self._WatermarkTextProperty)

	def set_WatermarkText(self, value):
		self.SetValue(self._WatermarkTextProperty, value)

	WatermarkText = property(fget=get_WatermarkText, fset=set_WatermarkText)

	def get_WatermarkColor(self):
		return self.GetValue(self._WatermarkColorProperty)

	def set_WatermarkColor(self, value):
		self.SetValue(self._WatermarkColorProperty, value)

	WatermarkColor = property(fget=get_WatermarkColor, fset=set_WatermarkColor)

	def get_HasText(self):
		return self.GetValue(self._HasTextProperty)

	def set_HasText(self, value):
		self.SetValue(self._HasTextProperty, value)

	HasText = property(fget=get_HasText, fset=set_HasText)

	def get_UpdateDelay(self):
		return self.GetValue(self._UpdateDelayProperty)

	def set_UpdateDelay(self, value):
		self.SetValue(self._UpdateDelayProperty, value)

	UpdateDelay = property(fget=get_UpdateDelay, fset=set_UpdateDelay)

	def IconBorder_MouseLeftButtonUp(self, obj, e):
		if self.HasText:
			self._Text = str.Empty

	def OnTextChanged(self, e):
		self.OnTextChanged(e)
		self.HasText = self._Text.Length > 0
		if self._timer == None:
			self._timer = DispatcherTimer()
			self._timer.Tick += self.timer_Tick
		self._timer.Stop()
		self._timer.Interval = self.UpdateDelay
		self._timer.Start()

	def timer_Tick(self, sender, e):
		self._timer.Stop()
		self._timer = None
		textBinding = self.GetBindingExpression(TextProperty)
		if textBinding != None:
			textBinding.UpdateSource()

	def OnLostFocus(self, e):
		if not self.HasText:
			wl = self.GetTemplateChild("WatermarkLabel")
			if wl != None:
				wl.Visibility = Visibility.Visible
		self.OnLostFocus(e)

	def OnGotFocus(self, e):
		if not self.HasText:
			wl = self.GetTemplateChild("WatermarkLabel")
			if wl != None:
				wl.Visibility = Visibility.Hidden
		self.OnGotFocus(e)

	def OnApplyTemplate(self):
		self.OnApplyTemplate()
		iconBorder = self.GetTemplateChild("PART_IconBorder")
		if iconBorder != None:
			iconBorder.MouseLeftButtonUp += self.IconBorder_MouseLeftButtonUp

	def OnKeyDown(self, e):
		if e.Key == Key.Escape and self._Text.Length > 0:
			self._Text = str.Empty
			e.Handled = True
		else:
			self.OnKeyDown(e)