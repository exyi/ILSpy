from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Text.RegularExpressions import *
from System.Windows.Media import *
from ICSharpCode.ILSpy.TreeNodes import *
from ICSharpCode.NRefactory.CSharp import *
from ICSharpCode.NRefactory.Utils import *
from Mono.Cecil import *
from Mono.Cecil.Cil import *

class AbstractSearchStrategy(object):
	def __init__(self, terms):
		if terms.Length == 1 and terms[0].Length > 2:
			search = terms[0]
			if search.StartsWith("/", StringComparison.Ordinal) and search.EndsWith("/", StringComparison.Ordinal) and search.Length > 4:
				self._regex = self.SafeNewRegex(search.Substring(1, search.Length - 2))
			terms[0] = search
		self._searchTerm = terms

	def IsMatch(self, text):
		if self._regex != None:
			return self._regex.IsMatch(text)
		i = 0
		while i < self._searchTerm.Length:
			# How to handle overlapping matches?
			term = self._searchTerm[i]
			if str.IsNullOrEmpty(term):
				continue
			if term[0] == '+': # must contain
				term = term.Substring(1)
			elif term[0] == '-': # should not contain
				if term.Length > 1 and text.IndexOf(term.Substring(1), StringComparison.OrdinalIgnoreCase) >= 0:
					return False
			elif term[0] == '=': # exact match
				equalCompareLength = text.IndexOf('`')
				if equalCompareLength == -1:
					equalCompareLength = text.Length
				if term.Length > 1 and String.Compare(term, 1, text, 0, Math.Max(term.Length, equalCompareLength), StringComparison.OrdinalIgnoreCase) != 0:
					return False
			else:
				if text.IndexOf(term, StringComparison.OrdinalIgnoreCase) < 0:
					return False
			i += 1
		return True

	def IsMatch(self, field):
		return False

	def IsMatch(self, property):
		return False

	def IsMatch(self, ev):
		return False

	def IsMatch(self, m):
		return False

	def Add(self, items, type, language, addResult, matcher, image):
		enumerator = items.GetEnumerator()
		while enumerator.MoveNext():
			item = enumerator.Current
			if self.matcher(item):
				self.addResult(SearchResult(Member = item, Image = self.image(item), Name = item.Name, LocationImage = TypeTreeNode.GetIcon(type), Location = language.TypeToString(type, includeNamespace = True)))

	def Search(self, type, language, addResult):
		self.Add(type.Fields, type, language, addResult, IsMatch, FieldTreeNode.GetIcon)
		self.Add(type.Properties, type, language, addResult, IsMatch, )
		self.Add(type.Events, type, language, addResult, IsMatch, EventTreeNode.GetIcon)
		self.Add(type.Methods.Where(NotSpecialMethod), type, language, addResult, IsMatch, MethodTreeNode.GetIcon)

	def NotSpecialMethod(self, arg):
		return (arg.SemanticsAttributes & (MethodSemanticsAttributes.Setter | MethodSemanticsAttributes.Getter | MethodSemanticsAttributes.AddOn | MethodSemanticsAttributes.RemoveOn | MethodSemanticsAttributes.Fire)) == 0

	def SafeNewRegex(self, unsafePattern):
		try:
			return Regex(unsafePattern, RegexOptions.Compiled)
		except ArgumentException, :
			return None
		finally:

class LiteralSearchStrategy(AbstractSearchStrategy):
	def __init__(self, terms):
		if 1 == searchTerm.Length:
			parser = CSharpParser()
			pe = parser.ParseExpression(searchTerm[0])
			if pe != None and pe.Value != None:
				peValueType = Type.GetTypeCode(pe.Value.GetType())
				if peValueType == TypeCode.Byte or peValueType == TypeCode.SByte or peValueType == TypeCode.Int16 or peValueType == TypeCode.UInt16 or peValueType == TypeCode.Int32 or peValueType == TypeCode.UInt32 or peValueType == TypeCode.Int64 or peValueType == TypeCode.UInt64:
					self._searchTermLiteralType = TypeCode.Int64
					self._searchTermLiteralValue = CSharpPrimitiveCast.Cast(TypeCode.Int64, pe.Value, False)
				elif peValueType == TypeCode.Single or peValueType == TypeCode.Double or peValueType == TypeCode.String:
					self._searchTermLiteralType = peValueType
					self._searchTermLiteralValue = pe.Value

	def IsMatch(self, field):
		return self.IsLiteralMatch(field.Constant)

	def IsMatch(self, property):
		return self.MethodIsLiteralMatch(property.GetMethod) or self.MethodIsLiteralMatch(property.SetMethod)

	def IsMatch(self, ev):
		return self.MethodIsLiteralMatch(ev.AddMethod) or self.MethodIsLiteralMatch(ev.RemoveMethod) or self.MethodIsLiteralMatch(ev.InvokeMethod)

	def IsMatch(self, m):
		return self.MethodIsLiteralMatch(m)

	def IsLiteralMatch(self, val):
		if val == None:
			return False
		if self._searchTermLiteralType == TypeCode.Int64:
			tc = Type.GetTypeCode(val.GetType())
			if tc >= TypeCode.SByte and tc <= TypeCode.UInt64:
				return CSharpPrimitiveCast.Cast(TypeCode.Int64, val, False).Equals(self._searchTermLiteralValue)
			else:
				return False
		elif self._searchTermLiteralType == TypeCode.Single or self._searchTermLiteralType == TypeCode.Double or self._searchTermLiteralType == TypeCode.String:
			return self._searchTermLiteralValue.Equals(val)
		else:
			# substring search with searchTerm
			return self.IsMatch(val.ToString())

	def MethodIsLiteralMatch(self, m):
		if m == None:
			return False
		body = m.Body
		if body == None:
			return False
		if self._searchTermLiteralType == TypeCode.Int64:
			val = self._searchTermLiteralValue
			enumerator = body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				inst = enumerator.Current
				if inst.OpCode.Code == Code.Ldc_I8:
					if val == inst.Operand:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4:
					if val == inst.Operand:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_S:
					if val == inst.Operand:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_M1:
					if val == -1:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_0:
					if val == 0:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_1:
					if val == 1:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_2:
					if val == 2:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_3:
					if val == 3:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_4:
					if val == 4:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_5:
					if val == 5:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_6:
					if val == 6:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_7:
					if val == 7:
						return True
				elif inst.OpCode.Code == Code.Ldc_I4_8:
					if val == 8:
						return True
		elif self._searchTermLiteralType != TypeCode.Empty:
			if self._searchTermLiteralType == TypeCode.Single:
				expectedCode = Code.Ldc_R4
			elif self._searchTermLiteralType == TypeCode.Double:
				expectedCode = Code.Ldc_R8
			elif self._searchTermLiteralType == TypeCode.String:
				expectedCode = Code.Ldstr
			else:
				raise InvalidOperationException()
			enumerator = body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				inst = enumerator.Current
				if inst.OpCode.Code == expectedCode and self._searchTermLiteralValue.Equals(inst.Operand):
					return True
		else:
			enumerator = body.Instructions.GetEnumerator()
			while enumerator.MoveNext():
				inst = enumerator.Current
				if inst.OpCode.Code == Code.Ldstr and self.IsMatch(inst.Operand):
					return True
		return False

class MemberSearchKind(object):
	def __init__(self):

class MemberSearchStrategy(AbstractSearchStrategy):
	def __init__(self, terms, searchKind):
		self._searchKind = searchKind

	def __init__(self, terms, searchKind):
		self._searchKind = searchKind

	def IsMatch(self, field):
		return (self._searchKind == MemberSearchKind.All or self._searchKind == MemberSearchKind.Field) and self.IsMatch(field.Name)

	def IsMatch(self, property):
		return (self._searchKind == MemberSearchKind.All or self._searchKind == MemberSearchKind.Property) and self.IsMatch(property.Name)

	def IsMatch(self, ev):
		return (self._searchKind == MemberSearchKind.All or self._searchKind == MemberSearchKind.Event) and self.IsMatch(ev.Name)

	def IsMatch(self, m):
		return (self._searchKind == MemberSearchKind.All or self._searchKind == MemberSearchKind.Method) and self.IsMatch(m.Name)

class TypeSearchStrategy(AbstractSearchStrategy):
	def __init__(self, terms):
		pass
	def Search(self, type, language, addResult):
		if self.IsMatch(type.Name) or self.IsMatch(type.FullName):
			self.addResult(SearchResult(Member = type, Image = TypeTreeNode.GetIcon(type), Name = language.TypeToString(type, includeNamespace = False), LocationImage = TypeTreeNode.GetIcon(type.DeclaringType) if type.DeclaringType != None else Images.Namespace, Location = language.TypeToString(type.DeclaringType, includeNamespace = True) if type.DeclaringType != None else type.Namespace))
		enumerator = type.NestedTypes.GetEnumerator()
		while enumerator.MoveNext():
			nestedType = enumerator.Current
			self.Search(nestedType, language, addResult)

class TypeAndMemberSearchStrategy(AbstractSearchStrategy):
	def __init__(self, terms):
		pass
	def Search(self, type, language, addResult):
		if self.IsMatch(type.Name) or self.IsMatch(type.FullName):
			self.addResult(SearchResult(Member = type, Image = TypeTreeNode.GetIcon(type), Name = language.TypeToString(type, includeNamespace = False), LocationImage = TypeTreeNode.GetIcon(type.DeclaringType) if type.DeclaringType != None else Images.Namespace, Location = language.TypeToString(type.DeclaringType, includeNamespace = True) if type.DeclaringType != None else type.Namespace))
		enumerator = type.NestedTypes.GetEnumerator()
		while enumerator.MoveNext():
			nestedType = enumerator.Current
			self.Search(nestedType, language, addResult)
		self.Search(type, language, addResult)

	def IsMatch(self, field):
		return self.IsMatch(field.Name)

	def IsMatch(self, property):
		return self.IsMatch(property.Name)

	def IsMatch(self, ev):
		return self.IsMatch(ev.Name)

	def IsMatch(self, m):
		return self.IsMatch(m.Name)