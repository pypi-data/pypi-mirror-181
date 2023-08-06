class AuthUser:
	__auth_data = dict()

	def __getitem__(self, item):
		return self.__auth_data.get(item)

	def __init__(self, type: str = None, username: str = None, userid: str = None, **kwargs):
		self.__auth_data['auth_type'] = type
		self.__auth_data['userid'] = userid
		self.__auth_data['username'] = username
		self.__auth_data = dict(**self.__auth_data, **kwargs)
		self.__auth_data['is_authenticated'] = (
			username is not None and userid is not None
		)

	@property
	def id(self):
		return self.__auth_data.get('userid')

	@property
	def user(self):
		return self.id

	@property
	def username(self):
		return self.__auth_data.get('username')

	@property
	def is_authenticated(self) -> bool:
		return self.__auth_data.get('is_authenticated')

	@property
	def auth_data(self) -> dict:
		return self.__auth_data
