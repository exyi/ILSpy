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
from System.ComponentModel import *
from System.ComponentModel.Composition import *
from System.Diagnostics import *
from System.IO import *
from System.Linq import *
from System.Net import *
from System.Text.RegularExpressions import *
from System.Threading.Tasks import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Data import *
from System.Windows.Input import *
from System.Xml.Linq import *
from ICSharpCode.AvalonEdit.Rendering import *
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.TextView import *

class AboutPage(SimpleCommand):
	def __init__(self):
		self._decompilerTextView = None
		self._UpdateUrl = Uri("http://www.ilspy.net/updates.xml")
		self._band = "stable"
		# we already retrieved the latest version sometime earlier
		self._currentVersion = Version(RevisionClass.Major + "." + RevisionClass.Minor + "." + RevisionClass.Build + "." + RevisionClass.Revision)

	def Execute(self, parameter):
		MainWindow.Instance.UnselectAll()
		self.Display(self._decompilerTextView)

	def Display(textView):
		output = AvalonEditTextOutput()
		output.WriteLine("ILSpy version " + RevisionClass.FullVersion)
		output.AddUIElement()
		output.WriteLine()
		enumerator = App.CompositionContainer.GetExportedValues().GetEnumerator()
		while enumerator.MoveNext():
			plugin = enumerator.Current
			plugin.Write(output)
		output.WriteLine()
		output.AddVisualLineElementGenerator(MyLinkElementGenerator("SharpDevelop", "http://www.icsharpcode.net/opensource/sd/"))
		output.AddVisualLineElementGenerator(MyLinkElementGenerator("MIT License", "resource:license.txt"))
		output.AddVisualLineElementGenerator(MyLinkElementGenerator("LGPL", "resource:LGPL.txt"))
		output.AddVisualLineElementGenerator(MyLinkElementGenerator("MS-PL", "resource:MS-PL.txt"))
		textView.ShowText(output)

	Display = staticmethod(Display)

	class MyLinkElementGenerator(LinkElementGenerator):
		def __init__(self, matchText, url):
			self._uri = Uri(url)
			self._RequireControlModifierForClick = False

		def GetUriFromMatch(self, match):
			return self._uri

	def AddUpdateCheckButton(stackPanel, textView):
		button = Button()
		button.Content = "Check for updates"
		button.Cursor = Cursors.Arrow
		stackPanel.Children.Add(button)
		button.Click += 

	AddUpdateCheckButton = staticmethod(AddUpdateCheckButton)

	def ShowAvailableVersion(availableVersion, stackPanel):
		if currentVersion == availableVersion.Version:
			stackPanel.Children.Add(Image(Width = 16, Height = 16, Source = Images.OK, Margin = Thickness(4, 0, 4, 0)))
			stackPanel.Children.Add(TextBlock(Text = "You are using the latest release.", VerticalAlignment = VerticalAlignment.Bottom))
		elif currentVersion < availableVersion.Version:
			stackPanel.Children.Add(TextBlock(Text = "Version " + availableVersion.Version + " is available.", Margin = Thickness(0, 0, 8, 0), VerticalAlignment = VerticalAlignment.Bottom))
			if availableVersion.DownloadUrl != None:
				button = Button()
				button.Content = "Download"
				button.Cursor = Cursors.Arrow
				button.Click += 
				stackPanel.Children.Add(button)
		else:
			stackPanel.Children.Add(TextBlock(Text = "You are using a nightly build newer than the latest release."))

	ShowAvailableVersion = staticmethod(ShowAvailableVersion)

	def GetLatestVersionAsync():
		tcs = TaskCompletionSource[AvailableVersionInfo]() # don't accept non-urls
		Action().BeginInvoke(None, None)
		return tcs.Task

	GetLatestVersionAsync = staticmethod(GetLatestVersionAsync)

	class AvailableVersionInfo(object):
		def __init__(self):

	class UpdateSettings(INotifyPropertyChanged):
		def __init__(self, spySettings):
			s = spySettings["UpdateSettings"]
			self._automaticUpdateCheckEnabled = s.Element("AutomaticUpdateCheckEnabled") == True
			try:
				self._lastSuccessfulUpdateCheck = s.Element("LastSuccessfulUpdateCheck")
			except FormatException, :
			finally:

		# avoid crashing on settings files invalid due to
		# https://github.com/icsharpcode/ILSpy/issues/closed/#issue/2
		def get_AutomaticUpdateCheckEnabled(self):
			return self._automaticUpdateCheckEnabled

		def set_AutomaticUpdateCheckEnabled(self, value):
			if self._automaticUpdateCheckEnabled != value:
				self._automaticUpdateCheckEnabled = value
				self.Save()
				self.OnPropertyChanged("AutomaticUpdateCheckEnabled")

		AutomaticUpdateCheckEnabled = property(fget=get_AutomaticUpdateCheckEnabled, fset=set_AutomaticUpdateCheckEnabled)

		def get_LastSuccessfulUpdateCheck(self):
			return self._lastSuccessfulUpdateCheck

		def set_LastSuccessfulUpdateCheck(self, value):
			if self._lastSuccessfulUpdateCheck != value:
				self._lastSuccessfulUpdateCheck = value
				self.Save()
				self.OnPropertyChanged("LastSuccessfulUpdateCheck")

		LastSuccessfulUpdateCheck = property(fget=get_LastSuccessfulUpdateCheck, fset=set_LastSuccessfulUpdateCheck)

		def Save(self):
			updateSettings = XElement("UpdateSettings")
			updateSettings.Add(XElement("AutomaticUpdateCheckEnabled", self._automaticUpdateCheckEnabled))
			if self._lastSuccessfulUpdateCheck != None:
				updateSettings.Add(XElement("LastSuccessfulUpdateCheck", self._lastSuccessfulUpdateCheck))
			ILSpySettings.SaveSettings(updateSettings)

		def OnPropertyChanged(self, propertyName):
			if PropertyChanged != None:
				self.PropertyChanged(self, PropertyChangedEventArgs(propertyName))

	def CheckForUpdatesIfEnabledAsync(spySettings):
		""" <summary>
		 If automatic update checking is enabled, checks if there are any updates available.
		 Returns the download URL if an update is available.
		 Returns null if no update is available, or if no check was performed.
		 </summary>
		"""
		tcs = TaskCompletionSource[str]()
		s = UpdateSettings(spySettings)
		if s.AutomaticUpdateCheckEnabled:
			# perform update check if we never did one before;
			# or if the last check wasn't in the past 7 days
			if s.LastSuccessfulUpdateCheck == None or s.LastSuccessfulUpdateCheck < DateTime.UtcNow.AddDays(-7) or s.LastSuccessfulUpdateCheck > DateTime.UtcNow:
				AboutPage.CheckForUpdateInternal(tcs, s)
			else:
				tcs.SetResult(None)
		else:
			tcs.SetResult(None)
		return tcs.Task

	CheckForUpdatesIfEnabledAsync = staticmethod(CheckForUpdatesIfEnabledAsync)

	def CheckForUpdatesAsync(spySettings):
		tcs = TaskCompletionSource[str]()
		s = UpdateSettings(spySettings)
		AboutPage.CheckForUpdateInternal(tcs, s)
		return tcs.Task

	CheckForUpdatesAsync = staticmethod(CheckForUpdatesAsync)

	def CheckForUpdateInternal(tcs, s):
		AboutPage.GetLatestVersionAsync().ContinueWith()

	CheckForUpdateInternal = staticmethod(CheckForUpdateInternal)

# ignore errors getting the version info
class IAboutPageAddition(object):
	""" <summary>
	 Interface that allows plugins to extend the about page.
	 </summary>
	"""
	def Write(self, textOutput):
		pass