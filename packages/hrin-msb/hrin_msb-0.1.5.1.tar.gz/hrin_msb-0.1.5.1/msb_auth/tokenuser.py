from django.utils.functional import cached_property


class TokenUser:
	token: dict
	__auth_data: dict

	def __init__(self, tokendata: dict = None):
		self.token = tokendata if tokendata else dict()

	def __str__(self):
		return f"<TokenUser,id={self.userid},user={self.username}>"

	def __hash__(self):
		return hash(self.use)

	def __getattr__(self, attr):
		"""This acts as a backup attribute getter for custom claims defined in Token serializers."""
		return self.token.get(attr, None)

	def set_validation_status(self, status: bool = False):
		self.token['is_valid'] = status

	def get(self, key: str = '', default=None):
		val = self.__auth_data.get(key)
		return val if val is not None else None

	@cached_property
	def userid(self):
		return self.get('userid')

	@cached_property
	def username(self):
		return self.get('username')

	@cached_property
	def auth_type(self):
		return self.get('auth_type')

	@cached_property
	def is_admin(self):
		return self.get("is_admin")

	@property
	def is_valid(self):
		return self.token.get('is_valid', False)

	@property
	def is_authenticated(self):
		return self.get('is_authenticated', False) and self.is_valid

	@property
	def role(self):
		return self.get('role')

	@property
	def id(self):
		return self.get('employee_number')

	def __set_auth_data(self):
		self.__auth_data = self.token.get('userdata').get('auth_data') if self.token else dict()
