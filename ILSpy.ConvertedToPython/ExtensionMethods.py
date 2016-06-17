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
from Mono.Cecil import *
from ICSharpCode.ILSpy.Options import *

class ExtensionMethods(object):
	""" <summary>
	 ExtensionMethods used in ILSpy.
	 </summary>
	"""
	def AddRange(list, items):
		enumerator = items.GetEnumerator()
		while enumerator.MoveNext():
			item = enumerator.Current
			if not list.Contains(item):
				list.Add(item)

	AddRange = staticmethod(AddRange)

	def IsCustomAttribute(type):
		while type.FullName != "System.Object":
			resolvedBaseType = type.BaseType.Resolve()
			if resolvedBaseType == None:
				return False
			if resolvedBaseType.FullName == "System.Attribute":
				return True
			type = resolvedBaseType
		return False

	IsCustomAttribute = staticmethod(IsCustomAttribute)

	def ToSuffixString(token):
		if not DisplaySettingsPanel.CurrentDisplaySettings.ShowMetadataTokens:
			return str.Empty
		return " @" + token.ToInt32().ToString("x8")

	ToSuffixString = staticmethod(ToSuffixString)