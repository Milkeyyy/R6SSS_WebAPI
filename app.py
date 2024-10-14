import json


class App:
	"""アプリケーション"""

	data: dict

	@classmethod
	def name(cls) -> str:
		"""名前"""
		return cls.data["name"]

	@classmethod
	def description(cls) -> str:
		"""説明"""
		return cls.data["description"].format(cls.name())

	@classmethod
	def version(cls) -> str:
		"""バージョン"""
		return cls.data["version"]

	@classmethod
	def build(cls) -> float:
		"""内部バージョン"""
		return cls.data["build"]

	@classmethod
	def version_text(cls) -> str:
		"""バージョン表記"""
		return cls.version() + "-" + str(cls.build())

	@classmethod
	def author(cls) -> str:
		"""作者"""
		return cls.data["author"]

	@classmethod
	def copyright(cls) -> str:
		"""著作権表記"""
		return cls.data["copyright"].format(cls.author())

with open("../app.json", mode="r", encoding="utf-8") as f:
	App.data = json.loads(f.read())
