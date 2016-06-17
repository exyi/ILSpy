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
from System.Diagnostics import *
from System.IO import *
from System.Runtime.CompilerServices import *
from ICSharpCode.NRefactory.Documentation import *
from Mono.Cecil import *

class XmlDocLoader(object):
	""" <summary>
	 Helps finding and loading .xml documentation.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Helps finding and loading .xml documentation.
		 </summary>
		"""
		self._mscorlibDocumentation = Lazy[XmlDocumentationProvider](LoadMscorlibDocumentation)
		self._cache = ConditionalWeakTable[ModuleDefinition, XmlDocumentationProvider]()
		self._referenceAssembliesPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), @"Reference Assemblies\Microsoft\\Framework")
		self._frameworkPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows), @"Microsoft.NET\Framework")

	def LoadMscorlibDocumentation():
		xmlDocFile = XmlDocLoader.FindXmlDocumentation("mscorlib.dll", TargetRuntime.Net_4_0) == XmlDocLoader.FindXmlDocumentation("mscorlib.dll", TargetRuntime.Net_2_0)
		if xmlDocFile != None:
			return XmlDocumentationProvider(xmlDocFile)
		else:
			return None

	LoadMscorlibDocumentation = staticmethod(LoadMscorlibDocumentation)

	def get_MscorlibDocumentation(self):
		return self._mscorlibDocumentation.Value

	MscorlibDocumentation = property(fget=get_MscorlibDocumentation)

	def LoadDocumentation(module):
		if module == None:
			raise ArgumentNullException("module")

	LoadDocumentation = staticmethod(LoadDocumentation)

	def FindXmlDocumentation(assemblyFileName, runtime):
		if runtime == TargetRuntime.Net_1_0:
			fileName = XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._frameworkPath, "v1.0.3705", assemblyFileName))
		elif runtime == TargetRuntime.Net_1_1:
			fileName = XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._frameworkPath, "v1.1.4322", assemblyFileName))
		elif runtime == TargetRuntime.Net_2_0:
			fileName = XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._frameworkPath, "v2.0.50727", assemblyFileName)) == XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._referenceAssembliesPath, "v3.5")) == XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._referenceAssembliesPath, "v3.0")) == XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._referenceAssembliesPath, @".NETFramework\v3.5\Profile\Client"))
		elif runtime == TargetRuntime.Net_4_0 or runtime == :
			fileName = XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._referenceAssembliesPath, @".NETFramework\v4.0", assemblyFileName)) == XmlDocLoader.LookupLocalizedXmlDoc(Path.Combine(self._frameworkPath, "v4.0.30319", assemblyFileName))
		return fileName

	FindXmlDocumentation = staticmethod(FindXmlDocumentation)

	def LookupLocalizedXmlDoc(fileName):
		if str.IsNullOrEmpty(fileName):
			return None
		xmlFileName = Path.ChangeExtension(fileName, ".xml")
		currentCulture = System.Threading.Thread.CurrentThread.CurrentUICulture.TwoLetterISOLanguageName
		localizedXmlDocFile = XmlDocLoader.GetLocalizedName(xmlFileName, currentCulture)
		Debug.WriteLine("Try find XMLDoc @" + localizedXmlDocFile)
		if File.Exists(localizedXmlDocFile):
			return localizedXmlDocFile
		Debug.WriteLine("Try find XMLDoc @" + xmlFileName)
		if File.Exists(xmlFileName):
			return xmlFileName
		if currentCulture != "en":
			englishXmlDocFile = XmlDocLoader.GetLocalizedName(xmlFileName, "en")
			Debug.WriteLine("Try find XMLDoc @" + englishXmlDocFile)
			if File.Exists(englishXmlDocFile):
				return englishXmlDocFile
		return None

	LookupLocalizedXmlDoc = staticmethod(LookupLocalizedXmlDoc)

	def GetLocalizedName(fileName, language):
		localizedXmlDocFile = Path.GetDirectoryName(fileName)
		localizedXmlDocFile = Path.Combine(localizedXmlDocFile, language)
		localizedXmlDocFile = Path.Combine(localizedXmlDocFile, Path.GetFileName(fileName))
		return localizedXmlDocFile

	GetLocalizedName = staticmethod(GetLocalizedName)