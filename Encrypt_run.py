# -*- coding: gb2312 -*-
import sys
from PyQt5.QtWidgets import QApplication, QDialog , QMainWindow, QFileDialog, QMessageBox, QInputDialog
from PyQt5.uic import loadUiType
from Encrypt import Ui_Dialog
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import os


class En_Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ����ť�ĵ���ź����Զ���Ĳۺ�����������
        #�����ļ�
        self.Choose_File.clicked.connect(self.Select_multiple_files)
        self.En_file.clicked.connect(self.AES_Encrypt_files)
        
        #������Կ
        self.Choose_keyFile.clicked.connect(self.Select_multiple_files_2)
        self.En_key.clicked.connect(self.RSA_Encrypt_keys)
        


    def Select_multiple_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "ѡ���ļ�", "/", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt);;Docx Files (*.docx)")
        if file_paths:
            file_list_text = "\n".join(file_paths)  # ���ļ�·���б�ת��Ϊ�ַ�����ÿ���ļ�·��ռһ��
            self.FileEdit.setPlainText(file_list_text)  # ���ַ����������õ�QTextEdit����ʾ
            

    def Select_multiple_files_2(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "ѡ���ļ�", "/", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt);;Docx Files (*.docx)")
        if file_paths:
            file_list_text = "\n".join(file_paths)  # ���ļ�·���б�ת��Ϊ�ַ�����ÿ���ļ�·��ռһ��
            self.KeyEdit.setPlainText(file_list_text)  # ���ַ����������õ�QTextEdit����ʾ

    def AES_Encrypt_files(self):
    # �����ļ�ѡ��Ի������û�ѡ����Կ�ļ�
        key_file_path, _ = QFileDialog.getOpenFileName(self, "ѡ����Կ�ļ�", "", "Key Files (*.bin);;All Files (*)")
        if key_file_path:
            try:
                with open(key_file_path, 'rb') as key_file:
                    key = key_file.read()
                if len(key) not in [16, 24, 32]:  # �����Կ�����Ƿ����AES��׼��16��24��32�ֽڷֱ��ӦAES-128��AES-192��AES-256��
                    QMessageBox.warning(self, "����", "��Կ���Ȳ�����AES��׼����ѡ����ȷ����Կ�ļ�")
                    return
                file_paths_text = self.FileEdit.toPlainText()
                file_paths = file_paths_text.splitlines()
                for file_path in file_paths:
                    if file_path:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        cipher = AES.new(key, AES.MODE_ECB)
                        # ������Ҫ�����ֽ���
                        padding_length = AES.block_size - (len(file_data) % AES.block_size)
                        if padding_length == 0:
                            padding_length = AES.block_size
                        # ��������ֽڴ�
                        padding = bytes([padding_length]) * padding_length
                        padded_data = file_data + padding
                        encrypted_data = cipher.encrypt(padded_data)
                        dir_name = os.path.dirname(file_path)
                        file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
                        encrypted_file_name = file_name_without_ext + '_encrypted' + os.path.splitext(file_path)[1]
                        encrypted_file_path = os.path.join(dir_name, encrypted_file_name)
                        with open(encrypted_file_path, 'wb') as f:
                            f.write(encrypted_data)
                QMessageBox.information(self, "��ʾ", "�ļ����������")
            except FileNotFoundError:
                QMessageBox.warning(self, "����", "ָ������Կ�ļ������ڣ�������ѡ��")
            except Exception as e:
                QMessageBox.warning(self, "����", f"���ܹ��̳��ִ���: {str(e)}")
        else:
            QMessageBox.warning(self, "��ʾ", "��ѡ����Կ�ļ����ٽ��м��ܲ���")
    

    def RSA_Encrypt_keys(self):
        key_file_paths_text = self.KeyEdit.toPlainText()
        key_file_paths = key_file_paths_text.splitlines()
        if not key_file_paths:
            QMessageBox.warning(self, "��ʾ", "����ѡ��Ҫ���ܵ�AES��Կ�ļ�")
            return
        # �����ļ�ѡ��Ի������û�ѡ��RSA��Կ�ļ�
        rsa_public_key_file_path, _ = QFileDialog.getOpenFileName(self, "ѡ��RSA��Կ�ļ�", "", "RSA Public Key Files (*.pem);;All Files (*)")
        if not rsa_public_key_file_path:
            QMessageBox.warning(self, "��ʾ", "��ѡ��RSA��Կ�ļ����ٽ��м��ܲ���")
            return
        try:
            with open(rsa_public_key_file_path, 'rb') as rsa_public_key_file:
                rsa_public_key = RSA.import_key(rsa_public_key_file.read())
            rsa_cipher = PKCS1_OAEP.new(rsa_public_key)
            for key_file_path in key_file_paths:
                if key_file_path:
                    with open(key_file_path, 'rb') as key_file:
                        aes_key_data = key_file.read()
                    encrypted_aes_key_data = rsa_cipher.encrypt(aes_key_data)
                    encrypted_key_file_name = os.path.basename(key_file_path) + '.encrypted'
                    encrypted_key_file_path = os.path.join(os.path.dirname(key_file_path), encrypted_key_file_name)
                    with open(encrypted_key_file_path, 'wb') as encrypted_key_file:
                        encrypted_key_file.write(encrypted_aes_key_data)
            QMessageBox.information(self, "��ʾ", "AES��Կ�ļ����������")
        except FileNotFoundError as e:
            QMessageBox.warning(self, "����", f"�ļ������ڴ���: {str(e)}")
        except ValueError as e:
            QMessageBox.warning(self, "����", f"��Կ��ʽ����ܲ�������: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "����", f"���ܹ��̳���δ֪����: {str(e)}")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    AES_Windows = En_Dialog()
    AES_Windows.show()
    sys.exit(app.exec_())
    


 
 