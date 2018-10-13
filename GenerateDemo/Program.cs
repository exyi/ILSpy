using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Reflection.Metadata;
using System.Runtime.Loader;
using ICSharpCode.Decompiler;
using ICSharpCode.Decompiler.CSharp;
using ICSharpCode.Decompiler.IL;
using IL = ICSharpCode.Decompiler.IL;
using ICSharpCode.Decompiler.Metadata;
using ICSharpCode.Decompiler.TypeSystem;
using ICSharpCode.Decompiler.TypeSystem.Implementation;
using ICSharpCode.Decompiler.CSharp.Syntax;
using ICSharpCode.Decompiler.IL.Transforms;
using ICSharpCode.Decompiler.IL.ControlFlow;
using ICSharpCode.Decompiler.CSharp.OutputVisitor;
using System.Diagnostics;
using ICSharpCode.Decompiler.Util;
using ICSharpCode.Decompiler.CSharp.Resolver;

namespace GenerateDemo
{
    public static class TypeSystemUtils
    {
        public static INamespace FindDescendantNamespace(this INamespace ns, string nsName)
        {
            var xs = nsName.Split('.');
            foreach (var x in xs)
            {
                ns = ns?.GetChildNamespace(x);
            }
            return ns;
        }
    }

    public class HackedSimpleCompilation : SimpleCompilation, IDecompilerTypeSystem
    {
        public HackedSimpleCompilation(IModuleReference mainAssembly, params IModuleReference[] assemblyReferences) : base(mainAssembly, assemblyReferences)
        {
        }

        public HackedSimpleCompilation(IModuleReference mainAssembly, IEnumerable<IModuleReference> assemblyReferences) : base(mainAssembly, assemblyReferences)
        {
        }

        protected HackedSimpleCompilation()
        {
        }

        MetadataModule IDecompilerTypeSystem.MainModule => throw new NotSupportedException("");
    }

    class Program
    {
        static void Main(string[] args)
        {
            var someModules = from r in Enumerable.Concat(typeof(Program).Assembly.GetReferencedAssemblies(), new[] {
                                  typeof(string).Assembly.GetName(),
                                  // new AssemblyName("netstandard")
                              })
                              let location = AssemblyLoadContext.Default.LoadFromAssemblyName(r).Location
                              where !string.IsNullOrEmpty(location)
                              let lUrl = new Uri(location)
                              let fileName = lUrl.AbsolutePath
                              select new PEFile(fileName);

            var mRef = new VirtualModuleReference(true, "NewEpicModule");
            var compilation = new HackedSimpleCompilation(mRef, someModules);

            foreach (var x in typeof(Program).Assembly.GetReferencedAssemblies())
                Console.WriteLine($"RefAsm: {x}");
            Console.WriteLine($"String asm: {typeof(string).Assembly}");
            foreach (var x in compilation.Modules)
                Console.WriteLine($"Module: {x.FullAssemblyName}");

            var mod = mRef.Resolve(compilation);


            var tString = compilation.FindType(typeof(string));
            var tChar = compilation.FindType(typeof(char));
            var t2 = compilation.FindType(typeof(IEnumerable<char>));
            var tEnumerable = compilation.FindType(typeof(Enumerable));
            var toArray = tEnumerable.GetMethods(m => m.Name == "ToArray").Single().Specialize(new TypeParameterSubstitution(null, new [] { tChar }));

            var adhocType = new VirtualType(TypeKind.Class, Accessibility.Public, new FullTypeName("SomeNs.SomeType"), isStatic: false, isSealed: false, isAbstract: false, parentModule: mod);
            mod.AddType(adhocType);
            var methodParams = new[] { new DefaultParameter(tString, "testParam") };
            var adhocMethod = new VirtualMethod(adhocType, Accessibility.Public, "SomeMethod", methodParams, t2);
            adhocType.Methods.Add(adhocMethod);

            // var method = tString.GetMethods(m => m.IsConstructor && m.Parameters.Count == 1 && m.Parameters.Single().Type.Name == "IEnumerable`1").Single();

            adhocMethod.BodyFactory = () => {
                var variable = new ILVariable(VariableKind.Local, tString, StackType.O, 0);
                var functionContainer = new BlockContainer(expectedResultType: StackType.O);
                functionContainer.Blocks.Add(
                    new Block()
                    {
                        Instructions = {
                            new IL.StLoc(variable, new IL.LdStr("ahoj\"\u200BF")),
                            new IL.Leave(functionContainer, value: new IL.Call(toArray) { Arguments = { new IL.LdLoc(variable) } })
                        },
                        // FinalInstruction = new IL.LdLoc(variable)
                    });

                var ilFunc = new ILFunction(adhocMethod, 10000, new ICSharpCode.Decompiler.TypeSystem.GenericContext(), functionContainer) {
                    Variables = { variable }
                };
                ilFunc.AddRef(); // whatever, somehow initializes the freaking tree
                Debug.Assert(variable.Function == ilFunc);
                return ilFunc;
            };

            var emitter = new CSharpEmitter(compilation, new DecompilerSettings(LanguageVersion.Latest));
            var result = emitter.DecompileTypeAsString(adhocType.FullTypeName);


            Console.WriteLine($"result: \n\n{result}");
        }

    }
}
