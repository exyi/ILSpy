import clr

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
from System.Windows.Media.Imaging import *
from System.Windows.Media import *
from System.Windows import *
from System.Collections.Generic import *

class Images(object):
	def __init__(self):
		self._Breakpoint = self.LoadBitmap("Breakpoint")
		self._CurrentLine = self.LoadBitmap("CurrentLine")
		self._ViewCode = self.LoadBitmap("ViewCode")
		self._Save = self.LoadBitmap("SaveFile")
		self._OK = self.LoadBitmap("OK")
		self._Delete = self.LoadBitmap("Delete")
		self._Search = self.LoadBitmap("Search")
		self._Assembly = self.LoadBitmap("Assembly")
		self._AssemblyWarning = self.LoadBitmap("AssemblyWarning")
		self._AssemblyLoading = self.LoadBitmap("FindAssembly")
		self._Library = self.LoadBitmap("Library")
		self._Namespace = self.LoadBitmap("NameSpace")
		self._ReferenceFolderOpen = self.LoadBitmap("ReferenceFolder.Open")
		self._ReferenceFolderClosed = self.LoadBitmap("ReferenceFolder.Closed")
		self._SubTypes = self.LoadBitmap("SubTypes")
		self._SuperTypes = self.LoadBitmap("SuperTypes")
		self._FolderOpen = self.LoadBitmap("Folder.Open")
		self._FolderClosed = self.LoadBitmap("Folder.Closed")
		self._Resource = self.LoadBitmap("Resource")
		self._ResourceImage = self.LoadBitmap("ResourceImage")
		self._ResourceResourcesFile = self.LoadBitmap("ResourceResourcesFile")
		self._ResourceXml = self.LoadBitmap("ResourceXml")
		self._ResourceXsd = self.LoadBitmap("ResourceXsd")
		self._ResourceXslt = self.LoadBitmap("ResourceXslt")
		self._Class = self.LoadBitmap("Class")
		self._Struct = self.LoadBitmap("Struct")
		self._Interface = self.LoadBitmap("Interface")
		self._Delegate = self.LoadBitmap("Delegate")
		self._Enum = self.LoadBitmap("Enum")
		self._StaticClass = self.LoadBitmap("StaticClass")
		self._Field = self.LoadBitmap("Field")
		self._FieldReadOnly = self.LoadBitmap("FieldReadOnly")
		self._Literal = self.LoadBitmap("Literal")
		self._EnumValue = self.LoadBitmap("EnumValue")
		self._Method = self.LoadBitmap("Method")
		self._Constructor = self.LoadBitmap("Constructor")
		self._VirtualMethod = self.LoadBitmap("VirtualMethod")
		self._Operator = self.LoadBitmap("Operator")
		self._ExtensionMethod = self.LoadBitmap("ExtensionMethod")
		self._PInvokeMethod = self.LoadBitmap("PInvokeMethod")
		self._Property = self.LoadBitmap("Property")
		self._Indexer = self.LoadBitmap("Indexer")
		self._Event = self.LoadBitmap("Event")
		self._OverlayProtected = self.LoadBitmap("OverlayProtected")
		self._OverlayInternal = self.LoadBitmap("OverlayInternal")
		self._OverlayProtectedInternal = self.LoadBitmap("OverlayProtectedInternal")
		self._OverlayPrivate = self.LoadBitmap("OverlayPrivate")
		self._OverlayCompilerControlled = self.LoadBitmap("OverlayCompilerControlled")
		self._OverlayStatic = self.LoadBitmap("OverlayStatic")
		self._typeIconCache = TypeIconCache()
		self._memberIconCache = MemberIconCache()

	def LoadBitmap(name):
		image = BitmapImage(Uri("pack://application:,,,/Images/" + name + ".png"))
		image.Freeze()
		return image

	LoadBitmap = staticmethod(LoadBitmap)

	def LoadImage(part, icon):
		assembly = part.GetType().Assembly
		if assembly == clr.GetClrType(Images).Assembly:
			uri = Uri("pack://application:,,,/" + icon)
		else:
			name = assembly.GetName()
			uri = Uri("pack://application:,,,/" + name.Name + ";v" + name.Version + ";component/" + icon)
		image = BitmapImage(uri)
		image.Freeze()
		return image

	LoadImage = staticmethod(LoadImage)

	def GetIcon(icon, overlay, isStatic):

	GetIcon = staticmethod(GetIcon)

	def GetIcon(icon, overlay, isStatic):

	GetIcon = staticmethod(GetIcon)

	class TypeIconCache(IconCache):
		def __init__(self):
			self.PreloadPublicIconToCache(TypeIcon.Class, Images.Class)
			self.PreloadPublicIconToCache(TypeIcon.Enum, Images.Enum)
			self.PreloadPublicIconToCache(TypeIcon.Struct, Images.Struct)
			self.PreloadPublicIconToCache(TypeIcon.Interface, Images.Interface)
			self.PreloadPublicIconToCache(TypeIcon.Delegate, Images.Delegate)
			self.PreloadPublicIconToCache(TypeIcon.StaticClass, Images.StaticClass)

		def GetBaseImage(self, icon):
			if icon == TypeIcon.Class:
				baseImage = Images.Class
			elif icon == TypeIcon.Enum:
				baseImage = Images.Enum
			elif icon == TypeIcon.Struct:
				baseImage = Images.Struct
			elif icon == TypeIcon.Interface:
				baseImage = Images.Interface
			elif icon == TypeIcon.Delegate:
				baseImage = Images.Delegate
			elif icon == TypeIcon.StaticClass:
				baseImage = Images.StaticClass
			else:
				raise NotSupportedException()
			return baseImage

	class MemberIconCache(IconCache):
		def __init__(self):
			self.PreloadPublicIconToCache(MemberIcon.Field, Images.Field)
			self.PreloadPublicIconToCache(MemberIcon.FieldReadOnly, Images.FieldReadOnly)
			self.PreloadPublicIconToCache(MemberIcon.Literal, Images.Literal)
			self.PreloadPublicIconToCache(MemberIcon.EnumValue, Images.EnumValue)
			self.PreloadPublicIconToCache(MemberIcon.Property, Images.Property)
			self.PreloadPublicIconToCache(MemberIcon.Indexer, Images.Indexer)
			self.PreloadPublicIconToCache(MemberIcon.Method, Images.Method)
			self.PreloadPublicIconToCache(MemberIcon.Constructor, Images.Constructor)
			self.PreloadPublicIconToCache(MemberIcon.VirtualMethod, Images.VirtualMethod)
			self.PreloadPublicIconToCache(MemberIcon.Operator, Images.Operator)
			self.PreloadPublicIconToCache(MemberIcon.ExtensionMethod, Images.ExtensionMethod)
			self.PreloadPublicIconToCache(MemberIcon.PInvokeMethod, Images.PInvokeMethod)
			self.PreloadPublicIconToCache(MemberIcon.Event, Images.Event)

		def GetBaseImage(self, icon):
			if icon == MemberIcon.Field:
				baseImage = Images.Field
			elif icon == MemberIcon.FieldReadOnly:
				baseImage = Images.FieldReadOnly
			elif icon == MemberIcon.Literal:
				baseImage = Images.Literal
			elif icon == MemberIcon.EnumValue:
				baseImage = Images.Literal
			elif icon == MemberIcon.Property:
				baseImage = Images.Property
			elif icon == MemberIcon.Indexer:
				baseImage = Images.Indexer
			elif icon == MemberIcon.Method:
				baseImage = Images.Method
			elif icon == MemberIcon.Constructor:
				baseImage = Images.Constructor
			elif icon == MemberIcon.VirtualMethod:
				baseImage = Images.VirtualMethod
			elif icon == MemberIcon.Operator:
				baseImage = Images.Operator
			elif icon == MemberIcon.ExtensionMethod:
				baseImage = Images.ExtensionMethod
			elif icon == MemberIcon.PInvokeMethod:
				baseImage = Images.PInvokeMethod
			elif icon == MemberIcon.Event:
				baseImage = Images.Event
			else:
				raise NotSupportedException()
			return baseImage

	class IconCache(object):
		def __init__(self):
			self._cache = Dictionary[Tuple, ImageSource]()
			self._iconRect = Rect(0, 0, 16, 16)

		def PreloadPublicIconToCache(self, icon, image):
			iconKey = Tuple[T, AccessOverlayIcon, Boolean](icon, AccessOverlayIcon.Public, False)
			self._cache.Add(iconKey, image)

		def GetIcon(self, icon, overlay, isStatic):
			iconKey = Tuple[T, AccessOverlayIcon, Boolean](icon, overlay, isStatic)
			if self._cache.ContainsKey(iconKey):
				return self._cache[iconKey]
			else:
				result = self.BuildMemberIcon(icon, overlay, isStatic)
				self._cache.Add(iconKey, result)
				return result

		def BuildMemberIcon(self, icon, overlay, isStatic):
			baseImage = self.GetBaseImage(icon)
			overlayImage = self.GetOverlayImage(overlay)
			return self.CreateOverlayImage(baseImage, overlayImage, isStatic)

		def GetBaseImage(self, icon):
			pass

		def GetOverlayImage(overlay):
			if overlay == AccessOverlayIcon.Public:
				overlayImage = None
			elif overlay == AccessOverlayIcon.Protected:
				overlayImage = Images.OverlayProtected
			elif overlay == AccessOverlayIcon.Internal:
				overlayImage = Images.OverlayInternal
			elif overlay == AccessOverlayIcon.ProtectedInternal:
				overlayImage = Images.OverlayProtectedInternal
			elif overlay == AccessOverlayIcon.Private:
				overlayImage = Images.OverlayPrivate
			elif overlay == AccessOverlayIcon.CompilerControlled:
				overlayImage = Images.OverlayCompilerControlled
			else:
				raise NotSupportedException()
			return overlayImage

		GetOverlayImage = staticmethod(GetOverlayImage)

		def CreateOverlayImage(baseImage, overlay, isStatic):
			group = DrawingGroup()
			group.Children.Add(ImageDrawing(baseImage, self._iconRect))
			if overlay != None:
				group.Children.Add(ImageDrawing(overlay, self._iconRect))
			if isStatic:
				group.Children.Add(ImageDrawing(Images.OverlayStatic, self._iconRect))
			image = DrawingImage(group)
			image.Freeze()
			return image

		CreateOverlayImage = staticmethod(CreateOverlayImage)