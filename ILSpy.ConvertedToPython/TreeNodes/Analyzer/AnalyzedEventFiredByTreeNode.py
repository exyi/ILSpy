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
from System.Collections.Concurrent import *
from System.Collections.Generic import *
from System.Linq import *
from System.Threading import *
from Mono.Cecil import *
from Mono.Cecil.Cil import *

class AnalyzedEventFiredByTreeNode(AnalyzerSearchTreeNode):
	def __init__(self, analyzedEvent):
		if analyzedEvent == None:
			raise ArgumentNullException("analyzedEvent")
		self._analyzedEvent = analyzedEvent
		self._eventBackingField = self.GetBackingField(analyzedEvent)
		self._eventFiringMethod = analyzedEvent.EventType.Resolve().Methods.First()

	def get_Text(self):
		return "Raised By"

	Text = property(fget=get_Text)

	def FetchChildren(self, ct):
		self._foundMethods = ConcurrentDictionary[MethodDefinition, int]()
		enumerator = self.FindReferencesInType(self._analyzedEvent.DeclaringType).OrderBy().GetEnumerator()
		while enumerator.MoveNext():
			child = enumerator.Current
		self._foundMethods = None

	def FindReferencesInType(self, type):
		# HACK: in lieu of proper flow analysis, I'm going to use a simple heuristic
		# If the method accesses the event's backing field, and calls invoke on a delegate 
		# with the same signature, then it is (most likely) raise the given event.
		enumerator = type.Methods.GetEnumerator()
		while enumerator.MoveNext():
			method = enumerator.Current
			readBackingField = False
			found = False
			if not method.HasBody:
				continue
			enumerator = method.Body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				instr = enumerator.Current
				code = instr.OpCode.Code
				if code == Code.Ldfld or code == Code.Ldflda:
					fr = instr.Operand
					if fr != None and fr.Name == self._eventBackingField.Name and fr == self._eventBackingField:
						readBackingField = True
				if readBackingField and (code == Code.Callvirt or code == Code.Call):
					mr = instr.Operand
					if mr != None and mr.Name == self._eventFiringMethod.Name and mr.Resolve() == self._eventFiringMethod:
						found = True
						break
			method.Body = None
			if found:
				codeLocation = self._Language.GetOriginalCodeLocation(method)
				if codeLocation != None and not self.HasAlreadyBeenFound(codeLocation):
					node = AnalyzedMethodTreeNode(codeLocation)
					node.Language = self._Language

	def HasAlreadyBeenFound(self, method):
		return not self._foundMethods.TryAdd(method, 0)

	# HACK: we should probably examine add/remove methods to determine this
	def GetBackingField(ev):
		fieldName = ev.Name
		vbStyleFieldName = fieldName + "Event"
		fieldType = ev.EventType
		enumerator = ev.DeclaringType.Fields.GetEnumerator()
		while enumerator.MoveNext():
			fd = enumerator.Current
			if fd.Name == fieldName or fd.Name == vbStyleFieldName:
				if fd.FieldType.FullName == fieldType.FullName:
					return fd
		return None

	GetBackingField = staticmethod(GetBackingField)

	def CanShow(ev):
		return AnalyzedEventFiredByTreeNode.GetBackingField(ev) != None

	CanShow = staticmethod(CanShow)