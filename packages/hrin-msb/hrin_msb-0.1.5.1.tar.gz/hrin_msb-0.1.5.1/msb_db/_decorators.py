def configuration_object(klass):
	def config_loader(self):
		if self._config_model is not None:
			config_list = self._config_model.objects.filter(name=self._config_name).all()
			if len(config_list) > 0:
				for config in config_list:
					setattr(self, config.key, config.value)

	setattr(klass, "__init__", config_loader)
	return klass
