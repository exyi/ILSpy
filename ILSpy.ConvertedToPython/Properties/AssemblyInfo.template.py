from System import *
from System.Resources import *
from System.Reflection import *
from System.Runtime.CompilerServices import *
from System.Runtime.InteropServices import *
# General Information about an assembly is controlled through the following 
# set of attributes. Change these attribute values to modify the information
# associated with an assembly.
# This sets the default COM visibility of types in the assembly to invisible.
# If you need to expose a type to COM, use [ComVisible(true)] on that type.
class RevisionClass(object):
	def __init__(self):
		self._Major = "2"
		self._Minor = "4"
		self._Build = "0"
		self._Revision = "$INSERTREVISION$"
		self._VersionName = None
		self._FullVersion = self._Major + "." + self._Minor + "." + self._Build + ".$INSERTREVISION$$INSERTBRANCHPOSTFIX$$INSERTVERSIONNAMEPOSTFIX$"