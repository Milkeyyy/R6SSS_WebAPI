from contextlib import asynccontextmanager
import datetime
import os
from os import getenv
import traceback
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import httpx
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app import App as AppInfo
import db
from logger import logger


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
	print(f"{AppInfo.name()} - v{AppInfo.version_text()}\nDeveloped by {AppInfo.author()}\n{AppInfo.copyright()}")

	# .envファイルが存在する場合はファイルから環境変数を読み込む
	env_path = os.path.join(os.getcwd(), ".env")
	if os.path.isfile(env_path):
		logger.info("環境変数を読み込み: %s", env_path)
		load_dotenv(env_path)

	# スケジュールDBへ接続
	db.connect()

	# サーバーステータスを更新
	await ServerStatusManager.update_status()

	yield

	logger.info("Bye.")

def get_fwd_ipddr(request: Request) -> str:
	"""クライアントのIPアドレスをヘッダーから取得する"""

	if "cf-connecting-ip" in request.headers:
		return request.headers["cf-connecting-ip"]

	if "x-forwarded-for" in request.headers:
		return request.headers["x-forwarded-for"]

	if not request.client or not request.client.host:
		return "127.0.0.1"

	return request.client.host

# レート制限リミッター
limiter = Limiter(key_func=get_fwd_ipddr)
# FastAPI
app = FastAPI(lifespan=lifespan, docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")

# リミッターを設定
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class ServerStatus:
	data: dict

	def __init__(self, data: dict) -> None:
		self.data = data

	@property
	def platform(self) -> str | None:
		if "Platform" in self.data:
			return self.data["Platform"]
		return None

	@property
	def status(self) -> str | None:
		if "Status" in self.data:
			return self.data["Status"]
		return None

class ServerStatusManager:
	# サーバーステータスAPIのURL
	# API_URL = "https://game-status-api.ubisoft.com/v1/instances?spaceIds=57e580a1-6383-4506-9509-10a390b7e2f1,05bfb3f7-6c21-4c42-be1f-97a33fb5cf66,96c1d424-057e-4ff7-860b-6b9c9222bdbf,98a601e5-ca91-4440-b1c5-753f601a2c90,631d8095-c443-4e21-b301-4af1a0929c27"
	# API_URL_PC = "https://game-status-api.ubisoft.com/v1/instances?appIds=e3d5ea9e-50bd-43b7-88bf-39794f4e3d40"
	API_URL = "https://public-ubiservices.ubi.com/v1/applications/gameStatuses"
	API_URL_QUERY_PF = [ # アプリケーションID一覧
		"e3d5ea9e-50bd-43b7-88bf-39794f4e3d40", # PC
		"fb4cc4c9-2063-461d-a1e8-84a7d36525fc", # PS4
		"4008612d-3baf-49e4-957a-33066726a7bc", # Xbox One
		"6e3c99c9-6c3f-43f4-b4f6-f1a3143f2764", # PS5
		"76f580d5-7f50-47cc-bbc1-152d000bfe59"  # Xbox Series X/S
	]

	DEFAULT_PLATFORM_STATUS: dict = {
		"Status": {
			"Connectivity": "Unknown",
			"Features": {
				"Authentication": "Unknown",
				"Leaderboard": "Unknown",
				"Matchmaking": "Unknown",
				"Purchase": "Unknown"
			},
			"Maintenance": None
		},
		"UpdatedAt": None
	}

	# サーバーステータス辞書を初期化
	data: dict = {}

	# サーバーステータスを取得して整えて返す
	@classmethod
	async def get_server_status(cls):
		logger.info("サーバーステータスを取得")
		# サーバーステータスを取得する
		async with httpx.AsyncClient(timeout=15.0) as client:
			res = await client.get(
				cls.API_URL,
				params={
					"applicationIds": ",".join(cls.API_URL_QUERY_PF)
				},
				headers={
					"Ubi-Appid": "f612511e-58a2-4e9a-831f-61838b1950bb",
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
				}
			) # PC以外

		# ステータスコードが200ではない場合は不明というステータスを返す
		if res.status_code != 200:
			logger.error("サーバーステータスの取得に失敗 - ステータスコード: %s", {res.status_code})
			status = cls.DEFAULT_PLATFORM_STATUS.copy()
			return status

		raw_status = res.json()
		game_statuses = None

		if len(raw_status["gameStatuses"]) > 0:
			game_statuses = raw_status["gameStatuses"]

		if game_statuses is None:
			logger.error("取得失敗")
			logger.debug(str(raw_status))
			return cls.data

		logger.info("取得完了")
		logger.debug(str(raw_status))

		# 各プラットフォームのステータスをループ、ステータス辞書に加える
		status = {}
		for s in game_statuses:
			p = s["platformType"]
			# プラットフォームのキーを以前のものへ戻す
			if p == "ORBIS":
				p = "PS4"
			elif p == "DURANGO":
				p = "XB1"
			elif p == "XboxScarlett":
				p = "XBSX"
			status[p] = cls.DEFAULT_PLATFORM_STATUS.copy()

			if s["status"] == "online":
				status[p]["Status"]["Connectivity"] = "Operational"
				for fk in status[p]["Status"]["Features"].keys():
					status[p]["Status"]["Features"][fk] = "Operational"

			# ImpactedFeatures をループする リストに含まれる場合は停止中なので、該当するステータスをOutageにする
			for f in s["impactedFeatures"]:
				status[p]["Status"]["Features"][f] = "Outage"

			# Maintenance が null の場合はステータスの Maintenance に False をセットする
			if s["isMaintenance"] == False:
				status[p]["Status"]["Maintenance"] = False
			else:
				status[p]["Status"]["Maintenance"] = s["isMaintenance"]

			# 最終更新日時を更新する
			status[p]["UpdatedAt"] = datetime.datetime.fromisoformat(raw_status["lastModifiedAt"]).timestamp()

		logger.info("サーバーステータスの整形完了")
		logger.debug(str(status))

		return status

	@classmethod
	async def update_status(cls):
		cls.data = await cls.get_server_status()


@app.post("/__update")
async def update_serverstatus(key: str = None):
	if key is None:
		return JSONResponse(
			content=jsonable_encoder({"detail": "Key is undefined"}),
			status_code=401
		)
	elif key != getenv("UPDATE_KEY"):
		return JSONResponse(
			content=jsonable_encoder({"detail": "Invalid key"}),
			status_code=401
		)

	await ServerStatusManager.update_status()
	logger.info("Server Status Updated: %s" , str(ServerStatusManager.data))
	return JSONResponse(
		content=jsonable_encoder({"detail": "OK"}),
		status_code=200
	)


@app.get("/v2/status")
@limiter.limit("10/minute")
async def get_server_status_v2(request: Request, platform: List[str] = Query(default=None)):
	status = {}

	try:
		logger.info("Client IP: %s", get_fwd_ipddr(request))
		# パラメーターが指定されていない場合は全てのプラットフォームのステータスを返す
		if platform is None:
			status = ServerStatusManager.data
		else:
			# 指定されたプラットフォームのステータスだけ返す
			for p in platform:
				d = ServerStatusManager.data.get(p)
				if d is not None:
					status[p] = d
	except Exception:
		logger.error(traceback.format_exc())
		return JSONResponse(
			content=jsonable_encoder({"detail": "Internal Server Error"}),
			status_code=500
		)

	# JSONでサーバーステータスのデータを返す
	return JSONResponse(
		content=jsonable_encoder({
			"info": { 
				"name": AppInfo.name(),
				"version": AppInfo.version_text(),
				"author": AppInfo.author()
			},
			"detail": "OK",
			"data": status
		}),
		status_code=200
	)

@app.get("/v2/schedule/latest")
@limiter.limit("10/minute")
async def get_latest_maintenance_schedule_v2(request: Request):
	try:
		logger.info("Client IP: %s", get_fwd_ipddr(request))

		# データベースからスケジュール情報を取得
		data = db.collection.find_one(sort=([("_id", db.pymongo.DESCENDING),]))

		if data is None:
			return JSONResponse(content=jsonable_encoder({"detail": "No schedule information found.", "result": False, "data": data}), status_code=404)

		# 取得したデータからIDを削除する
		data.pop("_id")

		# JSONでスケジュールのデータを返す
		return JSONResponse(
			content=jsonable_encoder({
				"info": { 
					"name": AppInfo.name(),
					"version": AppInfo.version_text(),
					"author": AppInfo.author()
				},
				"detail": "OK",
				"data": data
			}),
			status_code=200
		)

		# パラメーターが指定されていない場合は全てのプラットフォームのステータスを返す
		# if platform is None:
		# 	status = ServerStatusManager.data
		# else:
		# 	# 指定されたプラットフォームのステータスだけ返す
		# 	for p in platform:
		# 		d = ServerStatusManager.data.get(p)
		# 		if d is not None:
		# 			status[p] = d
	except Exception:
		logger.error(traceback.format_exc())
		return JSONResponse(
			content=jsonable_encoder({"detail": "Internal Server Error"}),
			status_code=500
		)

	# JSONでサーバーステータスのデータを返す
	return JSONResponse(
		content=jsonable_encoder({
			"info": { 
				"name": AppInfo.name(),
				"version": AppInfo.version_text(),
				"author": AppInfo.author()
			},
			"detail": "OK",
			"data": data
		}),
		status_code=200
	)
