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
from System.Threading import *
from ICSharpCode.Decompiler import *
from ICSharpCode.ILSpy.Options import *

class DecompilationOptions(object):
	""" <summary>
	 Options passed to the decompiler.
	 </summary>
	"""
	# <summary>
	# Gets whether a full decompilation (all members recursively) is desired.
	# If this option is false, language bindings are allowed to show the only headers of the decompiled element's children.
	# </summary>
	def get_FullDecompilation(self):

	def set_FullDecompilation(self, value):

	FullDecompilation = property(fget=get_FullDecompilation, fset=set_FullDecompilation)

	# <summary>
	# Gets/Sets the directory into which the project is saved.
	# </summary>
	def get_SaveAsProjectDirectory(self):

	def set_SaveAsProjectDirectory(self, value):

	SaveAsProjectDirectory = property(fget=get_SaveAsProjectDirectory, fset=set_SaveAsProjectDirectory)

	# <summary>
	# Gets the cancellation token that is used to abort the decompiler.
	# </summary>
	# <remarks>
	# Decompilers should regularly call <c>options.CancellationToken.ThrowIfCancellationRequested();</c>
	# to allow for cooperative cancellation of the decompilation task.
	# </remarks>
	def get_CancellationToken(self):

	def set_CancellationToken(self, value):

	CancellationToken = property(fget=get_CancellationToken, fset=set_CancellationToken)

	# <summary>
	# Gets the settings for the decompiler.
	# </summary>
	def get_DecompilerSettings(self):

	def set_DecompilerSettings(self, value):

	DecompilerSettings = property(fget=get_DecompilerSettings, fset=set_DecompilerSettings)

	# <summary>
	# Gets/sets an optional state of a decompiler text view.
	# </summary>
	# <remarks>
	# This state is used to restore test view's state when decompilation is started by Go Back/Forward action.
	# </remarks>
	def get_TextViewState(self):

	def set_TextViewState(self, value):

	TextViewState = property(fget=get_TextViewState, fset=set_TextViewState)

	def __init__(self):
		self.DecompilerSettings = DecompilerSettingsPanel.CurrentDecompilerSettings