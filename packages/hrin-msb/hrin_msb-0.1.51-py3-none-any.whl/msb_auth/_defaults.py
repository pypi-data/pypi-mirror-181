from datetime import timedelta

from .tokenuser import TokenUser
from msb_config.env import Config


def jwt_user_auth_rule(user: TokenUser):
	return user


JWT_TOKEN_SETTINGS = {

	'USER_AUTHENTICATION_RULE': 'auth_management.core.rules.jwt_user_auth_rule',
	'TOKEN_USER_CLASS': 'msb_auth.TokenUser',
	'ALGORITHM': 'HS256',
	'SIGNING_KEY': Config.get('JWT_TOKEN_SIGNING_KEY', default=None),
	'VERIFYING_KEY': Config.get('JWT_TOKEN_VERIFY_KEY', default=None),

	'AUTH_HEADER_TYPES': ('Bearer',),
	'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
	'USER_ID_FIELD': 'userid',
	'USER_ID_CLAIM': 'id',
	'TOKEN_TYPE_CLAIM': 'token_type',
	'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
	'JTI_CLAIM': 'jti',

	'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(Config.get('JWT_ACCESS_TOKEN_VALIDITY', default=30).as_str())),
	'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(Config.get('JWT_REFRESH_TOKEN_VALIDITY', default=1440).as_str())),

	'ROTATE_REFRESH_TOKENS': False,
	'BLACKLIST_AFTER_ROTATION': False,
	'AUDIENCE': Config.get('BASE_URL', default=None),
	'ISSUER': Config.get('BASE_URL', default=None),

}
