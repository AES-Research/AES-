# -*- coding: gb2312 -*-
import sys
from PyQt5.QtWidgets import QApplication, QDialog , QFileDialog, QMessageBox
from PyQt5.uic import loadUiType
from Key_create import Ui_Dialog
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import os


class Key_Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ����ť�ĵ���ź����Զ���Ĳۺ�����������
        self.Create_randomAES_key.clicked.connect(self.Randomkey_create)
        self.Create_RSA_key.clicked.connect(self.RSAkey_create)

        
    def Randomkey_create(self):
        try:
            # ����ѡ���ļ��жԻ���
            dir_path = QFileDialog.getExistingDirectory(self, "ѡ�񱣴���Կ���ļ���")
            if dir_path:
                # ����AES-192�����Կ��24�ֽڣ�
                key = get_random_bytes(24)
                key_file_path = os.path.join(dir_path, "random_aes_192_key.bin")
                with open(key_file_path, 'wb') as f:
                    f.write(key)
                QMessageBox.information(self, "��ʾ", "��Կ�ļ�����ɹ�")
        except Exception as e:
            print(f"�������AES��Կʱ���ִ���: {str(e)}")
            
    def RSAkey_create(self):
        try:
            key = RSA.generate(2048)

            # ����˽Կ�͹�Կ
            private_key = key.export_key()
            public_key = key.publickey().export_key()
            dir_path = QFileDialog.getExistingDirectory(self, "ѡ�񱣴���Կ���ļ���")
            if dir_path:
                # ����˽Կ�͹�Կ��PEM�ļ���ʹ�ò�ͬ���ļ�����
                key_file_path = os.path.join(dir_path, "private_key.pem")
                with open(key_file_path, 'wb') as f:
                    f.write(private_key)
                key_file_path = os.path.join(dir_path, "public_key.pem")
                with open(key_file_path, 'wb') as f:
                    f.write(public_key)
                QMessageBox.information(self, "��ʾ", "��Կ�ļ�����ɹ�")
        except Exception as e:
            print(f"����RSA��Կʱ���ִ���: {str(e)}")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    AES_Windows = Key_Dialog()
    AES_Windows.show()
    sys.exit(app.exec_())