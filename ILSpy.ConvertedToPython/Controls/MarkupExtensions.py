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
from System.Windows.Markup import *
from System.Windows.Media import *

class ControlColor(MarkupExtension):
	# <summary>
	# Amount of highlight (0..1)
	# </summary>
	def get_Highlight(self):

	def set_Highlight(self, value):

	Highlight = property(fget=get_Highlight, fset=set_Highlight)

	def __init__(self, val):
		""" <summary>
		 val: Color value in the range 105..255.
		 </summary>
		"""
		if not (val >= 105 and val <= 255):
			raise ArgumentOutOfRangeException("val")
		self._val = val

	def ProvideValue(self, serviceProvider):
		if self._val > 227:
			return self.Interpolate(227, SystemColors.ControlLightColor, 255, SystemColors.ControlLightLightColor)
		elif self._val > 160:
			return self.Interpolate(160, SystemColors.ControlDarkColor, 227, SystemColors.ControlLightColor)
		else:
			return self.Interpolate(105, SystemColors.ControlDarkDarkColor, 160, SystemColors.ControlDarkColor)

	def Interpolate(self, v1, c1, v2, c2):
		v = (self._val - v1) / (v2 - v1)
		c = c1 * (1 - v) + c2 * v
		return c * (1 - self.Highlight) + SystemColors.HighlightColor * self.Highlight