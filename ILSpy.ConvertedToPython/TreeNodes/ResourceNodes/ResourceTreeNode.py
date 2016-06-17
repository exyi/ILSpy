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
from System.IO import *
from System.Text import *
from ICSharpCode.AvalonEdit.Highlighting import *
from ICSharpCode.AvalonEdit.Utils import *
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.TextView import *
from Microsoft.Win32 import *
from Mono.Cecil import *

class ResourceTreeNode(ILSpyTreeNode):
	""" <summary>
	 This is the default resource entry tree node, which is used if no specific
	 <see cref="IResourceNodeFactory"/> exists for the given resource type. 
	 </summary>
	"""
	def __init__(self, r):
		if r == None:
			raise ArgumentNullException("r")
		self._r = r

	def get_Resource(self):
		return r

	Resource = property(fget=get_Resource)

	def get_Text(self):
		return r.Name

	Text = property(fget=get_Text)

	def get_Icon(self):
		return Images.Resource

	Icon = property(fget=get_Icon)

	def Filter(self, settings):
		if not settings.ShowInternalApi and (self._r.Attributes & ManifestResourceAttributes.VisibilityMask) == ManifestResourceAttributes.Private:
			return FilterResult.Hidden
		if settings.SearchTermMatches(self._r.Name):
			return FilterResult.Match
		else:
			return FilterResult.Hidden

	def Decompile(self, language, output, options):
		language.WriteCommentLine(output, str.Format("{0} ({1}, {2})", self._r.Name, self._r.ResourceType, self._r.Attributes))
		smartOutput = output
		if smartOutput != None and :
			smartOutput.AddButton(Images.Save, "Save", )
			output.WriteLine()

	def View(self, textView):
		er = self._r
		if er != None:
			s = er.GetResourceStream()
			if s != None and s.Length < DecompilerTextView.DefaultOutputLengthLimit:
				s.Position = 0
				type = GuessFileType.DetectFileType(s)
				if type != FileType.Binary:
					s.Position = 0
					output = AvalonEditTextOutput()
					output.Write(FileReader.OpenStream(s, Encoding.UTF8).ReadToEnd())
					if type == FileType.Xml:
						ext = ".xml"
					else:
						ext = Path.GetExtension(DecompilerTextView.CleanUpName(er.Name))
					textView.ShowNode(output, self, HighlightingManager.Instance.GetDefinitionByExtension(ext))
					return True
		return False

	def Save(self, textView):
		er = self._r
		if er != None:
			dlg = SaveFileDialog()
			dlg.FileName = DecompilerTextView.CleanUpName(er.Name)
			if dlg.ShowDialog() == True:
				s = er.GetResourceStream()
				s.Position = 0
			return True
		return False

	def Create(resource):
		result = None
		enumerator = App.CompositionContainer.GetExportedValues().GetEnumerator()
		while enumerator.MoveNext():
			factory = enumerator.Current
			result = factory.CreateNode(resource)
			if result != None:
				break
		return result == ResourceTreeNode(resource)

	Create = staticmethod(Create)