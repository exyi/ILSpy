﻿# Copyright (c) 2011 AlphaSierraPapa for the SharpDevelop Team
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
from System.Collections.ObjectModel import *
from System.ComponentModel.Composition.Hosting import *
from System.Linq import *

class Languages(object):
	def __init__(self):

	# <summary>
	# A list of all languages.
	# </summary>
	def get_AllLanguages(self):
		return self._allLanguages

	AllLanguages = property(fget=get_AllLanguages)

	def Initialize(composition):
		languages = List[Language]()
		languages.AddRange(composition.GetExportedValues())
		languages.Add(ILLanguage(True))
		languages.AddRange(ILAstLanguage.GetDebugLanguages())
		languages.AddRange(CSharpLanguage.GetDebugLanguages())
		self._allLanguages = languages.AsReadOnly()

	Initialize = staticmethod(Initialize)

	def GetLanguage(name):
		""" <summary>
		 Gets a language using its name.
		 If the language is not found, C# is returned instead.
		 </summary>
		"""
		return self.AllLanguages.FirstOrDefault() == self.AllLanguages.First()

	GetLanguage = staticmethod(GetLanguage)