import hashlib, random
from cryptography.fernet import Fernet, InvalidToken


class Hash(object):
    '''
        Creates decrypted tokens
    '''

    _fernet_key = 'dEiflQr6_TunDrQnSMEw0VSFaOZ-7zRrPDVlimrC0HM='

    @staticmethod
    def _generatesalt():
        salt = hashlib.sha1(str(random.random()).encode('utf-8'))
        return salt.hexdigest()

    @staticmethod
    def createhashforstring(string):
        ''' createhashforstring '''
        salt = Hash._generatesalt()
        salt = salt[0:5] + string + salt[0:5]
        return hashlib.sha1(salt.encode('utf-8')).hexdigest()

    @staticmethod
    def encrypt_string(plain_text):
        ''' encrypt_string '''
        cipher_suite = Fernet(Hash._fernet_key)
        plain_text = plain_text.encode('utf-8')
        return cipher_suite.encrypt(plain_text)

    @staticmethod
    def decrypt_string(encrypted_text):
        ''' decrypt_string'''
        cipher_suite = Fernet(Hash._fernet_key)
        try:
            return cipher_suite.decrypt(encrypted_text)
        except InvalidToken:
            return b''

