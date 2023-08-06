def use_djnago(settings_dir: str, **kwargs):
	def outer_func(_func):
		from functools import wraps
		@wraps(_func)
		def inner_func(*args, **kwargs):
			from msb_devtools import init_django_app
			init_django_app(settings_dir=settings_dir)
			return _func(*args, **kwargs)

		return inner_func

	return outer_func
