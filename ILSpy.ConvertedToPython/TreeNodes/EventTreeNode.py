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
from System.Windows.Media import *
from ICSharpCode.Decompiler import *
from Mono.Cecil import *

class EventTreeNode(ILSpyTreeNode, IMemberTreeNode):
	""" <summary>
	 Represents an event in the TreeView.
	 </summary>
	"""
	def __init__(self, ev):
		if ev == None:
			raise ArgumentNullException("ev")
		self._ev = ev
		if ev.AddMethod != None:
			self._Children.Add(MethodTreeNode(ev.AddMethod))
		if ev.RemoveMethod != None:
			self._Children.Add(MethodTreeNode(ev.RemoveMethod))
		if ev.InvokeMethod != None:
			self._Children.Add(MethodTreeNode(ev.InvokeMethod))
		if ev.HasOtherMethods:
			enumerator = ev.OtherMethods.GetEnumerator()
			while enumerator.MoveNext():
				m = enumerator.Current
				self._Children.Add(MethodTreeNode(m))

	def get_EventDefinition(self):
		return ev

	EventDefinition = property(fget=get_EventDefinition)

	def get_Text(self):
		return self.GetText(ev, self._Language) + ev.MetadataToken.ToSuffixString()

	Text = property(fget=get_Text)

	def GetText(eventDef, language):
		return EventTreeNode.HighlightSearchMatch(eventDef.Name, " : " + language.TypeToString(eventDef.EventType, False, eventDef))

	GetText = staticmethod(GetText)

	def get_Icon(self):
		return self.GetIcon(self._ev)

	Icon = property(fget=get_Icon)

	def GetIcon(eventDef):
		accessor = eventDef.AddMethod == eventDef.RemoveMethod
		if accessor != None:
			return Images.GetIcon(MemberIcon.Event, EventTreeNode.GetOverlayIcon(eventDef.AddMethod.Attributes), eventDef.AddMethod.IsStatic)
		else:
			return Images.GetIcon(MemberIcon.Event, AccessOverlayIcon.Public, False)

	GetIcon = staticmethod(GetIcon)

	def GetOverlayIcon(methodAttributes):
		if methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Public:
			return AccessOverlayIcon.Public
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Assembly or methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.FamANDAssem:
			return AccessOverlayIcon.Internal
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Family:
			return AccessOverlayIcon.Protected
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.FamORAssem:
			return AccessOverlayIcon.ProtectedInternal
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.Private:
			return AccessOverlayIcon.Private
		elif methodAttributes & MethodAttributes.MemberAccessMask == MethodAttributes.CompilerControlled:
			return AccessOverlayIcon.CompilerControlled
		else:
			raise NotSupportedException()

	GetOverlayIcon = staticmethod(GetOverlayIcon)

	def Filter(self, settings):
		if settings.SearchTermMatches(self._ev.Name) and settings.Language.ShowMember(self._ev):
			return FilterResult.Match
		else:
			return FilterResult.Hidden

	def Decompile(self, language, output, options):
		language.DecompileEvent(self._ev, output, options)

	def get_IsPublicAPI(self):
		accessor = self._ev.AddMethod == self._ev.RemoveMethod
		return accessor != None and (accessor.IsPublic or accessor.IsFamilyOrAssembly or accessor.IsFamily)

	IsPublicAPI = property(fget=get_IsPublicAPI)

	def get_Member(self):
		return self._ev

	Member = property(fget=get_Member)