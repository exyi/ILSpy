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
from System.Collections.Concurrent import *
from System.Collections.Generic import *
from System.Collections.ObjectModel import *
from System.Collections.Specialized import *
from System.IO import *
from System.Linq import *
from System.Windows.Threading import *
from System.Xml.Linq import *

class AssemblyList(object):
	""" <summary>
	 A list of assemblies.
	 </summary>
	"""
	# <summary>Dirty flag, used to mark modifications so that the list is saved later</summary>
	# <summary>
	# The assemblies in this list.
	# Needs locking for multi-threaded access!
	# Write accesses are allowed on the GUI thread only (but still need locking!)
	# </summary>
	# <remarks>
	# Technically read accesses need locking when done on non-GUI threads... but whenever possible, use the
	# thread-safe <see cref="GetAssemblies()"/> method.
	# </remarks>
	def __init__(self, listElement):
		self._assemblyLookupCache = ConcurrentDictionary[str, LoadedAssembly]()
		self._winRTMetadataLookupCache = ConcurrentDictionary[str, LoadedAssembly]()
		self._assemblies = ObservableCollection[LoadedAssembly]()
		# <summary>
		# Loads an assembly list from XML.
		# </summary>
		enumerator = listElement.Elements("Assembly").GetEnumerator()
		while enumerator.MoveNext():
			asm = enumerator.Current
			self.OpenAssembly(asm)
		self._dirty = False

	def __init__(self, listElement):
		self._assemblyLookupCache = ConcurrentDictionary[str, LoadedAssembly]()
		self._winRTMetadataLookupCache = ConcurrentDictionary[str, LoadedAssembly]()
		self._assemblies = ObservableCollection[LoadedAssembly]()
		enumerator = listElement.Elements("Assembly").GetEnumerator()
		while enumerator.MoveNext():
			asm = enumerator.Current
			self.OpenAssembly(asm)
		self._dirty = False
 # OpenAssembly() sets dirty, so reset it afterwards
	def GetAssemblies(self):
		""" <summary>
		 Gets the loaded assemblies. This method is thread-safe.
		 </summary>
		"""

	def SaveAsXml(self):
		""" <summary>
		 Saves this assembly list to XML.
		 </summary>
		"""
		return XElement("List", XAttribute("name", self._ListName), self._assemblies.Where().Select())

	# <summary>
	# Gets the name of this list.
	# </summary>
	def get_ListName(self):
		return self._listName

	ListName = property(fget=get_ListName)

	def Assemblies_CollectionChanged(self, sender, e):
		self.ClearCache()
		# Whenever the assembly list is modified, mark it as dirty
		# and enqueue a task that saves it once the UI has finished modifying the assembly list.
		if not self._dirty:
			self._dirty = True
			App.Current.Dispatcher.BeginInvoke(DispatcherPriority.Background, Action())

	def RefreshSave(self):
		if not self._dirty:
			self._dirty = True
			App.Current.Dispatcher.BeginInvoke(DispatcherPriority.Background, Action())

	def ClearCache(self):
		self._assemblyLookupCache.Clear()
		self._winRTMetadataLookupCache.Clear()

	def OpenAssembly(self, file, isAutoLoaded):
		""" <summary>
		 Opens an assembly from disk.
		 Returns the existing assembly node if it is already loaded.
		 </summary>
		"""
		App.Current.Dispatcher.VerifyAccess()
		file = Path.GetFullPath(file)
		enumerator = self._assemblies.GetEnumerator()
		while enumerator.MoveNext():
			asm = enumerator.Current
			if file.Equals(asm.FileName, StringComparison.OrdinalIgnoreCase):
				return asm
		newAsm = LoadedAssembly(self, file)
		newAsm.IsAutoLoaded = isAutoLoaded
		return newAsm

	def HotReplaceAssembly(self, file, stream):
		""" <summary>
		 Replace the assembly object model from a crafted stream, without disk I/O
		 Returns null if it is not already loaded.
		 </summary>
		"""
		App.Current.Dispatcher.VerifyAccess()
		file = Path.GetFullPath(file)
		target = self._assemblies.FirstOrDefault()
		if target == None:
			return None
		index = self._assemblies.IndexOf(target)
		newAsm = LoadedAssembly(self, file, stream)
		newAsm.IsAutoLoaded = target.IsAutoLoaded
		return newAsm

	def ReloadAssembly(self, file):
		App.Current.Dispatcher.VerifyAccess()
		file = Path.GetFullPath(file)
		target = self._assemblies.FirstOrDefault()
		if target == None:
			return None
		index = self._assemblies.IndexOf(target)
		newAsm = LoadedAssembly(self, file)
		newAsm.IsAutoLoaded = target.IsAutoLoaded
		return newAsm

	def Unload(self, assembly):
		App.Current.Dispatcher.VerifyAccess()
		self.RequestGC()

	def RequestGC(self):
		if self._gcRequested:
			return 
		self._gcRequested = True
		App.Current.Dispatcher.BeginInvoke(DispatcherPriority.ContextIdle, Action())

	def Sort(self, comparer):
		self.Sort(0, int.MaxValue, comparer)

	def Sort(self, index, count, comparer):
		App.Current.Dispatcher.VerifyAccess()