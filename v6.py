import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,QMessageBox,QInputDialog,QProgressBar
from cryptography.fernet import Fernet


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("ptcnbcFolder-encryptor app")
        self.create_ui_elements()
        self.create_progress_bar()


    def create_ui_elements(self):
        self.select_folder_label = QLabel("Select the folder you want to encrypt:", self)
        self.select_folder_label.setGeometry(30, 30, 250, 20)

        self.select_button = QPushButton("Select Folder", self)
        self.select_button.setGeometry(30, 60, 100, 30)
        self.select_button.clicked.connect(self.select_folder)

        self.encrypt_label = QLabel("", self)
        self.encrypt_label.setGeometry(150, 60, 250, 30)

        self.encrypt_button = QPushButton("Encrypt Selected Folder", self)
        self.encrypt_button.setGeometry(30, 100, 180, 30)
        self.encrypt_button.clicked.connect(self.encrypt_folder)

        self.decrypt_button = QPushButton("Decode selected Folder", self)
        self.decrypt_button.setGeometry(30, 140, 260, 30)
        self.decrypt_button.clicked.connect(self.decrypt_folder)

        self.result_label = QLabel("", self)
        self.result_label.setGeometry(30, 180, 500, 100)
    
    def create_progress_bar(self):
        # İlerleme çubuğu oluştur
        self.file_count = 0
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(30, 220, 440, 20)
        self.progress_bar.setVisible(False)

    def progress_bar_method(self):
        self.progress_bar.setRange(0, self.file_count)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if folder_path:
            self.encrypt_label.setText(f"Selected Folder: {folder_path}")
            self.selected_folder = folder_path

        for root, dirs, files in os.walk(self.selected_folder):
            self.file_count += len(files)

    def encrypt_folder(self):
        if hasattr(self, 'selected_folder'):
            key = Fernet.generate_key()
            fernet = Fernet(key)

            self.progress_bar_method()
            progress = 0

            for root, dirs, files in os.walk(self.selected_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    encrypted_data = fernet.encrypt(data)
                    with open(file_path, 'wb') as f:
                        f.write(encrypted_data)
                    progress += 1
                    self.progress_bar.setValue(progress)

            self.result_label.setText(f"Folder encrypted saved in directory with python code.encryption key:\n{key.decode()}")
            key_file_name = os.path.basename(self.selected_folder) + "_key.txt"
            with open(key_file_name,"wb") as f:
                f.write(key)
                # İlerleme çubuğunu gizle
                self.progress_bar.setVisible(False)
        else:
            QMessageBox.warning(self, "Hata", "Please select a folder.")
            return

    def decrypt_folder(self):
        if hasattr(self, 'selected_folder'):
            key, ok = QInputDialog.getText(self, "Decryption Key", "Enter Encryption Key:")
            if ok:
                try:
                    self.progress_bar_method()
                    progress = 0
                    for root, dirs, files in os.walk(self.selected_folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'rb') as f:
                                data = f.read()
                            decrypted_data = Fernet(key).decrypt(data)
                            with open(file_path, 'wb') as f:
                                f.write(decrypted_data)
                            progress += 1
                            self.progress_bar.setValue(progress)

                    self.result_label.setText(f"Folder decrypted and encryption key used.")
                    # İlerleme çubuğunu gizle
                    self.progress_bar.setVisible(False)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"An error occurred during decryption. your password may not be correct.: {str(e)}")
            else:
                QMessageBox.warning(self, "Error", "Please enter an encryption key.")
        else:
            QMessageBox.warning(self, "Error", "Please select a folder.")
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

# password that can never be cracked  ptcnbc app