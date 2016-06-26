using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace ICSharpCode.ILSpy.Commands
{
	[ExportMainMenuCommand(Menu = "_File", Header = "Open All Assemblies In _Directory", MenuIcon = "Images/AssemblyList.png", MenuCategory = "Open", MenuOrder = 2)]
	public sealed class OpenAllInDirectoryCommand : SimpleCommand
	{
		public override void Execute(object parameter)
		{
			var dlg = new System.Windows.Forms.FolderBrowserDialog();
			dlg.Description = "Open All Assemblies In The Directory";
			if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK) {
				MainWindow.Instance.OpenFiles(
					Directory.GetFiles(dlg.SelectedPath, "*", SearchOption.AllDirectories)
						.Where(f => f.EndsWith(".dll", StringComparison.OrdinalIgnoreCase) || f.EndsWith(".exe", StringComparison.OrdinalIgnoreCase))
						.ToArray(),
					removeUnloadable: true);
			}
		}
	}
}
