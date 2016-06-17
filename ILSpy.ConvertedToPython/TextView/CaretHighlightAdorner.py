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
from System.Windows.Documents import *
from System.Windows.Media import *
from System.Windows.Media.Animation import *
from System.Windows.Threading import *
from ICSharpCode.AvalonEdit.Editing import *

class CaretHighlightAdorner(Adorner):
	""" <summary>
	 Animated rectangle around the caret.
	 This is used after clicking links that lead to another location within the text view.
	 </summary>
	"""
	def __init__(self, textArea):
		min = textArea.Caret.CalculateCaretRectangle()
		min.Offset(-textArea.TextView.ScrollOffset)
		max = min
		size = Math.Max(min.Width, min.Height) * 0.25
		max.Inflate(size, size)
		self._pen = Pen(TextBlock.GetForeground(textArea.TextView).Clone(), 1)
		self._geometry = RectangleGeometry(min, 2, 2)
		self._geometry.BeginAnimation(RectangleGeometry.RectProperty, RectAnimation(min, max, Duration(TimeSpan.FromMilliseconds(300))AutoReverse = True))
		self._pen.Brush.BeginAnimation(Brush.OpacityProperty, DoubleAnimation(1, 0, Duration(TimeSpan.FromMilliseconds(200))BeginTime = TimeSpan.FromMilliseconds(450)))

	def DisplayCaretHighlightAnimation(textArea):
		layer = AdornerLayer.GetAdornerLayer(textArea.TextView)
		adorner = CaretHighlightAdorner(textArea)
		layer.Add(adorner)
		timer = DispatcherTimer()
		timer.Interval = TimeSpan.FromSeconds(1)
		timer.Tick += 
		timer.Start()

	DisplayCaretHighlightAnimation = staticmethod(DisplayCaretHighlightAnimation)

	def OnRender(self, drawingContext):
		drawingContext.DrawGeometry(None, self._pen, self._geometry)