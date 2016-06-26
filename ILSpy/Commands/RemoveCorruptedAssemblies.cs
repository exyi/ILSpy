using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ICSharpCode.ILSpy.Commands
{
	[ExportMainMenuCommand(Menu = "_File", Header = "Remove Corrupted Assemblies", MenuIcon = "Images/AssemblyWarning.png", MenuCategory = "Open", MenuOrder = 3)]
	public sealed class RemoveCorruptedAssemblies : SimpleCommand
	{
		public override void Execute(object parameter)
		{
			var window = MainWindow.Instance;
			window.RemoveCurruptedAssemblies();
		}
	}
}
