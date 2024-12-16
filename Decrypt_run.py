# -*- coding: gb2312 -*-
import sys
from PyQt5.QtWidgets import QApplication, QDialog , QMainWindow, QFileDialog, QMessageBox, QInputDialog
from PyQt5.uic import loadUiType
from Decrypt import Ui_Dialog
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import os


class De_Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ����ť�ĵ���ź����Զ���Ĳۺ�����������
        
        #������Կ
        self.Choose_keyFile.clicked.connect(self.Select_multiple_files)
        self.Decrypt_key.clicked.connect(self.RSA_Decrypt_keys)
        
        #�����ļ�
        self.Choose_File.clicked.connect(self.Select_multiple_files_2)
        self.Decrypt_file.clicked.connect(self.AES_Decrypt_files)



    def Select_multiple_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "ѡ���ļ�", "/", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt);;Docx Files (*.docx)")
        if file_paths:
            file_list_text = "\n".join(file_paths)  # ���ļ�·���б�ת��Ϊ�ַ�����ÿ���ļ�·��ռһ��
            self.keyEdit.setPlainText(file_list_text)  # ���ַ����������õ�QTextEdit����ʾ
    def Select_multiple_files_2(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "ѡ���ļ�", "/", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt);;Docx Files (*.docx)")
        if file_paths:
            file_list_text = "\n".join(file_paths)  # ���ļ�·���б�ת��Ϊ�ַ�����ÿ���ļ�·��ռһ��
            self.fileEdit.setPlainText(file_list_text)  # ���ַ����������õ�QTextEdit����ʾ

            
    def AES_Decrypt_files(self):
        # �����ļ�ѡ��Ի������û�ѡ����Կ�ļ�
        key_file_path, _ = QFileDialog.getOpenFileName(self, "ѡ����Կ�ļ�", "", "Key Files (*.bin);;All Files (*)")
        if key_file_path:
            try:
                with open(key_file_path, 'rb') as key_file:
                    key = key_file.read()
                if len(key) not in [16, 24, 32]:  # �����Կ�����Ƿ����AES��׼��16��24��32�ֽڷֱ��ӦAES-128��AES-192��AES-256��
                    QMessageBox.warning(self, "����", "��Կ���Ȳ�����AES��׼����ѡ����ȷ����Կ�ļ�")
                    return
                file_paths_text = self.fileEdit.toPlainText()
                file_paths = file_paths_text.splitlines()
                for file_path in file_paths:
                    if file_path:
                        with open(file_path, 'rb') as f:
                            encrypted_data = f.read()
                        cipher = AES.new(key, AES.MODE_ECB)
                        # �Ƚ��н��ܲ���
                        decrypted_data = cipher.decrypt(encrypted_data)
                        # ��ȡ�����ֽ��������һ���ֽڱ�ʾ�����ֽ�����
                        padding_length = decrypted_data[-1]
                        # ��֤��䳤���Ƿ�Ϸ�
                        if padding_length < 1 or padding_length > AES.block_size:
                            raise ValueError("��Ч����䳤��")
                        # ��֤��������Ƿ���ȷ������PKCS7����ĩβ�����ֽڶ�Ӧ������䳤��ֵ��Ӧ���ֽڣ�
                        expected_padding = bytes([padding_length]) * padding_length
                        if decrypted_data[-padding_length:]!= expected_padding:
                            raise ValueError("�����֤ʧ��")
                        # ȥ������ֽڵõ������Ľ�������
                        decrypted_data = decrypted_data[:-padding_length]
                        dir_name = os.path.dirname(file_path)
                        file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
                        decrypted_file_name = file_name_without_ext + '_decrypted' + os.path.splitext(file_path)[1]
                        decrypted_file_path = os.path.join(dir_name, decrypted_file_name)
                        with open(decrypted_file_path, 'wb') as f:
                            f.write(decrypted_data)
                # �����ļ�������ɺ󣬵�����ʾ������֪�û�
                QMessageBox.information(self, "��ʾ", "�ļ����������")
            except FileNotFoundError:
                QMessageBox.warning(self, "����", "ָ�����ļ������ڣ�������ѡ��")
            except ValueError as ve:
                QMessageBox.warning(self, "����", f"���ܹ��̳��ִ���: {str(ve)}")
            except Exception as e:
                QMessageBox.warning(self, "����", f"���ܹ��̳��ִ���: {str(e)}")
        else:
            QMessageBox.warning(self, "��ʾ", "��ѡ����Կ�ļ����ٽ��н��ܲ���")
            


    def RSA_Decrypt_keys(self):
        encrypted_key_file_paths_text = self.keyEdit.toPlainText()
        encrypted_key_file_paths = encrypted_key_file_paths_text.splitlines()
        if not encrypted_key_file_paths:
            QMessageBox.warning(self, "��ʾ", "����ѡ��Ҫ���ܵļ���AES��Կ�ļ�")
            return
        # �����ļ�ѡ��Ի������û�ѡ��RSA˽Կ�ļ�
        rsa_private_key_file_path, _ = QFileDialog.getOpenFileName(self, "ѡ��RSA˽Կ�ļ�", "", "RSA Private Key Files (*.pem);;All Files (*)")
        if not rsa_private_key_file_path:
            QMessageBox.warning(self, "��ʾ", "��ѡ��RSA˽Կ�ļ����ٽ��н��ܲ���")
            return
        try:
            with open(rsa_private_key_file_path, 'rb') as rsa_private_key_file:
                rsa_private_key = RSA.import_key(rsa_private_key_file.read())
            rsa_cipher = PKCS1_OAEP.new(rsa_private_key)
            for encrypted_key_file_path in encrypted_key_file_paths:
                if encrypted_key_file_path:
                    with open(encrypted_key_file_path, 'rb') as encrypted_key_file:
                        encrypted_aes_key_data = encrypted_key_file.read()
                    try:
                        decrypted_aes_key_data = rsa_cipher.decrypt(encrypted_aes_key_data)
                    except ValueError as e:
                        QMessageBox.warning(self, "����", f"����ʧ�ܣ���������Կ��ƥ�����������: {str(e)}")
                        continue
                    decrypted_key_file_name = os.path.basename(encrypted_key_file_path).replace('.encrypted', '')
                    decrypted_key_file_path = os.path.join(os.path.dirname(encrypted_key_file_path), decrypted_key_file_name)
                    with open(decrypted_key_file_path, 'wb') as decrypted_key_file:
                        decrypted_key_file.write(decrypted_aes_key_data)
            QMessageBox.information(self, "��ʾ", "AES��Կ�ļ����������")
        except FileNotFoundError as e:
            QMessageBox.warning(self, "����", f"�ļ������ڴ���: {str(e)}")
        except ValueError as e:
            QMessageBox.warning(self, "����", f"��Կ��ʽ����ܲ�������: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "����", f"���ܹ��̳���δ֪����: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Encrypt_windows = De_Dialog()
    Encrypt_windows.show()
    sys.exit(app.exec_())
    


 
 