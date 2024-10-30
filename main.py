from contextlib import asynccontextmanager
import datetime
import json
from os import getenv
import traceback
from typing import List
from urllib import request

from fastapi import FastAPI, Request, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_ipaddr, get_remote_address
from slowapi.errors import RateLimitExceeded

from app import App as AppInfo
from logger import logger


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info(f"{AppInfo.name()} - v{AppInfo.version_text()}\nDeveloped by {AppInfo.author()}\n{AppInfo.copyright()}")

	# サーバーステータスを更新
	ServerStatusManager.update_status()

	yield

	logger.info("Bye.")

limiter = Limiter(key_func=get_ipaddr)
app = FastAPI(lifespan=lifespan, docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")
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
	API_URL = "https://game-status-api.ubisoft.com/v1/instances?spaceIds=57e580a1-6383-4506-9509-10a390b7e2f1,05bfb3f7-6c21-4c42-be1f-97a33fb5cf66,96c1d424-057e-4ff7-860b-6b9c9222bdbf,98a601e5-ca91-4440-b1c5-753f601a2c90,631d8095-c443-4e21-b301-4af1a0929c27"
	API_URL_PC = "https://game-status-api.ubisoft.com/v1/instances?appIds=e3d5ea9e-50bd-43b7-88bf-39794f4e3d40"

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
	def get_server_status(cls):
		logger.info("サーバーステータスを取得")
		# サーバーステータスを取得する
		res = request.urlopen(request.Request(cls.API_URL))
		res_pc = request.urlopen(request.Request(cls.API_URL_PC))

		# ステータスコードが200ではない場合は不明というステータスを返す
		if res.status != 200 or res_pc.status != 200:
			logger.error("サーバーステータスの取得に失敗 - ステータスコード: %s / %s", {res.status}, {res_pc.status})
			status = cls.DEFAULT_PLATFORM_STATUS.copy()
			return status

		raw_status = json.loads(res_pc.read())
		raw_status.extend(json.loads(res.read()))
		logger.info("取得完了")
		logger.info(str(raw_status))

		# 各プラットフォームのステータスをループ、ステータス辞書に加える
		status = {}
		for s in raw_status:
			p = s["Platform"]
			status[p] = cls.DEFAULT_PLATFORM_STATUS.copy()

			if s["Status"] == "Online":
				status[p]["Status"]["Connectivity"] = "Operational"
				for fk in status[p]["Status"]["Features"].keys():
					status[p]["Status"]["Features"][fk] = "Operational"

			# ImpactedFeatures をループする リストに含まれる場合は停止中なので、該当するステータスをOutageにする
			for f in s["ImpactedFeatures"]:
				status[p]["Status"]["Features"][f] = "Outage"

			# Maintenance が null の場合はステータスの Maintenance に False をセットする
			if s["Maintenance"] is None:
				status[p]["Status"]["Maintenance"] = False
			else:
				status[p]["Status"]["Maintenance"] = s["Maintenance"]

			status[p]["UpdatedAt"] = datetime.datetime.now().timestamp()

		logger.info("サーバーステータスの整形完了")
		logger.info(str(status))

		return status

	@classmethod
	def update_status(cls):
		cls.data = cls.get_server_status()


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

	ServerStatusManager.update_status()
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
