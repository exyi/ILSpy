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
from Mono.Cecil import *

class AnalyzedEventTreeNode(AnalyzerEntityTreeNode):
	def __init__(self, analyzedEvent, prefix):
		if analyzedEvent == None:
			raise ArgumentNullException("analyzedEvent")
		self._analyzedEvent = analyzedEvent
		self._prefix = prefix
		self._LazyLoading = True

	def get_Member(self):
		return analyzedEvent

	Member = property(fget=get_Member)

	def get_Icon(self):
		return EventTreeNode.GetIcon(analyzedEvent)

	Icon = property(fget=get_Icon)

	def get_Text(self):
		# TODO: This way of formatting is not suitable for events which explicitly implement interfaces.
		return prefix + Language.TypeToString(analyzedEvent.DeclaringType, True) + "." + EventTreeNode.GetText(analyzedEvent, Language)

	Text = property(fget=get_Text)

	def LoadChildren(self):
		if self._analyzedEvent.AddMethod != None:
			self._Children.Add(AnalyzedEventAccessorTreeNode(self._analyzedEvent.AddMethod, "add"))
		if self._analyzedEvent.RemoveMethod != None:
			self._Children.Add(AnalyzedEventAccessorTreeNode(self._analyzedEvent.RemoveMethod, "remove"))
		enumerator = self._analyzedEvent.OtherMethods.GetEnumerator()
		while enumerator.MoveNext():
			accessor = enumerator.Current
			self._Children.Add(AnalyzedEventAccessorTreeNode(accessor, None))
		if AnalyzedEventFiredByTreeNode.CanShow(self._analyzedEvent):
			self._Children.Add(AnalyzedEventFiredByTreeNode(self._analyzedEvent))
		if AnalyzedEventOverridesTreeNode.CanShow(self._analyzedEvent):
			self._Children.Add(AnalyzedEventOverridesTreeNode(self._analyzedEvent))
		if AnalyzedInterfaceEventImplementedByTreeNode.CanShow(self._analyzedEvent):
			self._Children.Add(AnalyzedInterfaceEventImplementedByTreeNode(self._analyzedEvent))

	def TryCreateAnalyzer(member):
		if AnalyzedEventTreeNode.CanShow(member):
			return AnalyzedEventTreeNode(member)
		else:
			return None

	TryCreateAnalyzer = staticmethod(TryCreateAnalyzer)

	def CanShow(member):
		eventDef = member
		if eventDef == None:
			return False
		return not MainWindow.Instance.CurrentLanguage.ShowMember(eventDef.AddMethod == eventDef.RemoveMethod) or AnalyzedEventOverridesTreeNode.CanShow(eventDef)

	CanShow = staticmethod(CanShow)