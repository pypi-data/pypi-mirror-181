import os
import sys


def add_paths_to_system(*path_list):
	for path in path_list:
		sys.path.append(path)


def init_django_app(settings_dir: str, **kwargs):
	import django
	if isinstance(kwargs.get('sys_pathlist'), list):
		add_paths_to_system(*kwargs.get('sys_pathlist'))

	os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{settings_dir}.settings")
	os.environ.setdefault("PYTHONUNBUFFERED", "1")


	django.setup()


def log_to_console(msg, format=False):
	_log_message = f"\n{f'[ {msg} ] ' :*^100}" if format else f"LOG : {msg}"
	return print(_log_message)
