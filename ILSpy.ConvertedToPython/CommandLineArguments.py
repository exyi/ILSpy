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

class CommandLineArguments(object):
	# see /doc/Command Line.txt for details
	def __init__(self, arguments):
		self._AssembliesToLoad = List[str]()
		enumerator = arguments.GetEnumerator()
		while enumerator.MoveNext():
			arg = enumerator.Current
			if arg.Length == 0:
				continue
			if arg[0] == '/':
				if arg.Equals("/singleInstance", StringComparison.OrdinalIgnoreCase):
					self._SingleInstance = True
				elif arg.Equals("/separate", StringComparison.OrdinalIgnoreCase):
					self._SingleInstance = False
				elif arg.StartsWith("/navigateTo:", StringComparison.OrdinalIgnoreCase):
					self._NavigateTo = arg.Substring("/navigateTo:".Length)
				elif arg.StartsWith("/search:", StringComparison.OrdinalIgnoreCase):
					self._Search = arg.Substring("/search:".Length)
				elif arg.StartsWith("/language:", StringComparison.OrdinalIgnoreCase):
					self._Language = arg.Substring("/language:".Length)
				elif arg.Equals("/noActivate", StringComparison.OrdinalIgnoreCase):
					self._NoActivate = True
				elif arg.StartsWith("/fixedGuid:", StringComparison.OrdinalIgnoreCase):
					guid = arg.Substring("/fixedGuid:".Length)
					if guid.Length < 32:
						guid = guid + System.String('0', 32 - guid.Length)
					if Guid.TryParse(guid, ):
						self._FixedGuid = fixedGuid
				elif arg.StartsWith("/saveDir:", StringComparison.OrdinalIgnoreCase):
					self._SaveDirectory = arg.Substring("/saveDir:".Length)
			else:
				self._AssembliesToLoad.Add(arg)