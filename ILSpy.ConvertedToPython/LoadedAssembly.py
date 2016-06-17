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
from System.Threading.Tasks import *
from System.Windows.Threading import *
from ICSharpCode.ILSpy.Options import *
from Mono.Cecil import *
from Mono.Cecil.Cil import *
from System.Linq import *

class LoadedAssembly(object):
	""" <summary>
	 Represents an assembly loaded into ILSpy.
	 </summary>
	"""
	def __init__(self, assemblyList, fileName, stream):
		if assemblyList == None:
			raise ArgumentNullException("assemblyList")
		if fileName == None:
			raise ArgumentNullException("fileName")
		self._assemblyList = assemblyList
		self._fileName = fileName
		self._assemblyTask = Task.Factory.StartNew(LoadAssembly, stream) # requires that this.fileName is set
		self._shortName = Path.GetFileNameWithoutExtension(fileName)

	# <summary>
	# Gets the Cecil ModuleDefinition.
	# Can be null when there was a load error.
	# </summary>
	def get_ModuleDefinition(self):
		try:
			return self._assemblyTask.Result
		except AggregateException, :
			return None
		finally:

	ModuleDefinition = property(fget=get_ModuleDefinition)

	# <summary>
	# Gets the Cecil AssemblyDefinition.
	# Is null when there was a load error; or when opening a netmodule.
	# </summary>
	def get_AssemblyDefinition(self):
		module = self.ModuleDefinition
		return module.Assembly if module != None else None

	AssemblyDefinition = property(fget=get_AssemblyDefinition)

	def get_AssemblyList(self):
		return assemblyList

	AssemblyList = property(fget=get_AssemblyList)

	def get_FileName(self):
		return fileName

	FileName = property(fget=get_FileName)

	def get_ShortName(self):
		return self._shortName

	ShortName = property(fget=get_ShortName)

	def get_Text(self):
		if self.AssemblyDefinition != None:
			return String.Format("{0} ({1})", self.ShortName, self.AssemblyDefinition.Name.Version)
		else:
			return self.ShortName

	Text = property(fget=get_Text)

	def get_IsLoaded(self):
		return self._assemblyTask.IsCompleted

	IsLoaded = property(fget=get_IsLoaded)

	def get_HasLoadError(self):
		return self._assemblyTask.IsFaulted

	HasLoadError = property(fget=get_HasLoadError)

	def get_IsAutoLoaded(self):

	def set_IsAutoLoaded(self, value):

	IsAutoLoaded = property(fget=get_IsAutoLoaded, fset=set_IsAutoLoaded)

	def LoadAssembly(self, state):
		stream = state
		# runs on background thread
		p = ReaderParameters()
		p.AssemblyResolver = MyAssemblyResolver(self)
		if stream != None:
			# Read the module from a precrafted stream
			module = self.ModuleDefinition.ReadModule(stream, p)
		else:
			# Read the module from disk (by default)
			module = self.ModuleDefinition.ReadModule(self._fileName, p)
		if DecompilerSettingsPanel.CurrentDecompilerSettings.UseDebugSymbols:
			try:
				self.LoadSymbols(module)
			except IOException, :
			except UnauthorizedAccessException, :
			except InvalidOperationException, :
			finally:
		# ignore any errors during symbol loading
		return module

	def LoadSymbols(self, module):
		# search for pdb in same directory as dll
		pdbName = Path.Combine(Path.GetDirectoryName(self._fileName), Path.GetFileNameWithoutExtension(self._fileName) + ".pdb")
		if not File.Exists(pdbName):
			pdbName = Path.Combine(Environment.GetEnvironmentVariable("LocalAppData"), "Temp/SymbolCache", Path.GetFileNameWithoutExtension(self._fileName) + ".pdb")
			if Directory.Exists(pdbName):
				pdbName = Directory.GetFiles(pdbName, "*" + Path.GetFileNameWithoutExtension(self._fileName) + ".pdb", SearchOption.AllDirectories).First()
		if File.Exists(pdbName):
			return 

	# TODO: use symbol cache, get symbols from microsoft
	def DisableAssemblyLoad():
		self._assemblyLoadDisableCount += 1
		return DecrementAssemblyLoadDisableCount()

	DisableAssemblyLoad = staticmethod(DisableAssemblyLoad)

	class DecrementAssemblyLoadDisableCount(IDisposable):
		def __init__(self):

		def Dispose(self):
			if not self._disposed:
				self._disposed = True
				assemblyLoadDisableCount -= 1
				# clear the lookup cache since we might have stored the lookups failed due to DisableAssemblyLoad()
				MainWindow.Instance.CurrentAssemblyList.ClearCache()

	class MyAssemblyResolver(IAssemblyResolver):
		def __init__(self, parent):
			self._parent = parent

		def Resolve(self, name):
			node = self._parent.LookupReferencedAssembly(name)
			return node.AssemblyDefinition if node != None else None

		def Resolve(self, name, parameters):
			node = self._parent.LookupReferencedAssembly(name)
			return node.AssemblyDefinition if node != None else None

		def Resolve(self, fullName):
			node = self._parent.LookupReferencedAssembly(fullName)
			return node.AssemblyDefinition if node != None else None

		def Resolve(self, fullName, parameters):
			node = self._parent.LookupReferencedAssembly(fullName)
			return node.AssemblyDefinition if node != None else None

	def GetAssemblyResolver(self):
		return MyAssemblyResolver(self)

	def LookupReferencedAssembly(self, name):
		if name == None:
			raise ArgumentNullException("name")
		if name.IsWindowsRuntime:
			return assemblyList.winRTMetadataLookupCache.GetOrAdd(name.Name, LookupWinRTMetadata)
		else:
			return assemblyList.assemblyLookupCache.GetOrAdd(name.FullName, LookupReferencedAssemblyInternal)

	def LookupReferencedAssembly(self, fullName):
		return assemblyList.assemblyLookupCache.GetOrAdd(fullName, LookupReferencedAssemblyInternal)

	def LookupReferencedAssemblyInternal(self, fullName):
		enumerator = assemblyList.GetAssemblies().GetEnumerator()
		while enumerator.MoveNext():
			asm = enumerator.Current
			if asm.AssemblyDefinition != None and fullName.Equals(asm.AssemblyDefinition.FullName, StringComparison.OrdinalIgnoreCase):
				return asm
		if assemblyLoadDisableCount > 0:
			return None
		if not App.Current.Dispatcher.CheckAccess():
			# Call this method on the GUI thread.
			return App.Current.Dispatcher.Invoke(DispatcherPriority.Normal, Func[str, LoadedAssembly](LookupReferencedAssembly), fullName)
		name = AssemblyNameReference.Parse(fullName)
		file = GacInterop.FindAssemblyInNetGac(name)
		if file == None:
			dir = Path.GetDirectoryName(self._fileName)
			if File.Exists(Path.Combine(dir, name.Name + ".dll")):
				file = Path.Combine(dir, name.Name + ".dll")
			elif File.Exists(Path.Combine(dir, name.Name + ".exe")):
				file = Path.Combine(dir, name.Name + ".exe")
		if file != None:
			loaded = assemblyList.OpenAssembly(file, True)
			return loaded
		else:
			return None

	def LookupWinRTMetadata(self, name):
		enumerator = assemblyList.GetAssemblies().GetEnumerator()
		while enumerator.MoveNext():
			asm = enumerator.Current
			if asm.AssemblyDefinition != None and name.Equals(asm.AssemblyDefinition.Name.Name, StringComparison.OrdinalIgnoreCase):
				return asm
		if assemblyLoadDisableCount > 0:
			return None
		if not App.Current.Dispatcher.CheckAccess():
			# Call this method on the GUI thread.
			return App.Current.Dispatcher.Invoke(DispatcherPriority.Normal, Func[str, LoadedAssembly](LookupWinRTMetadata), name)
		file = Path.Combine(Environment.SystemDirectory, "WinMetadata", name + ".winmd")
		if File.Exists(file):
			return assemblyList.OpenAssembly(file, True)
		else:
			return None

	def ContinueWhenLoaded(self, onAssemblyLoaded, taskScheduler):
		return self._assemblyTask.ContinueWith(onAssemblyLoaded, taskScheduler)

	def WaitUntilLoaded(self):
		""" <summary>
		 Wait until the assembly is loaded.
		 Throws an AggregateException when loading the assembly fails.
		 </summary>
		"""
		assemblyTask.Wait()