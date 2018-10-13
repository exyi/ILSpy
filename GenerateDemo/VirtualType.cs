using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata;
using ICSharpCode.Decompiler;
using ICSharpCode.Decompiler.IL;
using ICSharpCode.Decompiler.Metadata;
using ICSharpCode.Decompiler.TypeSystem;
using ICSharpCode.Decompiler.TypeSystem.Implementation;
using ICSharpCode.Decompiler.Util;

namespace GenerateDemo
{

    public class VirtualType : ITypeDefinition
    {
        public VirtualType(TypeKind kind, Accessibility accessibility, FullTypeName name, bool isStatic, bool isSealed, bool isAbstract, ITypeDefinition declaringType = null, IModule parentModule = null)
        {
            this.Kind = kind;
            this.DeclaringTypeDefinition = declaringType;
            this.Accessibility = accessibility;
            this.FullTypeName = name;
            this.IsAbstract = isAbstract;
            this.IsStatic = isStatic;
            this.IsSealed = isSealed;
            this.ParentModule = parentModule ?? declaringType.ParentModule ?? throw new ArgumentNullException(nameof(parentModule));
        }

        public TypeKind Kind { get; }

        public bool? IsReferenceType => this.Kind == TypeKind.Class || this.Kind == TypeKind.Interface;

        public bool IsByRefLike => false;

        public ITypeDefinition DeclaringTypeDefinition { get; }
        public IType DeclaringType => this.DeclaringTypeDefinition;

        public int TypeParameterCount => 0;

        public IReadOnlyList<ITypeParameter> TypeParameters => EmptyList<ITypeParameter>.Instance;

        public IReadOnlyList<IType> TypeArguments => EmptyList<IType>.Instance;

        public IEnumerable<IType> DirectBaseTypes => EmptyList<IType>.Instance;

        public string FullName => this.FullTypeName.ReflectionName;

        public string Name => this.FullTypeName.Name;

        public string ReflectionName => this.FullTypeName.ReflectionName;

        public string Namespace => this.FullTypeName.TopLevelTypeName.Namespace;

        public IReadOnlyList<IMember> Members => Methods;
        public List<IMethod> Methods = new List<IMethod>();
        IEnumerable<IMethod> ITypeDefinition.Methods => this.Methods;


        public IReadOnlyList<ITypeDefinition> NestedTypes => EmptyList<ITypeDefinition>.Instance;
        public IEnumerable<IField> Fields => EmptyList<IField>.Instance;

        public IEnumerable<IProperty> Properties => EmptyList<IProperty>.Instance;

        public IEnumerable<IEvent> Events => EmptyList<IEvent>.Instance;

        public KnownTypeCode KnownTypeCode => KnownTypeCode.None;

        public IType EnumUnderlyingType => throw new NotImplementedException();

        public bool IsReadOnly => false;

        public FullTypeName FullTypeName { get; }
        public bool HasExtensionMethods => false;

        public EntityHandle MetadataToken => default;


        public IModule ParentModule { get; }

        public Accessibility Accessibility { get; }

        public bool IsStatic { get; }

        public bool IsAbstract { get; }

        public bool IsSealed { get; }

        public SymbolKind SymbolKind => SymbolKind.TypeDefinition;

        public ICompilation Compilation => this.ParentModule.Compilation;

        public IType AcceptVisitor(TypeVisitor visitor)
        {
            return visitor.VisitTypeDefinition(this);
        }

        public bool Equals(IType other)
        {
            return this.ReflectionName == other.ReflectionName;
        }

        public IEnumerable<IMethod> GetAccessors(Predicate<IMethod> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public IEnumerable<IAttribute> GetAttributes()
        {
            yield break;
        }

        public IEnumerable<IMethod> GetConstructors(Predicate<IMethod> filter = null, GetMemberOptions options = GetMemberOptions.IgnoreInheritedMembers)
        {
            yield break;
        }

        public ITypeDefinition GetDefinition() => this;

        public IEnumerable<IEvent> GetEvents(Predicate<IEvent> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public IEnumerable<IField> GetFields(Predicate<IField> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public IEnumerable<IMember> GetMembers(Predicate<IMember> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public IEnumerable<IMethod> GetMethods(Predicate<IMethod> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            return this.Methods.Where(a => filter?.Invoke(a) ?? true);
        }

        public IEnumerable<IMethod> GetMethods(IReadOnlyList<IType> typeArguments, Predicate<IMethod> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public IEnumerable<IType> GetNestedTypes(Predicate<ITypeDefinition> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public IEnumerable<IType> GetNestedTypes(IReadOnlyList<IType> typeArguments, Predicate<ITypeDefinition> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public IEnumerable<IProperty> GetProperties(Predicate<IProperty> filter = null, GetMemberOptions options = GetMemberOptions.None)
        {
            yield break;
        }

        public TypeParameterSubstitution GetSubstitution()
        {
            return TypeParameterSubstitution.Identity;
        }

        public IType VisitChildren(TypeVisitor visitor)
        {
            return this;
        }
    }
}
