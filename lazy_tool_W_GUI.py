import os
# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory
os.chdir(script_dir)
import sys
import argparse
import openpyxl
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QRadioButton, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QComboBox, QMessageBox
import glob
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QRadioButton, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QComboBox, QMessageBox, QAction


class LazyToolGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lazy Tool")
        self.setGeometry(100, 100, 500, 300)
        self.manual_names_label = QLabel("Manual Names:")
        self.manual_names_input = QLineEdit()
        self.manual_names_input.setPlaceholderText("Enter names separated by comma")
        self.names_label = QLabel("Device List:")
        self.names_input = QComboBox()
        self.import_type = QComboBox()
        self.template_label = QLabel("Template:")
        self.template_input = QComboBox()
        self.template_input.addItems(glob.glob("templates_PLC/*"))
        self.directory_label = QLabel("Directory Name:")  # Added label for directory name
        self.directory_input = QLineEdit()  # Added input field for directory name
        self.generate_button = QPushButton("Generate Files")

        self.output_text = QTextEdit()
        self.names_input.addItems(glob.glob("Device Lists/*"))
        self.import_type.addItem("CM")
        self.import_type.addItem("IO")

        layout = QVBoxLayout()
        layout.addWidget(self.import_type)  # Add CM radio button to layout
        layout.addWidget(self.names_label)
        layout.addWidget(self.names_input)
        layout.addWidget(self.template_label)
        layout.addWidget(self.template_input)
        layout.addWidget(self.directory_label)  # Added directory label to layout
        layout.addWidget(self.directory_input)  # Added directory input field to layout
        layout.addWidget(self.generate_button)
        layout.addWidget(self.output_text)
        layout.addWidget(self.manual_names_label)
        layout.addWidget(self.manual_names_input)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.generate_button.clicked.connect(self.generate_files)
        self.import_type.currentTextChanged.connect(self.update_template_input)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu("Help")

        help_action = QAction("?", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def show_help(self):
        help_message = """How to Use
        Launch the Application: Run the lazy_tool_W_GUI.py script to start the application.

        Select Import Type: Choose between "CM" and "IO" from the dropdown menu at the top of the application.

        Select Device List: Choose the device list file from the dropdown menu labeled "Device List". This file should be located in the "Device Lists" directory.

        Select Template: Choose the template file from the dropdown menu labeled "Template". The available templates will depend on the selected import type and should be located in the "templates_PLC" or "templates_IO" directory.

        Enter Directory Name (Optional): If you want the generated files to be saved in a specific directory, enter the directory name in the "Directory Name" field. If this field is left blank, the files will be saved in the current working directory.

        Enter Manual Names (Optional): If you want to manually enter the names for the generated files, enter them in the "Manual Names" field, separated by commas. If this field is left blank, the names will be extracted from the selected device list file.

        Generate Files: Click the "Generate Files" button to start the file generation process. The names of the generated files will be displayed in the text area at the bottom of the application.

        Completion: Upon successful completion, a popup message saying "Files generated successfully!" will be displayed.

        Please note that the application assumes that the names are in the first column of the device list file and replaces '-' with '_' in the names. The application also replaces '' and the template file name (without extension) with the name in the template content."""
        QMessageBox.information(self, "Help", help_message)

    def update_template_input(self):
        selected_import_type = self.import_type.currentText()
        if selected_import_type == "CM":
            self.template_input.clear()
            self.template_input.addItems(glob.glob("templates_PLC/*"))
        else:
            self.template_input.clear()
            self.template_input.addItems(glob.glob("templates_IO/*"))
            
    def generate_files(self):
        # Get the output file from the user selection
        names_or_file = self.names_input.currentText()
        manual_names = self.manual_names_input.text()
        template_file = self.template_input.currentText()
        target_folder = self.directory_input.text()  # Get the directory name from the input field

        # Check if manual names were entered
        if manual_names:
            names = manual_names.split(",")
        else:
            # Read the file using openpyxl
            workbook = openpyxl.load_workbook(names_or_file)
            sheet = workbook.active

            # Get the names from the sheet
            names = []
            for row in sheet.iter_rows(values_only=True):
                name = row[0]  # Assuming the names are in the first column
                if name:
                    name = name.replace('-', '_')
                    names.append(name)

            # Close the workbook
            workbook.close()

        # Open the template file
        with open(template_file, 'r') as template_file_obj:
            template_content = template_file_obj.read()

        # Get the extension of the template file
        template_extension = Path(template_file).suffix

        if target_folder:
            # Check if the folder name is in the root directory
            if not os.path.isabs(target_folder):
                target_folder = os.path.join(script_dir, target_folder)

            # Create the target folder if it doesn't exist
            os.makedirs(target_folder, exist_ok=True)

        # Generate new files or append to the output file for each name
        for name in names:
            # Replace placeholder with the name in the template content
            new_content = template_content.replace('<NAME>', name)
            output_file = f"{name}_output{template_extension}"
            # Replace any occurrence of the template file name with the new name
            new_content = new_content.replace(Path(template_file).stem, name)

            if target_folder:
                # Create a new file with the name as the filename in the target folder
                new_filename = os.path.join(target_folder, f"{name}{template_extension}")
                with open(new_filename, 'w') as new_file:
                    new_file.write(new_content)
                self.output_text.append(f"Generated file: {new_filename}")
            else:
                # Save the file in the current working directory
                with open(output_file, 'w') as new_file:
                    new_file.write(new_content)
                self.output_text.append(f"Generated file: {output_file}")
                
        # Show a popup message when the files are generated
        QMessageBox.information(self, "Done", "Files generated successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LazyToolGUI()
    window.show()
    sys.exit(app.exec())
