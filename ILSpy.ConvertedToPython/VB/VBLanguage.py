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
from System.Threading.Tasks import *
from System.Xml import *
from ICSharpCode.Decompiler import *
from ICSharpCode.Decompiler.Ast import *
from ICSharpCode.Decompiler.Ast.Transforms import *
from ICSharpCode.ILSpy.XmlDoc import *
from ICSharpCode.NRefactory.VB import *
from ICSharpCode.NRefactory.VB.Visitors import *
from Mono.Cecil import *
from CSharp import *

class VBLanguage(Language):
	# <summary>
	# Decompiler logic for VB.
	# </summary>
	def __init__(self):
		self._transformAbortCondition = None
		self._showAllMembers = False
		# don't automatically load additional assemblies when an assembly node is selected in the tree view
		self._projectImports = Array[](("System.Diagnostics", "Microsoft.VisualBasic", "System", "System.Collections", "System.Collections.Generic"))

	def get_Name(self):
		return "VB"

	Name = property(fget=get_Name)

	def get_FileExtension(self):
		return ".vb"

	FileExtension = property(fget=get_FileExtension)

	def get_ProjectFileExtension(self):
		return ".vbproj"

	ProjectFileExtension = property(fget=get_ProjectFileExtension)

	def WriteCommentLine(self, output, comment):
		output.WriteLine("' " + comment)

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
				output.Write("' Global type: ")
				output.WriteReference(mainModule.Types[0].FullName, mainModule.Types[0])
				output.WriteLine()
			if mainModule.EntryPoint != None:
				output.Write("' Entry point: ")
				output.WriteReference(mainModule.EntryPoint.DeclaringType.FullName + "." + mainModule.EntryPoint.Name, mainModule.EntryPoint)
				output.WriteLine()
			self.WriteCommentLine(output, "Architecture: " + CSharpLanguage.GetPlatformDisplayName(mainModule))
			if (mainModule.Attributes & ModuleAttributes.ILOnly) == 0:
				self.WriteCommentLine(output, "This assembly contains unmanaged code.")
			if mainModule.Runtime == TargetRuntime.Net_1_0:
				self.WriteCommentLine(output, "Runtime: .NET 1.0")
			elif mainModule.Runtime == TargetRuntime.Net_1_1:
				self.WriteCommentLine(output, "Runtime: .NET 1.1")
			elif mainModule.Runtime == TargetRuntime.Net_2_0:
				self.WriteCommentLine(output, "Runtime: .NET 2.0")
			elif mainModule.Runtime == TargetRuntime.Net_4_0:
				self.WriteCommentLine(output, "Runtime: .NET 4.0")
			output.WriteLine()

	def WriteProjectFile(self, writer, files, module):
		ns = "http://schemas.microsoft.com/developer/msbuild/2003"
		platformName = CSharpLanguage.GetPlatformName(module)
		guid = App.CommandLineArguments.FixedGuid == Guid.NewGuid()
 # </Configuration> # </Platform>
	# TODO: Detect when .NET 3.0/3.5 is required # </PropertyGroup> # platform-specific # </PropertyGroup> (platform-specific) # Debug # </PropertyGroup> (Debug) # Release # </PropertyGroup> (Release) # References # </ItemGroup> (References) # Imports # </ItemGroup> (Imports)
	def IncludeTypeWhenDecompilingProject(self, type, options):
		if type.Name == "<Module>" or AstBuilder.MemberIsHidden(type, options.DecompilerSettings):
			return False
		if type.Namespace == "XamlGeneratedNamespace" and type.Name == "GeneratedInternalTypeHelper":
			return False
		return True

	def WriteAssemblyInfo(self, module, options, directories):
		# don't automatically load additional assemblies when an assembly node is selected in the tree view

	def WriteCodeFilesInProject(self, module, options, directories):
		files = module.Types.Where().GroupBy(, StringComparer.OrdinalIgnoreCase).ToList()
		AstMethodBodyBuilder.ClearUnhandledOpcodes()
		Parallel.ForEach(files, ParallelOptions(MaxDegreeOfParallelism = Environment.ProcessorCount), )
		AstMethodBodyBuilder.PrintNumberOfUnhandledOpcodes()
		return files.Select().Concat(self.WriteAssemblyInfo(module, options, directories))

	def DecompileMethod(self, method, output, options):
		self.WriteCommentLine(output, self.TypeToString(method.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = method.DeclaringType, isSingleMember = True)
		codeDomBuilder.AddMethod(method)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options, method.Module)

	def DecompileProperty(self, property, output, options):
		self.WriteCommentLine(output, self.TypeToString(property.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = property.DeclaringType, isSingleMember = True)
		codeDomBuilder.AddProperty(property)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options, property.Module)

	def DecompileField(self, field, output, options):
		self.WriteCommentLine(output, self.TypeToString(field.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = field.DeclaringType, isSingleMember = True)
		codeDomBuilder.AddField(field)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options, field.Module)

	def DecompileEvent(self, ev, output, options):
		self.WriteCommentLine(output, self.TypeToString(ev.DeclaringType, includeNamespace = True))
		codeDomBuilder = self.CreateAstBuilder(options, currentType = ev.DeclaringType, isSingleMember = True)
		codeDomBuilder.AddEvent(ev)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options, ev.Module)

	def DecompileType(self, type, output, options):
		codeDomBuilder = self.CreateAstBuilder(options, currentModule = type.Module)
		codeDomBuilder.AddType(type)
		self.RunTransformsAndGenerateCode(codeDomBuilder, output, options, type.Module)

	def ShowMember(self, member):
		return self._showAllMembers or not AstBuilder.MemberIsHidden(member, DecompilationOptions().DecompilerSettings)

	def RunTransformsAndGenerateCode(self, astBuilder, output, options, module):
		astBuilder.RunTransformations(self._transformAbortCondition)
		if options.DecompilerSettings.ShowXmlDocumentation:
			try:
				AddXmlDocTransform.Run(astBuilder.SyntaxTree)
			except XmlException, ex:
				msg = (" Exception while reading XmlDoc: " + ex.ToString()).Split(Array[](('\r', '\n')), StringSplitOptions.RemoveEmptyEntries)
				insertionPoint = astBuilder.SyntaxTree.FirstChild
				i = 0
				while i < msg.Length:
					astBuilder.SyntaxTree.InsertChildBefore(insertionPoint, CSharp.Comment(msg[i], CSharp.CommentType.Documentation), CSharp.Roles.Comment)
					i += 1
			finally:
		csharpUnit = astBuilder.SyntaxTree
		csharpUnit.AcceptVisitor(NRefactory.CSharp.InsertParenthesesVisitor(InsertParenthesesForReadability = True))
		unit = csharpUnit.AcceptVisitor(CSharpToVBConverterVisitor(ILSpyEnvironmentProvider()), None)
		outputFormatter = VBTextOutputFormatter(output)
		formattingPolicy = VBFormattingOptions()
		unit.AcceptVisitor(OutputVisitor(outputFormatter, formattingPolicy), None)

	def CreateAstBuilder(self, options, currentModule, currentType, isSingleMember):
		if currentModule == None:
			currentModule = currentType.Module
		settings = options.DecompilerSettings
		settings = settings.Clone()
		if isSingleMember:
			settings.UsingDeclarations = False
		settings.IntroduceIncrementAndDecrement = False
		settings.MakeAssignmentExpressions = False
		settings.QueryExpressions = False
		settings.AlwaysGenerateExceptionVariableForCatchBlocks = True
		return AstBuilder(DecompilerContext(currentModuleCancellationToken = options.CancellationToken, CurrentType = currentType, Settings = settings))

	def FormatMethodName(self, method):
		if method == None:
			raise ArgumentNullException("method")
		return method.DeclaringType.Name if (method.IsConstructor) else method.Name

	def FormatTypeName(self, type):
		if type == None:
			raise ArgumentNullException("type")
		return self.TypeToString(ConvertTypeOptions.DoNotUsePrimitiveTypeNames | ConvertTypeOptions.IncludeTypeParameterDefinitions, type)

	def TypeToString(self, type, includeNamespace, typeAttributes):
		options = ConvertTypeOptions.IncludeTypeParameterDefinitions
		if includeNamespace:
			options |= ConvertTypeOptions.IncludeNamespace
		return self.TypeToString(options, type, typeAttributes)

	def TypeToString(self, options, type, typeAttributes):
		envProvider = ILSpyEnvironmentProvider()
		converter = CSharpToVBConverterVisitor(envProvider)
		astType = AstBuilder.ConvertType(type, typeAttributes, options)
		w = StringWriter()
		if type.IsByReference:
			w.Write("ByRef ")
			if  and (astType).PointerRank > 0:
				(astType).PointerRank -= 1
		vbAstType = astType.AcceptVisitor(converter, None)
		vbAstType.AcceptVisitor(OutputVisitor(w, VBFormattingOptions()), None)
		return w.ToString()