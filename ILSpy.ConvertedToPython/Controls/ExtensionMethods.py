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
from System.Windows.Markup import *

class ExtensionMethods(object):
	""" <summary>
	 ExtensionMethods used in ILSpy.
	 </summary>
	"""
	def SetValueToExtension(targetObject, property, markupExtension):
		""" <summary>
		 Sets the value of a dependency property on <paramref name="targetObject"/> using a markup extension.
		 </summary>
		 <remarks>This method does not support markup extensions like x:Static that depend on
		 having a XAML file as context.</remarks>
		"""
		# This method was copied from ICSharpCode.Core.Presentation (with permission to switch license to X11)
		if targetObject == None:
			raise ArgumentNullException("targetObject")
		if property == None:
			raise ArgumentNullException("property")
		if markupExtension == None:
			raise ArgumentNullException("markupExtension")
		serviceProvider = SetValueToExtensionServiceProvider(targetObject, property)
		targetObject.SetValue(property, markupExtension.ProvideValue(serviceProvider))

	SetValueToExtension = staticmethod(SetValueToExtension)

	class SetValueToExtensionServiceProvider(IServiceProvider, IProvideValueTarget):
		# This class was copied from ICSharpCode.Core.Presentation (with permission to switch license to X11)
		def __init__(self, targetObject, property):
			self._targetObject = targetObject
			self._targetProperty = property

		def GetService(self, serviceType):
			if serviceType == clr.GetClrType(IProvideValueTarget):
				return self
			else:
				return None

		def get_TargetObject(self):
			return self._targetObject

		TargetObject = property(fget=get_TargetObject)

		def get_TargetProperty(self):
			return self._targetProperty

		TargetProperty = property(fget=get_TargetProperty)