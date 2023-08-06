from django.db import models

from ._model import MsbModel
from ._model import MsbModelManager
from ._fields import EncryptedString


class ConfigurationModelManager(MsbModelManager):
	pass


# Configuration model
class Configuration(MsbModel):
	# meta data
	class Meta:
		abstract = True
		indexes = [models.Index(fields=['name', 'key'])]

	# Model fields
	name = models.CharField(max_length=100, db_column='name')
	key = models.CharField(max_length=255, db_column='key')
	value = EncryptedString(db_column='value')

	# assign a custom manager to the model
	objects = ConfigurationModelManager()

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name
