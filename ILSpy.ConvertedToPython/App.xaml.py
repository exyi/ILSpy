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
from System.Collections.Generic import *
from System.ComponentModel.Composition.Hosting import *
from System.Diagnostics import *
from System.IO import *
from System.Linq import *
from System.Reflection import *
from System.Threading.Tasks import *
from System.Windows import *
from System.Windows.Documents import *
from System.Windows.Navigation import *
from System.Windows.Threading import *
from ICSharpCode.ILSpy.TextView import *

class App(Application):
	""" <summary>
	 Interaction logic for App.xaml
	 </summary>
	"""
	def get_CompositionContainer(self):
		return self._compositionContainer

	CompositionContainer = property(fget=get_CompositionContainer)

	class ExceptionData(object):
		def __init__(self):

	def __init__(self):

	# Don't use DirectoryCatalog, that causes problems if the plugins are from the Internet zone
	# see http://stackoverflow.com/questions/8063841/mef-loading-plugins-from-a-network-shared-folder
	# Cannot show MessageBox here, because WPF would crash with a XamlParseException
	# Remember and show exceptions in text output, once MainWindow is properly initialized
	def FullyQualifyPath(self, argument):
		# Fully qualify the paths before passing them to another process,
		# because that process might use a different current directory.
		if str.IsNullOrEmpty(argument) or argument[0] == '/':
			return argument
		try:
			return Path.Combine(Environment.CurrentDirectory, argument)
		except ArgumentException, :
			return argument
		finally:

	def DotNet40_UnobservedTaskException(self, sender, e):
		# On .NET 4.0, an unobserved exception in a task terminates the process unless we mark it as observed
		e.SetObserved()

	def Dispatcher_UnhandledException(sender, e):
		Debug.WriteLine(e.Exception.ToString())
		MessageBox.Show(e.Exception.ToString(), "Sorry, we crashed")
		e.Handled = True

	Dispatcher_UnhandledException = staticmethod(Dispatcher_UnhandledException)

	def ShowErrorBox(sender, e):
		ex = e.ExceptionObject
		if ex != None:
			Debug.WriteLine(ex.ToString())
			MessageBox.Show(ex.ToString(), "Sorry, we crashed")

	ShowErrorBox = staticmethod(ShowErrorBox)

	def SendToPreviousInstance(self, message, activate):
		success = False # stop enumeration # continue enumeration
		NativeMethods.EnumWindows(, IntPtr.Zero)
		return success

	def Send(hWnd, message):
		SMTO_NORMAL = 0
		lParam.Padding = IntPtr.Zero
		lParam.Size = message.Length * 2

	Send = staticmethod(Send)

	# SendMessage with 3s timeout (e.g. when the target process is stopped in the debugger)
	def Window_RequestNavigate(self, sender, e):
		if e.Uri.Scheme == "resource":
			output = AvalonEditTextOutput()
			ILSpy.MainWindow.Instance.TextView.ShowText(output)