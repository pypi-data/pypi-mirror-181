import os

from cryptography.fernet import Fernet

from msb_exceptions import AppException


class AsymmetricCipher():
	pass


class SymmetricCipher():

	def __init__(self, keyname: str = "SECRET_KEY", key: str = None):
		self.key = os.environ.get('SECRET_KEY', default='')

	def encrypt(self, data=None) -> str:
		if self.key is not None:
			try:
				data = str(data).encode() if not isinstance(data, bytes) else data
				return Fernet(key=self.key).encrypt(data).decode()
			except Exception as e:
				pass

		return data

	def decrypt(self, data=None) -> str:
		if self.key is not None:
			try:
				data = str(data).encode() if not isinstance(data, bytes) else data
				return Fernet(key=self.key).decrypt(data).decode()
			except Exception as e:
				pass
		return data


class Cipher:

	@staticmethod
	def get_instance(asymetric=False):
		if asymetric:
			cipher = AsymmetricCipher()
		else:
			cipher = SymmetricCipher()
		return cipher

	@staticmethod
	def encrypt(data=None, asymetric=False):
		try:
			if data is None:
				raise AppException('Value is None')
			return Cipher.get_instance().encrypt(data)
		except Exception:
			return data

	@staticmethod
	def decrypt(data=None, asymetric=False):
		try:
			if data is None:
				raise AppException('Value is None')
			return Cipher.get_instance().decrypt(data)
		except Exception:
			return data
