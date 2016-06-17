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
from System.Text import *
from System.Runtime.InteropServices import *

class NativeMethods(object):
	def __init__(self):
		self._WM_COPYDATA = 0x4a

	def EnumWindows(lpEnumFunc, lParam):
		pass

	EnumWindows = staticmethod(EnumWindows)

	def GetWindowText(hWnd, title, size):
		pass

	GetWindowText = staticmethod(GetWindowText)

	def GetWindowText(hWnd, maxLength):
		b = StringBuilder(maxLength + 1)
		if NativeMethods.GetWindowText(hWnd, b, b.Capacity) != 0:
			return b.ToString()
		else:
			return str.Empty

	GetWindowText = staticmethod(GetWindowText)

	def SendMessageTimeout(hWnd, msg, wParam, lParam, flags, timeout, result):
		pass

	SendMessageTimeout = staticmethod(SendMessageTimeout)

	def SetForegroundWindow(hWnd):
		pass

	SetForegroundWindow = staticmethod(SetForegroundWindow)

class CopyDataStruct(object):
	def __init__(self, padding, size, buffer):
		self._Padding = padding
		self._Size = size
		self._Buffer = buffer