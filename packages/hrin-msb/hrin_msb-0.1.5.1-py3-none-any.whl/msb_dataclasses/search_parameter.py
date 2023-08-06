from dataclasses import dataclass


@dataclass
class SearchParameter:
	_model_filters: dict
	_fields: list = None
	_order_by: str = None
	_limit: int = None
	_offset: int = None
	_order_field:str = None

	def __init__(self,**kwargs):
		self._model_filters = dict()
		self._fields        = kwargs.get('fields') if kwargs.get('fields') else []
		self._order_by      = kwargs.get('order_by') if kwargs.get('order_by') else 'ASC'
		self._limit         = kwargs.get('limit') if kwargs.get('limit') else 50
		self._offset        = kwargs.get('offset') if kwargs.get('offset') else 0
		self.order_field    = kwargs.get('order_field')

	def add_filters(self,key:str,value):
		if isinstance(key,str) and value is not None:
			self._model_filters[key] = value

	@property
	def filters(self) -> dict:
		return self._model_filters

	@property
	def fields(self) -> list:
		return self._fields

	@property
	def order_by(self) -> str:
		return self._order_by

	@property
	def limit(self) -> int:
		return self._limit

	@property
	def offset(self) -> int:
		return self._offset

	@property
	def order_field(self) -> str:
		return self._order_field


	@order_field.setter
	def order_field(self, value):
		if value is not None:
			if self.order_by is not 'ASC':
				self._order_field = f"-{value}"
			else:
				self._order_field = value

