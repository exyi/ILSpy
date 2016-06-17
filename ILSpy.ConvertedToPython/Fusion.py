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
from System.Runtime.InteropServices import *
from System.Runtime.InteropServices.ComTypes import *
from System.Text import *

class IAssemblyName(object):
	def SetProperty(self, PropertyId, pvProperty, cbProperty):
		pass

	def GetProperty(self, PropertyId, pvProperty, pcbProperty):
		pass

	def Finalize(self):
		pass

	def GetDisplayName(self, szDisplayName, pccDisplayName, dwDisplayFlags):
		pass

	def BindToObject(self, refIID, pAsmBindSink, pApplicationContext, szCodeBase, llFlags, pvReserved, cbReserved, ppv):
		pass

	def GetName(self, lpcwBuffer, pwzName):
		pass

	def GetVersion(self, pdwVersionHi, pdwVersionLow):
		pass

	def IsEqual(self, pName, dwCmpFlags):
		pass

	def Clone(self, pName):
		pass

class IApplicationContext(object):
	# .NET Fusion COM interfaces
	def SetContextNameObject(self, pName):
		pass

	def GetContextNameObject(self, ppName):
		pass

	def Set(self, szName, pvValue, cbValue, dwFlags):
		pass

	def Get(self, szName, pvValue, pcbValue, dwFlags):
		pass

	def GetDynamicDirectory(self, wzDynamicDir, pdwSize):
		pass

class IAssemblyEnum(object):
	def GetNextAssembly(self, ppAppCtx, ppName, dwFlags):
		pass

	def Reset(self):
		pass

	def Clone(self, ppEnum):
		pass

class Fusion(object):
	def CreateAssemblyEnum(ppEnum, pAppCtx, pName, dwFlags, pvReserved):
		pass

	CreateAssemblyEnum = staticmethod(CreateAssemblyEnum)

	def GetCachePath(flags, wzDir, pdwSize):
		pass

	GetCachePath = staticmethod(GetCachePath)

	# dwFlags: 1 = Enumerate native image (NGEN) assemblies
	#          2 = Enumerate GAC assemblies
	#          4 = Enumerate Downloaded assemblies
	#
	def GetGacPath(isCLRv4):
		ASM_CACHE_ROOT = 0x08 # CLR V2.0
		ASM_CACHE_ROOT_EX = 0x80 # CLR V4.0
		flags = ASM_CACHE_ROOT_EX if isCLRv4 else ASM_CACHE_ROOT
		size = 260 # MAX_PATH
		b = StringBuilder(size)
		tmp = size
		Fusion.GetCachePath(flags, b, )
		return b.ToString()

	GetGacPath = staticmethod(GetGacPath)