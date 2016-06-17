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
from System.ComponentModel.Composition import *
from System.IO import *
from System.Linq import *
from System.Text.RegularExpressions import *
from System.Threading.Tasks import *
from System.Xml import *
from ICSharpCode.Decompiler import *
from ICSharpCode.Decompiler.Ast import *
from ICSharpCode.Decompiler.Ast.Transforms import *
from ICSharpCode.ILSpy.Options import *
from ICSharpCode.ILSpy.XmlDoc import *
from ICSharpCode.NRefactory.CSharp import *
from Mono.Cecil import *

class CSharpLanguage(Language):
	# <summary>
	# Decompiler logic for C#.
	# </summary>
	def __init__(self):
		self._name = "C#"
		self._showAllMembers = False
		self._transformAbortCondition = None # copy for lambda
		# also fields and other ctors so that the field initializers can be shown as such
		# remove other ctors
		# Remove any fields without initializers
		# remove all fields
		# also decompile ctors so that the field initializer can be shown
		# <summary>
		# Removes all top-level members except for the specified fields.
		# </summary>
		# don't automatically load additional assemblies when an assembly node is selected in the tree view # </Configuration> # </Platform>
		# TODO: Detect when .NET 3.0/3.5 is required # </PropertyGroup> # platform-specific # </PropertyGroup> (platform-specific) # Debug # </PropertyGroup> (Debug) # Release # </PropertyGroup> (Release) # References # </ItemGroup> (References)
		# don't automatically load additional assemblies when an assembly node is selected in the tree view
		self._TypeToStringFormattingOptions = FormattingOptionsFactory.CreateEmpty()

	def GetDebugLanguages():
		context = DecompilerContext(ModuleDefinition.CreateModule("dummy", ModuleKind.Dll))
		lastTransformName = "no transforms"
		enumerator = TransformationPipeline.CreatePipeline(context).Select().Distinct().GetEnumerator()
		while enumerator.MoveNext():
			_transformType = enumerator.Current
			transformType = _transformType
			lastTransformName = "after " + transformType.Name

	GetDebugLanguages = staticmethod(GetDebugLanguages)

	def get_Name(self):
		return self._name

	Name = property(fget=get_Name)

	def get_FileExtension(self):
		return ".cs"

	FileExtension = property(fget=get_FileExtension)

	def get_ProjectFileExtension(self):
		return ".csproj"

	ProjectFileExtension = property(fget=get_ProjectFileExtension)

	def DecompileMethod(self, method, output, options):
		self.WriteCommentLine(output, self.TypeToString(method.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = method.DeclaringType, isSingleMember = True)
		if method.IsConstructor and not method.IsStatic and not method.DeclaringType.IsValueType:
			self.AddFieldsAndCtors(codeDomBuilder, method.DeclaringType, method.IsStatic)
			self.RunTransformsAndGenerateCode(codeDomBuilder, output, options, SelectCtorTransform(method))
		else:
			codeDomBuilder.AddMethod(method)
			self.RunTransformsAndGenerateCode(codeDomBuilder, output, options)

	class SelectCtorTransform(IAstTransform):
		def __init__(self, ctorDef):
			self._ctorDef = ctorDef

		def Run(self, compilationUnit):
			ctorDecl = None
			enumerator = compilationUnit.Children.GetEnumerator()
			while enumerator.MoveNext():
				node = enumerator.Current
				ctor = node
				if ctor != None:
					if ctor.Annotation() == self._ctorDef:
						ctorDecl = ctor
					else:
						ctor.Remove()
				fd = node
				if fd != None and fd.Variables.All():
					fd.Remove()
			if ctorDecl.Initializer.ConstructorInitializerType == ConstructorInitializerType.This:
				enumerator = compilationUnit.Children.GetEnumerator()
				while enumerator.MoveNext():
					node = enumerator.Current
					if :
						node.Remove()

	def DecompileProperty(self, property, output, options):
		self.WriteCommentLine(output, self.TypeToString(property.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = property.DeclaringType, isSingleMember = True)
		codeDomBuilder.AddProperty(property)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options)

	def DecompileField(self, field, output, options):
		self.WriteCommentLine(output, self.TypeToString(field.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = field.DeclaringType, isSingleMember = True)
		if field.IsLiteral:
			codeDomBuilder.AddField(field)
		else:
			self.AddFieldsAndCtors(codeDomBuilder, field.DeclaringType, field.IsStatic)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options, SelectFieldTransform(field))

	class SelectFieldTransform(IAstTransform):
		def __init__(self, field):
			self._field = field

		def Run(self, compilationUnit):
			enumerator = compilationUnit.Children.GetEnumerator()
			while enumerator.MoveNext():
				child = enumerator.Current
				if :
					if child.Annotation() != self._field:
						child.Remove()

	def AddFieldsAndCtors(self, codeDomBuilder, declaringType, isStatic):
		enumerator = declaringType.Fields.GetEnumerator()
		while enumerator.MoveNext():
			field = enumerator.Current
			if self._field.IsStatic == isStatic:
				codeDomBuilder.AddField(self._field)
		enumerator = declaringType.Methods.GetEnumerator()
		while enumerator.MoveNext():
			ctor = enumerator.Current
			if ctor.IsConstructor and ctor.IsStatic == isStatic:
				codeDomBuilder.AddMethod(ctor)

	def DecompileEvent(self, ev, output, options):
		self.WriteCommentLine(output, self.TypeToString(ev.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = ev.DeclaringType, isSingleMember = True)
		codeDomBuilder.AddEvent(ev)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options)

	def DecompileType(self, type, output, options):
		codeDomBuilder = self.CreateAstBuilder(options, currentModule = type.Module)
		codeDomBuilder.AddType(type)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options)

	def RunTransformsAndGenerateCode(self, astBuilder, output, options, additionalTransform):
		astBuilder.RunTransformations(transformAbortCondition)
		if additionalTransform != None:
			additionalTransform.Run(astBuilder.SyntaxTree)
		if options.DecompilerSettings.ShowXmlDocumentation:
			try:
				AddXmlDocTransform.Run(astBuilder.SyntaxTree)
			except XmlException, ex:
				msg = (" Exception while reading XmlDoc: " + ex.ToString()).Split(Array[](('\r', '\n')), StringSplitOptions.RemoveEmptyEntries)
				insertionPoint = astBuilder.SyntaxTree.FirstChild
				i = 0
				while i < msg.Length:
					astBuilder.SyntaxTree.InsertChildBefore(insertionPoint, Comment(msg[i], CommentType.Documentation), Roles.Comment)
					i += 1
			finally:
		astBuilder.GenerateCode(output)

	def GetPlatformDisplayName(module):
		if module.Architecture == TargetArchitecture.I386:
			if (module.Attributes & ModuleAttributes.Preferred32Bit) == ModuleAttributes.Preferred32Bit:
				return "AnyCPU (32-bit preferred)"
			elif (module.Attributes & ModuleAttributes.Required32Bit) == ModuleAttributes.Required32Bit:
				return "x86"
			else:
				return "AnyCPU (64-bit preferred)"
		elif module.Architecture == TargetArchitecture.AMD64:
			return "x64"
		elif module.Architecture == TargetArchitecture.IA64:
			return "Itanium"
		else:
			return module.Architecture.ToString()

	GetPlatformDisplayName = staticmethod(GetPlatformDisplayName)

	def GetPlatformName(module):
		if module.Architecture == TargetArchitecture.I386:
			if (module.Attributes & ModuleAttributes.Preferred32Bit) == ModuleAttributes.Preferred32Bit:
				return "AnyCPU"
			elif (module.Attributes & ModuleAttributes.Required32Bit) == ModuleAttributes.Required32Bit:
				return "x86"
			else:
				return "AnyCPU"
		elif module.Architecture == TargetArchitecture.AMD64:
			return "x64"
		elif module.Architecture == TargetArchitecture.IA64:
			return "Itanium"
		else:
			return module.Architecture.ToString()

	GetPlatformName = staticmethod(GetPlatformName)

	def GetRuntimeDisplayName(module):
		if module.Runtime == TargetRuntime.Net_1_0:
			return ".NET 1.0"
		elif module.Runtime == TargetRuntime.Net_1_1:
			return ".NET 1.1"
		elif module.Runtime == TargetRuntime.Net_2_0:
			return ".NET 2.0"
		elif module.Runtime == TargetRuntime.Net_4_0:
			return ".NET 4.0"
		return None

	GetRuntimeDisplayName = staticmethod(GetRuntimeDisplayName)

	def DecompileAssembly(self, assembly, output, options):
		if options.FullDecompilation and options.SaveAsProjectDirectory != None:
			directories = HashSet[str](StringComparer.OrdinalIgnoreCase)
			files = self.WriteCodeFilesInProject(assembly.ModuleDefinition, options, directories).ToList()
			files.AddRange(self.WriteResourceFilesInProject(assembly, options, directories))
			self.WriteProjectFile(TextOutputWriter(output), files, assembly.ModuleDefinition)
		else:
			self.DecompileAssembly(assembly, output, options)
			output.WriteLine()
			mainModule = assembly.ModuleDefinition
			if mainModule.Types.Count > 0:
				output.Write("// Global type: ")
				output.WriteReference(mainModule.Types[0].FullName, mainModule.Types[0])
				output.WriteLine()
			if mainModule.EntryPoint != None:
				output.Write("// Entry point: ")
				output.WriteReference(mainModule.EntryPoint.DeclaringType.FullName + "." + mainModule.EntryPoint.Name, mainModule.EntryPoint)
				output.WriteLine()
			output.WriteLine("// Architecture: " + self.GetPlatformDisplayName(mainModule))
			if (mainModule.Attributes & ModuleAttributes.ILOnly) == 0:
				output.WriteLine("// This assembly contains unmanaged code.")
			runtimeName = self.GetRuntimeDisplayName(mainModule)
			if runtimeName != None:
				output.WriteLine("// Runtime: " + runtimeName)
			output.WriteLine()

	def WriteProjectFile(self, writer, files, module):
		ns = "http://schemas.microsoft.com/developer/msbuild/2003"
		platformName = self.GetPlatformName(module)
		guid = App.CommandLineArguments.FixedGuid == Guid.NewGuid()

	def IncludeTypeWhenDecompilingProject(self, type, options):
		if type.Name == "<Module>" or AstBuilder.MemberIsHidden(type, options.DecompilerSettings):
			return False
		if type.Namespace == "XamlGeneratedNamespace" and type.Name == "GeneratedInternalTypeHelper":
			return False
		return True

	def WriteAssemblyInfo(self, module, options, directories):

	def WriteCodeFilesInProject(self, module, options, directories):
		files = module.Types.Where().GroupBy(, StringComparer.OrdinalIgnoreCase).ToList()
		AstMethodBodyBuilder.ClearUnhandledOpcodes()
		Parallel.ForEach(files, ParallelOptions(MaxDegreeOfParallelism = Environment.ProcessorCount), )
		AstMethodBodyBuilder.PrintNumberOfUnhandledOpcodes()
		return files.Select().Concat(self.WriteAssemblyInfo(module, options, directories))

	def CreateAstBuilder(self, options, currentModule, currentType, isSingleMember):
		if currentModule == None:
			currentModule = currentType.Module
		settings = options.DecompilerSettings
		if isSingleMember:
			settings = settings.Clone()
			settings.UsingDeclarations = False
		return AstBuilder(DecompilerContext(currentModuleCancellationToken = options.CancellationToken, CurrentType = currentType, Settings = settings))

	def TypeToString(self, type, includeNamespace, typeAttributes):
		options = ConvertTypeOptions.IncludeTypeParameterDefinitions
		if includeNamespace:
			options |= ConvertTypeOptions.IncludeNamespace
		return self.TypeToString(options, type, typeAttributes)

	def TypeToString(self, options, type, typeAttributes):
		astType = AstBuilder.ConvertType(type, typeAttributes, options)
		w = StringWriter()
		if type.IsByReference:
			pd = typeAttributes
			if pd != None and (not pd.IsIn and pd.IsOut):
				w.Write("out ")
			else:
				w.Write("ref ")
			if  and (astType).PointerRank > 0:
				(astType).PointerRank -= 1
		astType.AcceptVisitor(CSharpOutputVisitor(w, TypeToStringFormattingOptions))
		return w.ToString()

	def FormatPropertyName(self, property, isIndexer):
		if property == None:
			raise ArgumentNullException("property")
		if not isIndexer.HasValue:
			isIndexer = property.IsIndexer()
		if isIndexer.Value:
			buffer = System.Text.StringBuilder()
			accessor = property.GetMethod == property.SetMethod
			if accessor.HasOverrides:
				declaringType = accessor.Overrides.First().DeclaringType
				buffer.Append(self.TypeToString(declaringType, includeNamespace = True))
				buffer.Append(@".")
			buffer.Append(@"this[")
			addSeparator = False
			enumerator = property.Parameters.GetEnumerator()
			while enumerator.MoveNext():
				p = enumerator.Current
				if addSeparator:
					buffer.Append(@", ")
				else:
					addSeparator = True
				buffer.Append(self.TypeToString(p.ParameterType, includeNamespace = True))
			buffer.Append(@"]")
			return buffer.ToString()
		else:
			return property.Name

	def FormatMethodName(self, method):
		if method == None:
			raise ArgumentNullException("method")
		return method.DeclaringType.Name if (method.IsConstructor) else method.Name

	def FormatTypeName(self, type):
		if type == None:
			raise ArgumentNullException("type")
		return self.TypeToString(ConvertTypeOptions.DoNotUsePrimitiveTypeNames | ConvertTypeOptions.IncludeTypeParameterDefinitions, type)

	def ShowMember(self, member):
		return showAllMembers or not AstBuilder.MemberIsHidden(member, DecompilationOptions().DecompilerSettings)

	def GetOriginalCodeLocation(self, member):
		if showAllMembers or not DecompilerSettingsPanel.CurrentDecompilerSettings.AnonymousMethods:
			return member
		else:
			return TreeNodes.Analyzer.Helpers.GetOriginalCodeLocation(member)

	def GetTooltip(self, member):
		md = member
		pd = member
		ed = member
		fd = member
		if md != None or pd != None or ed != None or fd != None:
			b = AstBuilder(DecompilerContext(member.ModuleSettings = DecompilerSettings(UsingDeclarations = False)))
			b.DecompileMethodBodies = False
			if md != None:
				b.AddMethod(md)
			elif pd != None:
				b.AddProperty(pd)
			elif ed != None:
				b.AddEvent(ed)
			else:
				b.AddField(fd)
			b.RunTransformations()
			enumerator = b.SyntaxTree.Descendants.OfType().GetEnumerator()
			while enumerator.MoveNext():
				attribute = enumerator.Current
				attribute.Remove()
			w = StringWriter()
			b.GenerateCode(PlainTextOutput(w))
			return Regex.Replace(w.ToString(), @"\s+", " ").TrimEnd()
		return self.GetTooltip(member)