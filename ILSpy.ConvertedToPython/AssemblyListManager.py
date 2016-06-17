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
from System.Collections.ObjectModel import *
from System.Linq import *
from System.Xml.Linq import *

class AssemblyListManager(object):
	""" <summary>
	 Manages the available assembly lists.
	 
	 Contains the list of list names; and provides methods for loading/saving and creating/deleting lists.
	 </summary>
	"""
	def __init__(self, spySettings):
		self._AssemblyLists = ObservableCollection[str]()
		# <summary>
		# Loads an assembly list from the ILSpySettings.
		# If no list with the specified name is found, the default list is loaded instead.
		# </summary>
		self._DefaultListName = "(Default)"
		doc = spySettings["AssemblyLists"]
		enumerator = doc.Elements("List").GetEnumerator()
		while enumerator.MoveNext():
			list = enumerator.Current
			self._AssemblyLists.Add(list.Attribute("name"))

	def LoadList(self, spySettings, listName):
		list = self.DoLoadList(spySettings, listName)
		if not self._AssemblyLists.Contains(list.ListName):
			self._AssemblyLists.Add(list.ListName)
		return list

	def DoLoadList(self, spySettings, listName):
		doc = spySettings["AssemblyLists"]
		if listName != None:
			enumerator = doc.Elements("List").GetEnumerator()
			while enumerator.MoveNext():
				list = enumerator.Current
				if list.Attribute("name") == listName:
					return AssemblyList(list)
		firstList = doc.Elements("List").FirstOrDefault()
		if firstList != None:
			return AssemblyList(firstList)
		else:
			return AssemblyList(listName == self._DefaultListName)

	def SaveList(list):
		""" <summary>
		 Saves the specifies assembly list into the config file.
		 </summary>
		"""
		ILSpySettings.Update()

	SaveList = staticmethod(SaveList)

	def CreateList(self, list):
		if not self._AssemblyLists.Contains(list.ListName):
			self._AssemblyLists.Add(list.ListName)
			self.SaveList(list)
			return True
		return False

	def DeleteList(self, Name):
		if self._AssemblyLists.Contains(Name):
			self._AssemblyLists.Remove(Name)
			ILSpySettings.Update()
			return True
		return False