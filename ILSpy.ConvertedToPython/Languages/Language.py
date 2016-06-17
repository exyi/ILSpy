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
from System.Collections import *
from System.Collections.Generic import *
from System.IO import *
from System.Linq import *
from System.Resources import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class Language(object):
	""" <summary>
	 Base class for language-specific decompiler implementations.
	 </summary>
	"""
	# <summary>
	# Gets the name of the language (as shown in the UI)
	# </summary>
	def get_Name(self):

	Name = property(fget=get_Name)

	# <summary>
	# Gets the file extension used by source code files in this language.
	# </summary>
	def get_FileExtension(self):

	FileExtension = property(fget=get_FileExtension)

	def get_ProjectFileExtension(self):
		return None

	ProjectFileExtension = property(fget=get_ProjectFileExtension)

	# <summary>
	# Gets the syntax highlighting used for this language.
	# </summary>
	def get_SyntaxHighlighting(self):
		return ICSharpCode.AvalonEdit.Highlighting.HighlightingManager.Instance.GetDefinitionByExtension(self.FileExtension)

	SyntaxHighlighting = property(fget=get_SyntaxHighlighting)

	def DecompileMethod(self, method, output, options):
		self.WriteCommentLine(output, self.TypeToString(method.DeclaringType, True) + "." + method.Name)

	def DecompileProperty(self, property, output, options):
		self.WriteCommentLine(output, self.TypeToString(property.DeclaringType, True) + "." + property.Name)

	def DecompileField(self, field, output, options):
		self.WriteCommentLine(output, self.TypeToString(field.DeclaringType, True) + "." + field.Name)

	def DecompileEvent(self, ev, output, options):
		self.WriteCommentLine(output, self.TypeToString(ev.DeclaringType, True) + "." + ev.Name)

	def DecompileType(self, type, output, options):
		self.WriteCommentLine(output, self.TypeToString(type, True))

	def DecompileNamespace(self, nameSpace, types, output, options):
		self.WriteCommentLine(output, nameSpace)

	def DecompileAssembly(self, assembly, output, options):
		self.WriteCommentLine(output, assembly.FileName)
		if assembly.AssemblyDefinition != None:
			name = assembly.AssemblyDefinition.Name
			if name.IsWindowsRuntime:
				self.WriteCommentLine(output, name.Name + " [WinRT]")
			else:
				self.WriteCommentLine(output, name.FullName)
		else:
			self.WriteCommentLine(output, assembly.ModuleDefinition.Name)

	def WriteCommentLine(self, output, comment):
		output.WriteLine("// " + comment)

	def TypeToString(self, type, includeNamespace, typeAttributes):
		""" <summary>
		 Converts a type reference into a string. This method is used by the member tree node for parameter and return types.
		 </summary>
		"""
		if includeNamespace:
			return type.FullName
		else:
			return type.Name

	def GetTooltip(self, member):
		""" <summary>
		 Converts a member signature to a string.
		 This is used for displaying the tooltip on a member reference.
		 </summary>
		"""
		if :
			return self.TypeToString(member, True)
		else:
			return member.ToString()

	def FormatPropertyName(self, property, isIndexer):
		if property == None:
			raise ArgumentNullException("property")
		return property.Name

	def FormatMethodName(self, method):
		if method == None:
			raise ArgumentNullException("method")
		return method.Name

	def FormatTypeName(self, type):
		if type == None:
			raise ArgumentNullException("type")
		return type.Name

	def ToString(self):
		""" <summary>
		 Used for WPF keyboard navigation.
		 </summary>
		"""
		return self.Name

	def ShowMember(self, member):
		return True

	def GetOriginalCodeLocation(self, member):
		""" <summary>
		 Used by the analyzer to map compiler generated code back to the original code's location
		 </summary>
		"""
		return member

	def WriteResourceFilesInProject(self, assembly, options, directories):
		enumerator = assembly.ModuleDefinition.Resources.OfType().GetEnumerator()
		while enumerator.MoveNext():
			r = enumerator.Current
			stream = r.GetResourceStream()
			stream.Position = 0
			if r.Name.EndsWith(".resources", StringComparison.OrdinalIgnoreCase):
				if self.GetEntries(stream, ) and entries.All():
					enumerator = entries.GetEnumerator()
					while enumerator.MoveNext():
						pair = enumerator.Current
						fileName = Path.Combine((pair.Key).Split('/').Select().ToArray())
						dirName = Path.GetDirectoryName(fileName)
						if not str.IsNullOrEmpty(dirName) and directories.Add(dirName):
							Directory.CreateDirectory(Path.Combine(options.SaveAsProjectDirectory, dirName))
						entryStream = pair.Value
						handled = False
						enumerator = App.CompositionContainer.GetExportedValues().GetEnumerator()
						while enumerator.MoveNext():
							handler = enumerator.Current
							if handler.CanHandle(fileName, options):
								handled = True
								entryStream.Position = 0
								break
						if not handled:
				else:
					stream.Position = 0
					fileName = self.GetFileNameForResource(Path.ChangeExtension(r.Name, ".resx"), directories)
			else:
				fileName = self.GetFileNameForResource(r.Name, directories)

	def GetFileNameForResource(self, fullName, directories):
		splitName = fullName.Split('.')
		fileName = TextView.DecompilerTextView.CleanUpName(fullName)
		i = splitName.Length - 1
		while i > 0:
			ns = str.Join(".", splitName, 0, i)
			if directories.Contains(ns):
				name = str.Join(".", splitName, i, splitName.Length - i)
				fileName = Path.Combine(ns, TextView.DecompilerTextView.CleanUpName(name))
				break
			i -= 1
		return fileName

	def GetEntries(self, stream, entries):
		try:
			entries = ResourceSet(stream).Cast()
			return True
		except ArgumentException, :
			entries = None
			return False
		finally: