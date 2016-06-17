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
from System.Linq import *
from System.Threading.Tasks import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Documents import *
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.TextView import *
from ICSharpCode.TreeView import *
from Microsoft.Win32 import *
from Mono.Cecil import *

class AssemblyTreeNode(ILSpyTreeNode):
	""" <summary>
	 Tree node representing an assembly.
	 This class is responsible for loading both namespace and type nodes.
	 </summary>
	"""
	def __init__(self, assembly):
		self._namespaces = Dictionary[str, NamespaceTreeNode]()
		# change from "Loading" icon to final icon # cannot expand assemblies with load error
		# observe the exception so that the Task's finalizer doesn't re-throw it # shortname might have changed
		self._typeDict = Dictionary[TypeDefinition, TypeTreeNode]()
		# if we crashed on loading, then we don't have any children
		# <summary>
		# Finds the node for a top-level type.
		# </summary>
		# <summary>
		# Finds the node for a namespace.
		# </summary>
		self._DataFormat = "ILSpyAssemblies"
		if assembly == None:
			raise ArgumentNullException("assembly")
		self._assembly = assembly
		assembly.ContinueWhenLoaded(OnAssemblyLoaded, TaskScheduler.FromCurrentSynchronizationContext())
		self._LazyLoading = True

	def get_AssemblyList(self):
		return assembly.AssemblyList

	AssemblyList = property(fget=get_AssemblyList)

	def get_LoadedAssembly(self):
		return assembly

	LoadedAssembly = property(fget=get_LoadedAssembly)

	def get_IsAutoLoaded(self):
		return assembly.IsAutoLoaded

	IsAutoLoaded = property(fget=get_IsAutoLoaded)

	def get_Text(self):
		return self.HighlightSearchMatch(assembly.Text)

	Text = property(fget=get_Text)

	def get_Icon(self):
		if assembly.IsLoaded:
			return Images.AssemblyWarning if assembly.HasLoadError else Images.Assembly
		else:
			return Images.AssemblyLoading

	Icon = property(fget=get_Icon)

	def get_ToolTip(self):
		if assembly.HasLoadError:
			return "Assembly could not be loaded. Click here for details."
		if self._tooltip == None:
			self._tooltip = TextBlock()
			self._tooltip.Inlines.Add(Bold(Run("Name: ")))
			self._tooltip.Inlines.Add(Run(assembly.AssemblyDefinition.FullName))
			self._tooltip.Inlines.Add(LineBreak())
			self._tooltip.Inlines.Add(Bold(Run("Location: ")))
			self._tooltip.Inlines.Add(Run(assembly.FileName))
			self._tooltip.Inlines.Add(LineBreak())
			self._tooltip.Inlines.Add(Bold(Run("Architecture: ")))
			self._tooltip.Inlines.Add(Run(CSharpLanguage.GetPlatformDisplayName(assembly.AssemblyDefinition.MainModule)))
			runtimeName = CSharpLanguage.GetRuntimeDisplayName(assembly.AssemblyDefinition.MainModule)
			if runtimeName != None:
				self._tooltip.Inlines.Add(LineBreak())
				self._tooltip.Inlines.Add(Bold(Run("Runtime: ")))
				self._tooltip.Inlines.Add(Run(runtimeName))
		return self._tooltip

	ToolTip = property(fget=get_ToolTip)

	def get_ShowExpander(self):
		return not assembly.HasLoadError

	ShowExpander = property(fget=get_ShowExpander)

	def OnAssemblyLoaded(self, moduleTask):
		self.RaisePropertyChanged("Icon")
		self.RaisePropertyChanged("ExpandedIcon")
		if moduleTask.IsFaulted:
			self.RaisePropertyChanged("ShowExpander")
			try:
				moduleTask.Wait()
			except AggregateException, :
			finally:
		else:
			self.RaisePropertyChanged("Text")

	def LoadChildren(self):
		moduleDefinition = self._assembly.ModuleDefinition
		if moduleDefinition == None:
			return 
		self._Children.Add(ReferenceFolderTreeNode(moduleDefinition, self))
		if moduleDefinition.HasResources:
			self._Children.Add(ResourceListTreeNode(moduleDefinition))
		enumerator = self._namespaces.Values.GetEnumerator()
		while enumerator.MoveNext():
			ns = enumerator.Current
			ns.Children.Clear()
		enumerator = moduleDefinition.Types.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			type = enumerator.Current
			if not self._namespaces.TryGetValue(type.Namespace, ):
				ns = NamespaceTreeNode(type.Namespace)
				self._namespaces[type.Namespace] = ns
			node = TypeTreeNode(type, self)
			self._typeDict[type] = node
			ns.Children.Add(node)
		enumerator = self._namespaces.Values.OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			ns = enumerator.Current
			if ns.Children.Count > 0:
				self._Children.Add(ns)

	def get_CanExpandRecursively(self):
		return True

	CanExpandRecursively = property(fget=get_CanExpandRecursively)

	def FindTypeNode(self, def):
		if def == None:
			return None
		self.EnsureLazyChildren()
		if self._typeDict.TryGetValue(def, ):
			return node
		else:
			return None

	def FindNamespaceNode(self, namespaceName):
		if str.IsNullOrEmpty(namespaceName):
			return None
		self.EnsureLazyChildren()
		if self._namespaces.TryGetValue(namespaceName, ):
			return node
		else:
			return None

	def CanDrag(self, nodes):
		return nodes.All()

	def StartDrag(self, dragSource, nodes):
		DragDrop.DoDragDrop(dragSource, self.Copy(nodes), DragDropEffects.All)

	def CanDelete(self):
		return True

	def Delete(self):
		self.DeleteCore()

	def DeleteCore(self):
		self._assembly.AssemblyList.Unload(self._assembly)

	def Copy(self, nodes):
		dataObject = DataObject()
		dataObject.SetData(self._DataFormat, nodes.OfType().Select().ToArray())
		return dataObject

	def Filter(self, settings):
		if settings.SearchTermMatches(self._assembly.ShortName):
			return FilterResult.Match
		else:
			return FilterResult.Recurse

	def Decompile(self, language, output, options):
		try:
			self._assembly.WaitUntilLoaded()
		except AggregateException, ex: # necessary so that load errors are passed on to the caller
			language.WriteCommentLine(output, self._assembly.FileName)
			if :
				language.WriteCommentLine(output, "This file does not contain a managed assembly.")
				return 
			else:
				raise 
		finally:
		language.DecompileAssembly(self._assembly, output, options)

	def Save(self, textView):
		language = self._Language
		if str.IsNullOrEmpty(language.ProjectFileExtension):
			return False
		dlg = SaveFileDialog()
		dlg.FileName = DecompilerTextView.CleanUpName(self._assembly.ShortName) + language.ProjectFileExtension
		dlg.Filter = language.Name + " project|*" + language.ProjectFileExtension + "|" + language.Name + " single file|*" + language.FileExtension + "|All files|*.*"
		if dlg.ShowDialog() == True:
			options = DecompilationOptions()
			options.FullDecompilation = True
			if dlg.FilterIndex == 1:
				options.SaveAsProjectDirectory = Path.GetDirectoryName(dlg.FileName)
				enumerator = Directory.GetFileSystemEntries(options.SaveAsProjectDirectory).GetEnumerator()
				while enumerator.MoveNext():
					entry = enumerator.Current
					if not str.Equals(entry, dlg.FileName, StringComparison.OrdinalIgnoreCase):
						result = MessageBox.Show("The directory is not empty. File will be overwritten." + Environment.NewLine + "Are you sure you want to continue?", "Project Directory not empty", MessageBoxButton.YesNo, MessageBoxImage.Question, MessageBoxResult.No)
						if result == MessageBoxResult.No:
							return True # don't save, but mark the Save operation as handled
						break
			textView.SaveToDisk(language, Array[]((self)), options, dlg.FileName)
		return True

class RemoveAssembly(IContextMenuEntry):
	def IsVisible(self, context):
		if context.SelectedTreeNodes == None:
			return False
		return context.SelectedTreeNodes.All()

	def IsEnabled(self, context):
		return True

	def Execute(self, context):
		if context.SelectedTreeNodes == None:
			return 
		enumerator = context.SelectedTreeNodes.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			node.Delete()

class ReloadAssembly(IContextMenuEntry):
	def IsVisible(self, context):
		if context.SelectedTreeNodes == None:
			return False
		return context.SelectedTreeNodes.All()

	def IsEnabled(self, context):
		return True

	def Execute(self, context):
		if context.SelectedTreeNodes == None:
			return 
		paths = List[Array[str]]()
		MainWindow.Instance.SelectNodes(paths.Select().ToArray())
		MainWindow.Instance.RefreshDecompiledView()

class LoadDependencies(IContextMenuEntry):
	def IsVisible(self, context):
		if context.SelectedTreeNodes == None:
			return False
		return context.SelectedTreeNodes.All()

	def IsEnabled(self, context):
		return True

	def Execute(self, context):
		if context.SelectedTreeNodes == None:
			return 
		enumerator = context.SelectedTreeNodes.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			la = (node).LoadedAssembly
			if not la.HasLoadError:
				enumerator = la.ModuleDefinition.AssemblyReferences.GetEnumerator()
				while enumerator.MoveNext():
					assyRef = enumerator.Current
					la.LookupReferencedAssembly(assyRef.FullName)
		MainWindow.Instance.RefreshDecompiledView()

class AddToMainList(IContextMenuEntry):
	def IsVisible(self, context):
		if context.SelectedTreeNodes == None:
			return False
		return context.SelectedTreeNodes.Where().Any()

	def IsEnabled(self, context):
		return True

	def Execute(self, context):
		if context.SelectedTreeNodes == None:
			return 
		enumerator = context.SelectedTreeNodes.GetEnumerator()
		while enumerator.MoveNext():
			node = enumerator.Current
			loadedAssm = (node).LoadedAssembly
			if not loadedAssm.HasLoadError:
				loadedAssm.IsAutoLoaded = False
				node.RaisePropertyChanged("Foreground")
		MainWindow.Instance.CurrentAssemblyList.RefreshSave()