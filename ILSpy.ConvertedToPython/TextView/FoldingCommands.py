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
from System.Linq import *
from ICSharpCode.AvalonEdit import *
from ICSharpCode.AvalonEdit.Folding import *

class ToggleAllContextMenuEntry(IContextMenuEntry):
	def IsVisible(self, context):
		return context.TextView != None

	def IsEnabled(self, context):
		return context.TextView != None and context.TextView.FoldingManager != None

	def Execute(self, context):
		if None == context.TextView:
			return 
		foldingManager = context.TextView.FoldingManager
		if None == foldingManager:
			return 
		doFold = True
		enumerator = foldingManager.AllFoldings.GetEnumerator()
		while enumerator.MoveNext():
			fm = enumerator.Current
			if fm.IsFolded:
				doFold = False
				break
		enumerator = foldingManager.AllFoldings.GetEnumerator()
		while enumerator.MoveNext():
			fm = enumerator.Current
			fm.IsFolded = doFold

class ToggleContextMenuEntry(IContextMenuEntry):
	def IsVisible(self, context):
		return context.TextView != None

	def IsEnabled(self, context):
		return context.TextView != None and context.TextView.FoldingManager != None

	def Execute(self, context):
		textView = context.TextView
		if None == textView:
			return 
		editor = textView.textEditor
		foldingManager = context.TextView.FoldingManager
		if None == foldingManager:
			return 
		# TODO: or use Caret if position is not given?
		posBox = context.Position
		if None == posBox:
			return 
		pos = posBox.Value
		# look for folding on this line:
		folding = foldingManager.GetNextFolding(editor.Document.GetOffset(pos.Line, 1))
		if folding == None or editor.Document.GetLineByOffset(folding.StartOffset).LineNumber != pos.Line:
			# no folding found on current line: find innermost folding containing the mouse position
			folding = foldingManager.GetFoldingsContaining(editor.Document.GetOffset(pos.Line, pos.Column)).LastOrDefault()
		if folding != None:
			folding.IsFolded = not folding.IsFolded