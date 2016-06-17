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
from System.IO import *
from System.Text import *
from System.Threading import *
from System.Xml import *
from System.Xml.Linq import *

class ILSpySettings(object):
	""" <summary>
	 Manages IL Spy settings.
	 </summary>
	"""
	def __init__(self, root):
		# <summary>
		# Loads the settings file from disk.
		# </summary>
		# <returns>
		# An instance used to access the loaded settings.
		# </returns>
		# <summary>
		# Saves a setting section.
		# </summary>
		# <summary>
		# Updates the saved settings.
		# We always reload the file on updates to ensure we aren't overwriting unrelated changes performed
		# by another ILSpy instance.
		# </summary>
		# ensure the directory exists
		self._ConfigFileMutex = "01A91708-49D1-410D-B8EB-4DE2662B3971"
		self._root = root

	def __init__(self, root):
		self._ConfigFileMutex = "01A91708-49D1-410D-B8EB-4DE2662B3971"
		self._root = root

	def get_Item(self):
		return root.Element(section) == XElement(section)

	Item = property(fget=get_Item)

	def Load():

	Load = staticmethod(Load)

	def LoadWithoutCheckingCharacters(fileName):
		return XDocument.Load(fileName, LoadOptions.None)

	LoadWithoutCheckingCharacters = staticmethod(LoadWithoutCheckingCharacters)

	def SaveSettings(section):
		ILSpySettings.Update()

	SaveSettings = staticmethod(SaveSettings)

	def Update(action):

	Update = staticmethod(Update)

	def GetConfigFile():
		localPath = Path.Combine(Path.GetDirectoryName(clr.GetClrType(MainWindow).Assembly.Location), "ILSpy.xml")
		if File.Exists(localPath):
			return localPath
		return Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "ICSharpCode\\ILSpy.xml")

	GetConfigFile = staticmethod(GetConfigFile)

	class MutexProtector(IDisposable):
		""" <summary>
		 Helper class for serializing access to the config file when multiple ILSpy instances are running.
		 </summary>
		"""
		def __init__(self, name):
			self._mutex = Mutex(True, name, )
			if not createdNew:
				try:
					self._mutex.WaitOne()
				except AbandonedMutexException, :
				finally:

		def Dispose(self):
			self._mutex.ReleaseMutex()
			self._mutex.Dispose()