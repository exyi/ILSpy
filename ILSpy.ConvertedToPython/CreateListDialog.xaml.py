from System import *
from System.Windows import *
from System.Windows.Controls import *

class CreateListDialog(Window):
	""" <summary>
	 Interaction logic for Create.xaml
	 </summary>
	"""
	def __init__(self):
		self.InitializeComponent()

	def TextBox_TextChanged(self, sender, e):
		okButton.IsEnabled = not str.IsNullOrWhiteSpace(ListName.Text)

	def OKButton_Click(self, sender, e):
		if not str.IsNullOrWhiteSpace(ListName.Text):
			self._DialogResult = True

	def get_NewListName(self):
		return ListName.Text

	NewListName = property(fget=get_NewListName)