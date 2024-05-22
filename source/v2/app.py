import json


class App:
	"""アプリケーション"""

	data: dict

	@staticmethod
	def name() -> str:
		"""名前"""
		return App.data["name"]

	@staticmethod
	def description() -> str:
		"""説明"""
		return App.data["description"].format(App.name())

	@staticmethod
	def version() -> str:
		"""バージョン"""
		return App.data["version"]

	@staticmethod
	def build() -> float:
		"""内部バージョン"""
		return App.data["build"]

	@staticmethod
	def author() -> str:
		"""作者"""
		return App.data["author"]

	@staticmethod
	def copyright() -> str:
		"""著作権表記"""
		return App.data["copyright"].format(App.author())

with open("app.json", mode="r", encoding="utf-8") as f:
	App.data = json.loads(f.read())
