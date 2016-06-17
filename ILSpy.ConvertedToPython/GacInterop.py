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
from System.IO import *
from System.Text import *
from Mono.Cecil import *

class GacInterop(object):
	""" <summary>
	 Interop with the .NET GAC.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Interop with the .NET GAC.
		 </summary>
		"""
		# <summary>
		# Gets the names of all assemblies in the GAC.
		# </summary> # This region is based on code from Mono.Cecil:
		# Author:
		#   Jb Evain (jbevain@gmail.com)
		#
		# Copyright (c) 2008 - 2010 Jb Evain
		#
		# Permission is hereby granted, free of charge, to any person obtaining
		# a copy of this software and associated documentation files (the
		# "Software"), to deal in the Software without restriction, including
		# without limitation the rights to use, copy, modify, merge, publish,
		# distribute, sublicense, and/or sell copies of the Software, and to
		# permit persons to whom the Software is furnished to do so, subject to
		# the following conditions:
		#
		# The above copyright notice and this permission notice shall be
		# included in all copies or substantial portions of the Software.
		#
		# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
		# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
		# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
		# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
		# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
		# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
		# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
		#
		self._gac_paths = 
		self._gacs = 
		self._prefixes = 

	def GetGacAssemblyFullNames():
		applicationContext = None
		assemblyEnum = None
		assemblyName = None
		Fusion.CreateAssemblyEnum(, None, None, 2, 0)
		while assemblyEnum.GetNextAssembly(, , 0) == 0:
			nChars = 0
			assemblyName.GetDisplayName(None, , 0)
			name = StringBuilder(nChars)
			assemblyName.GetDisplayName(name, , 0)
			r = None
			try:
				r = AssemblyNameReference.Parse(name.ToString())
			except ArgumentException, :
			except FormatException, :
			except OverflowException, :
			finally:
			if r != None:

	GetGacAssemblyFullNames = staticmethod(GetGacAssemblyFullNames)

	def FindAssemblyInNetGac(reference):
		""" <summary>
		 Gets the file name for an assembly stored in the GAC.
		 </summary>
		"""
		# without public key, it can't be in the GAC
		if reference.PublicKeyToken == None:
			return None
		i = 0
		while i < 2:
			j = 0
			while j < self._gacs.Length:
				gac = Path.Combine(self._gac_paths[i], self._gacs[j])
				file = GacInterop.GetAssemblyFile(reference, self._prefixes[i], gac)
				if File.Exists(file):
					return file
				j += 1
			i += 1
		return None

	FindAssemblyInNetGac = staticmethod(FindAssemblyInNetGac)

	def GetAssemblyFile(reference, prefix, gac):
		gac_folder = StringBuilder().Append(prefix).Append(reference.Version).Append("__")
		i = 0
		while i < reference.PublicKeyToken.Length:
			gac_folder.Append(reference.PublicKeyToken[i].ToString("x2"))
			i += 1
		return Path.Combine(Path.Combine(Path.Combine(gac, reference.Name), gac_folder.ToString()), reference.Name + ".dll")

	GetAssemblyFile = staticmethod(GetAssemblyFile)