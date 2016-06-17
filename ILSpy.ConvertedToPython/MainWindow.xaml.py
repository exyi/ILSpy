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
from System.Collections.Specialized import *
from System.ComponentModel import *
from System.ComponentModel.Composition import *
from System.Diagnostics import *
from System.IO import *
from System.Linq import *
from System.Threading.Tasks import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Input import *
from System.Windows.Interop import *
from System.Windows.Media import *
from System.Windows.Media.Imaging import *
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.TextView import *
from ICSharpCode.ILSpy.TreeNodes import *
from ICSharpCode.ILSpy.XmlDoc import *
from ICSharpCode.TreeView import *
from Microsoft.Win32 import *
from Mono.Cecil import *
from ICSharpCode.Decompiler.Ast import *

class MainWindow(Window):
	""" <summary>
	 The main window of the application.
	 </summary>
	"""
	def get_Instance(self):
		return self._instance

	Instance = property(fget=get_Instance)

	def get_SessionSettings(self):
		return self._sessionSettings

	SessionSettings = property(fget=get_SessionSettings)

	def __init__(self):
		self._history = NavigationHistory[NavigationState]()
		self._decompilerTextView = None
		self._toolbarCommands = None
		self._mainMenuCommands = None
		# Validate and Set Window Bounds
		self._commandLineLoadedAssemblies = List[LoadedAssembly]()
		self._instance = self
		self._spySettings = ILSpySettings.Load()
		self._sessionSettings = SessionSettings(self._spySettings)
		self._assemblyListManager = AssemblyListManager(self._spySettings)
		self._Icon = BitmapImage(Uri("pack://application:,,,/ILSpy;component/images/ILSpy.ico"))
		self._DataContext = self._sessionSettings
		self.InitializeComponent()
		App.CompositionContainer.ComposeParts(self)
		mainPane.Content = self._decompilerTextView
		if self._sessionSettings.SplitterPosition > 0 and self._sessionSettings.SplitterPosition < 1:
			leftColumn.Width = GridLength(self._sessionSettings.SplitterPosition, GridUnitType.Star)
			rightColumn.Width = GridLength(1 - self._sessionSettings.SplitterPosition, GridUnitType.Star)
		self._sessionSettings.FilterSettings.PropertyChanged += self.filterSettings_PropertyChanged
		self.InitMainMenu()
		self.InitToolbar()
		ContextMenuProvider.Add(treeView, self._decompilerTextView)
		self._Loaded += self.MainWindow_Loaded

	def SetWindowBounds(self, bounds):
		self._Left = bounds.Left
		self._Top = bounds.Top
		self._Width = bounds.Width
		self._Height = bounds.Height

	def InitToolbar(self):
		navigationPos = 0
		openPos = 1
		enumerator = self._toolbarCommands.OrderBy().GroupBy().GetEnumerator()
		while enumerator.MoveNext():
			commandGroup = enumerator.Current
			if commandGroup.Key == "Navigation":
				enumerator = commandGroup.GetEnumerator()
				while enumerator.MoveNext():
					command = enumerator.Current
					toolBar.Items.Insert(navigationPos += 1, self.MakeToolbarItem(command))
					openPos += 1
			elif commandGroup.Key == "Open":
				enumerator = commandGroup.GetEnumerator()
				while enumerator.MoveNext():
					command = enumerator.Current
					toolBar.Items.Insert(openPos += 1, self.MakeToolbarItem(command))
			else:
				toolBar.Items.Add(Separator())
				enumerator = commandGroup.GetEnumerator()
				while enumerator.MoveNext():
					command = enumerator.Current
					toolBar.Items.Add(self.MakeToolbarItem(command))

	def MakeToolbarItem(self, command):
		return Button(Command = CommandWrapper.Unwrap(command.Value), ToolTip = command.Metadata.ToolTip, Tag = command.Metadata.Tag, Content = Image(Width = 16, Height = 16, Source = Images.LoadImage(command.Value, command.Metadata.ToolbarIcon)))

	def InitMainMenu(self):
		enumerator = self._mainMenuCommands.OrderBy().GroupBy().GetEnumerator()
		while enumerator.MoveNext():
			topLevelMenu = enumerator.Current
			topLevelMenuItem = mainMenu.Items.OfType().FirstOrDefault()
			enumerator = topLevelMenu.GroupBy().GetEnumerator()
			while enumerator.MoveNext():
				category = enumerator.Current
				if topLevelMenuItem == None:
					topLevelMenuItem = MenuItem()
					topLevelMenuItem.Header = topLevelMenu.Key
					mainMenu.Items.Add(topLevelMenuItem)
				elif topLevelMenuItem.Items.Count > 0:
					topLevelMenuItem.Items.Add(Separator())
				enumerator = category.GetEnumerator()
				while enumerator.MoveNext():
					entry = enumerator.Current
					menuItem = MenuItem()
					menuItem.Command = CommandWrapper.Unwrap(entry.Value)
					if not str.IsNullOrEmpty(entry.Metadata.Header):
						menuItem.Header = entry.Metadata.Header
					if not str.IsNullOrEmpty(entry.Metadata.MenuIcon):
						menuItem.Icon = Image(Width = 16, Height = 16, Source = Images.LoadImage(entry.Value, entry.Metadata.MenuIcon))
					menuItem.IsEnabled = entry.Metadata.IsEnabled
					menuItem.InputGestureText = entry.Metadata.InputGestureText
					topLevelMenuItem.Items.Add(menuItem)

	def OnSourceInitialized(self, e):
		self.OnSourceInitialized(e)
		source = PresentationSource.FromVisual(self)
		hwndSource = source
		if hwndSource != None:
			hwndSource.AddHook(WndProc)
		bounds = Rect.Transform(self._sessionSettings.WindowBounds, source.CompositionTarget.TransformToDevice)
		boundsRect = System.Drawing.Rectangle(bounds.Left, bounds.Top, bounds.Width, bounds.Height)
		boundsOK = False
		enumerator = System.Windows.Forms.Screen.AllScreens.GetEnumerator()
		while enumerator.MoveNext():
			screen = enumerator.Current
			intersection = System.Drawing.Rectangle.Intersect(boundsRect, screen.WorkingArea)
			if intersection.Width > 10 and intersection.Height > 10:
				boundsOK = True
		if boundsOK:
			self.SetWindowBounds(self._sessionSettings.WindowBounds)
		else:
			self.SetWindowBounds(self.SessionSettings.DefaultWindowBounds)
		self._WindowState = self._sessionSettings.WindowState

	def WndProc(self, hwnd, msg, wParam, lParam, handled):
		if msg == NativeMethods.WM_COPYDATA:
			copyData = lParam
			data = System.String(, 0,  / )
			if data.StartsWith("ILSpy:\r\n", StringComparison.Ordinal):
				data = data.Substring(8)
				lines = List[str]()
				args = CommandLineArguments(lines)
				if self.HandleCommandLineArguments(args):
					if not args.NoActivate and WindowState == WindowState.Minimized:
						WindowState = WindowState.Normal
					self.HandleCommandLineArgumentsAfterShowList(args)
					handled = True
					return 1
		return IntPtr.Zero

	def get_CurrentAssemblyList(self):
		return self._assemblyList

	CurrentAssemblyList = property(fget=get_CurrentAssemblyList)

	def HandleCommandLineArguments(self, args):
		enumerator = args.AssembliesToLoad.GetEnumerator()
		while enumerator.MoveNext():
			file = enumerator.Current
			self._commandLineLoadedAssemblies.Add(self._assemblyList.OpenAssembly(file))
		if args.Language != None:
			self._sessionSettings.FilterSettings.Language = Languages.GetLanguage(args.Language)
		return True

	def HandleCommandLineArgumentsAfterShowList(self, args):
		# if a SaveDirectory is given, do not start a second concurrent decompilation
		# by executing JumpoToReference (leads to https://github.com/icsharpcode/ILSpy/issues/710)
		if not str.IsNullOrEmpty(args.SaveDirectory):
			enumerator = commandLineLoadedAssemblies.GetEnumerator()
			while enumerator.MoveNext():
				x = enumerator.Current
				x.ContinueWhenLoaded(, TaskScheduler.FromCurrentSynchronizationContext())
		elif args.NavigateTo != None:
			found = False
			if args.NavigateTo.StartsWith("N:", StringComparison.Ordinal):
				namespaceName = args.NavigateTo.Substring(2)
				enumerator = commandLineLoadedAssemblies.GetEnumerator()
				while enumerator.MoveNext():
					asm = enumerator.Current
					asmNode = self._assemblyListTreeNode.FindAssemblyNode(asm)
					if asmNode != None:
						nsNode = asmNode.FindNamespaceNode(namespaceName)
						if nsNode != None:
							found = True
							self.SelectNode(nsNode)
							break
			else:
				enumerator = commandLineLoadedAssemblies.GetEnumerator()
				while enumerator.MoveNext():
					asm = enumerator.Current
					def = asm.ModuleDefinition
					if def != None:
						mr = XmlDocKeyProvider.FindMemberByKey(def, args.NavigateTo)
						if mr != None:
							found = True
							self.JumpToReference(mr)
							break
			if not found:
				output = AvalonEditTextOutput()
				output.Write(str.Format("Cannot find '{0}' in command line specified assemblies.", args.NavigateTo))
				self._decompilerTextView.ShowText(output)
		elif self._commandLineLoadedAssemblies.Count == 1:
			# NavigateTo == null and an assembly was given on the command-line:
			# Select the newly loaded assembly
			self.JumpToReference(self._commandLineLoadedAssemblies[0].ModuleDefinition)
		if args.Search != None:
			SearchPane.Instance.SearchTerm = args.Search
			SearchPane.Instance.Show()
		self._commandLineLoadedAssemblies.Clear()
 # clear references once we don't need them anymore
	def OnExportAssembly(self, moduleTask, path):
		asmNode = self._assemblyListTreeNode.FindAssemblyNode(moduleTask.Result)
		if asmNode != None:
			file = DecompilerTextView.CleanUpName(asmNode.LoadedAssembly.ShortName)
			language = self._sessionSettings.FilterSettings.Language
			options = DecompilationOptions()
			options.FullDecompilation = True
			options.SaveAsProjectDirectory = Path.Combine(App.CommandLineArguments.SaveDirectory, file)
			if not Directory.Exists(options.SaveAsProjectDirectory):
				Directory.CreateDirectory(options.SaveAsProjectDirectory)
			fullFile = Path.Combine(options.SaveAsProjectDirectory, file + language.ProjectFileExtension)
			TextView.SaveToDisk(language, Array[]((asmNode)), options, fullFile)

	def MainWindow_Loaded(self, sender, e):
		spySettings = self._spySettings
		self._spySettings = None
		# Load AssemblyList only in Loaded event so that WPF is initialized before we start the CPU-heavy stuff.
		# This makes the UI come up a bit faster.
		self._assemblyList = self._assemblyListManager.LoadList(self._spySettings, self._sessionSettings.ActiveAssemblyList)
		self.HandleCommandLineArguments(App.CommandLineArguments)
		if self._assemblyList.GetAssemblies().Length == 0 and self._assemblyList.ListName == AssemblyListManager.DefaultListName:
			self.LoadInitialAssemblies()
		self.ShowAssemblyList(self._assemblyList)
		self.HandleCommandLineArgumentsAfterShowList(App.CommandLineArguments)
		if App.CommandLineArguments.NavigateTo == None and App.CommandLineArguments.AssembliesToLoad.Count != 1:
			node = None
			if self._sessionSettings.ActiveTreeViewPath != None:
				node = self.FindNodeByPath(self._sessionSettings.ActiveTreeViewPath, True)
				if node == self._assemblyListTreeNode & self._sessionSettings.ActiveAutoLoadedAssembly != None:
					self._assemblyList.OpenAssembly(self._sessionSettings.ActiveAutoLoadedAssembly, True)
					node = self.FindNodeByPath(self._sessionSettings.ActiveTreeViewPath, True)
			if node != None:
				self.SelectNode(node)
				# only if not showing the about page, perform the update check:
				self.ShowMessageIfUpdatesAvailableAsync(self._spySettings)
			else:
				AboutPage.Display(self._decompilerTextView)
		output = AvalonEditTextOutput()
		if self.FormatExceptions(App.StartupExceptions.ToArray(), output):
			self._decompilerTextView.ShowText(output)

	def FormatExceptions(self, exceptions, output):
		if exceptions.Length == 0:
			return False
		first = True
		enumerator = exceptions.GetEnumerator()
		while enumerator.MoveNext():
			item = enumerator.Current
			if first:
				first = False
			else:
				output.WriteLine("-------------------------------------------------")
			output.WriteLine("Error(s) loading plugin: " + item.PluginName)
			if :
				e = item.Exception
				enumerator = e.LoaderExceptions.GetEnumerator()
				while enumerator.MoveNext():
					ex = enumerator.Current
					output.WriteLine(ex.ToString())
					output.WriteLine()
			else:
				output.WriteLine(item.Exception.ToString())
		return True

	def ShowMessageIfUpdatesAvailableAsync(self, spySettings, forceCheck):
		if forceCheck:
			result = AboutPage.CheckForUpdatesAsync(spySettings)
		else:
			result = AboutPage.CheckForUpdatesIfEnabledAsync(spySettings)
		result.ContinueWith(, TaskScheduler.FromCurrentSynchronizationContext())

	def updatePanelCloseButtonClick(self, sender, e):
		updatePanel.Visibility = Visibility.Collapsed

	def downloadOrCheckUpdateButtonClick(self, sender, e):
		if self._updateAvailableDownloadUrl != None:
			Process.Start(self._updateAvailableDownloadUrl)
		else:
			updatePanel.Visibility = Visibility.Collapsed
			AboutPage.CheckForUpdatesAsync(self._spySettings == ILSpySettings.Load()).ContinueWith(, TaskScheduler.FromCurrentSynchronizationContext())

	def AdjustUpdateUIAfterCheck(self, task, displayMessage):
		self._updateAvailableDownloadUrl = task.Result
		updatePanel.Visibility = Visibility.Visible if displayMessage else Visibility.Collapsed
		if task.Result != None:
			updatePanelMessage.Text = "A new ILSpy version is available."
			downloadOrCheckUpdateButton.Content = "Download"
		else:
			updatePanelMessage.Text = "No update for ILSpy found."
			downloadOrCheckUpdateButton.Content = "Check again"

	def ShowAssemblyList(self, name):
		settings = self._spySettings
		if settings == None:
			settings = ILSpySettings.Load()
		list = self._assemblyListManager.LoadList(settings, name)
		#Only load a new list when it is a different one
		if list.ListName != self.CurrentAssemblyList.ListName:
			self.ShowAssemblyList(list)

	def ShowAssemblyList(self, assemblyList):
		self._history.Clear()
		self._assemblyList = assemblyList
		assemblyList.assemblies.CollectionChanged += self.assemblyList_Assemblies_CollectionChanged
		self._assemblyListTreeNode = AssemblyListTreeNode(assemblyList)
		self._assemblyListTreeNode.FilterSettings = self._sessionSettings.FilterSettings.Clone()
		self._assemblyListTreeNode.Select = SelectNode
		treeView.Root = self._assemblyListTreeNode
		if assemblyList.ListName == AssemblyListManager.DefaultListName:
			self._Title = "ILSpy"
		else:
			self._Title = "ILSpy - " + assemblyList.ListName

	def assemblyList_Assemblies_CollectionChanged(self, sender, e):
		if e.Action == NotifyCollectionChangedAction.Reset:
			self._history.RemoveAll()
		if e.OldItems != None:
			oldAssemblies = HashSet[LoadedAssembly](e.OldItems.Cast())
			self._history.RemoveAll()
		if CurrentAssemblyListChanged != None:
			self.CurrentAssemblyListChanged(self, e)

	def LoadInitialAssemblies(self):
		# Called when loading an empty assembly list; so that
		# the user can see something initially.
		initialAssemblies = 
		enumerator = initialAssemblies.GetEnumerator()
		while enumerator.MoveNext():
			asm = enumerator.Current
			self._assemblyList.OpenAssembly(asm.Location)

	def filterSettings_PropertyChanged(self, sender, e):
		self.RefreshTreeViewFilter()
		if e.PropertyName == "Language":
			self.DecompileSelectedNodes(recordHistory = False)

	def RefreshTreeViewFilter(self):
		# filterSettings is mutable; but the ILSpyTreeNode filtering assumes that filter settings are immutable.
		# Thus, the main window will use one mutable instance (for data-binding), and assign a new clone to the ILSpyTreeNodes whenever the main
		# mutable instance changes.
		if self._assemblyListTreeNode != None:
			self._assemblyListTreeNode.FilterSettings = self._sessionSettings.FilterSettings.Clone()

	def get_AssemblyListTreeNode(self):
		return self._assemblyListTreeNode

	AssemblyListTreeNode = property(fget=get_AssemblyListTreeNode)

	def SelectNode(self, obj):
		if obj != None:
			if not obj.AncestorsAndSelf().Any():
				# Set both the selection and focus to ensure that keyboard navigation works as expected.
				treeView.FocusNode(obj)
				treeView.SelectedItem = obj
			else:
				MessageBox.Show("Navigation failed because the target is hidden or a compiler-generated class.\n" + "Please disable all filters that might hide the item (i.e. activate " + "\"View > Show internal types and members\") and try again.", "ILSpy", MessageBoxButton.OK, MessageBoxImage.Exclamation)

	def SelectNodes(self, nodes):
		if nodes.Any() and nodes.All():
			treeView.FocusNode(nodes.First())
			treeView.SetSelectedNodes(nodes)

	def FindNodeByPath(self, path, returnBestMatch):
		""" <summary>
		 Retrieves a node using the .ToString() representations of its ancestors.
		 </summary>
		"""
		if path == None:
			return None
		node = treeView.Root
		bestMatch = node
		enumerator = path.GetEnumerator()
		while enumerator.MoveNext():
			element = enumerator.Current
			if node == None:
				break
			bestMatch = node
			node.EnsureLazyChildren()
			node = node.Children.FirstOrDefault()
		if returnBestMatch:
			return node == bestMatch
		else:
			return node

	def GetPathForNode(node):
		""" <summary>
		 Gets the .ToString() representation of the node's ancestors.
		 </summary>
		"""
		if node == None:
			return None
		path = List[str]()
		while node.Parent != None:
			path.Add(node.ToString())
			node = node.Parent
		path.Reverse()
		return path.ToArray()

	GetPathForNode = staticmethod(GetPathForNode)

	def FindTreeNode(self, reference):
		if :
			return self._assemblyListTreeNode.FindTypeNode((reference).Resolve())
		elif :
			return self._assemblyListTreeNode.FindMethodNode((reference).Resolve())
		elif :
			return self._assemblyListTreeNode.FindFieldNode((reference).Resolve())
		elif :
			return self._assemblyListTreeNode.FindPropertyNode((reference).Resolve())
		elif :
			return self._assemblyListTreeNode.FindEventNode((reference).Resolve())
		elif :
			return self._assemblyListTreeNode.FindAssemblyNode(reference)
		elif :
			return self._assemblyListTreeNode.FindAssemblyNode(reference)
		elif :
			return self._assemblyListTreeNode.FindResourceNode(reference)
		else:
			return None

	def JumpToReference(self, reference):
		self.JumpToReferenceAsync(reference).HandleExceptions()

	def JumpToReferenceAsync(self, reference):
		""" <summary>
		 Jumps to the specified reference.
		 </summary>
		 <returns>
		 Returns a task that will signal completion when the decompilation of the jump target has finished.
		 The task will be marked as canceled if the decompilation is canceled.
		 </returns>
		"""
		self._decompilationTask = TaskHelper.CompletedTask
		treeNode = self.FindTreeNode(reference)
		if treeNode != None:
			self.SelectNode(treeNode)
		elif :
			link = "http://msdn.microsoft.com/library/system.reflection.emit.opcodes." + (reference).Code.ToString().ToLowerInvariant() + ".aspx"
			try:
				Process.Start(link)
			except , :
			finally:
		return self._decompilationTask

	def OpenCommandExecuted(self, sender, e):
		e.Handled = True
		dlg = OpenFileDialog()
		dlg.Filter = ".NET assemblies|*.dll;*.exe;*.winmd|All files|*.*"
		dlg.Multiselect = True
		dlg.RestoreDirectory = True
		if dlg.ShowDialog() == True:
			self.OpenFiles(dlg.FileNames)

	def OpenFiles(self, fileNames, focusNode):
		if fileNames == None:
			raise ArgumentNullException("fileNames")
		if focusNode:
			treeView.UnselectAll()
		lastNode = None
		enumerator = fileNames.GetEnumerator()
		while enumerator.MoveNext():
			file = enumerator.Current
			asm = self._assemblyList.OpenAssembly(file)
			if asm != None:
				node = self._assemblyListTreeNode.FindAssemblyNode(asm)
				if node != None and focusNode:
					treeView.SelectedItems.Add(node)
					lastNode = node
			if lastNode != None and focusNode:
				treeView.FocusNode(lastNode)

	def RefreshCommandExecuted(self, sender, e):
		path = self.GetPathForNode(treeView.SelectedItem)
		self.ShowAssemblyList(self._assemblyListManager.LoadList(ILSpySettings.Load(), self._assemblyList.ListName))
		self.SelectNode(self.FindNodeByPath(path, True))

	def SearchCommandExecuted(self, sender, e):
		SearchPane.Instance.Show()

	def TreeView_SelectionChanged(self, sender, e):
		self.DecompileSelectedNodes()
		if SelectionChanged != None:
			self.SelectionChanged(sender, e)