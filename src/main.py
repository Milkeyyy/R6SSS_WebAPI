import datetime
import json
import logging
from typing import List
from urllib import request

from fastapi import Body, FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app import App


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
	# サーバーステータスを更新
	ServerStatusManager.update_status()

	yield

	logging.info("Bye.")

app = FastAPI(lifespan=lifespan, docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")


class ServerStatus:
	data: dict

	def __init__(self, data: dict) -> None:
		self.data = data

	@property
	def platform(self) -> str:
		if "Platform" in self.data:
			return self.data["Platform"]
		else:
			return None

	@property
	def status(self) -> str:
		if "Status" in self.data:
			return self.data["Status"]
		else:
			return None

class ServerStatusManager:
	# サーバーステータスAPIのURL
	API_URL_OTHER = "https://game-status-api.ubisoft.com/v1/instances?spaceIds=57e580a1-6383-4506-9509-10a390b7e2f1,05bfb3f7-6c21-4c42-be1f-97a33fb5cf66,96c1d424-057e-4ff7-860b-6b9c9222bdbf,98a601e5-ca91-4440-b1c5-753f601a2c90,631d8095-c443-4e21-b301-4af1a0929c27"
	API_URL_PC = "https://game-status-api.ubisoft.com/v1/instances?appIds=e3d5ea9e-50bd-43b7-88bf-39794f4e3d40"
	# サーバーステータス辞書
	data: dict = {}

	# サーバーステータスを取得して整えて返す
	def get_server_status():
		logging.info("サーバーステータスを取得")
		# サーバーステータスを取得する
		res = request.urlopen(request.Request(ServerStatusManager.API_URL_OTHER))
		#logging.info(str(res.read()))
		res_pc = request.urlopen(request.Request(ServerStatusManager.API_URL_PC))
		#logging.info(str(res_pc.read()))

		# ステータスコードが200ではない場合は不明というステータスを返す
		if res.status != 200 or res_pc.status != 200:
			logging.error(f"サーバーステータスの取得に失敗 - ステータスコード: %s / %s", {res.status}, {res_pc.status})
			status = {"Unknown": {"Status": {"Connectivity": "Unknown", "Authentication": "Unknown", "Leaderboard": "Unknown", "Matchmaking": "Unknown", "Purchase": "Unknown"}, "Maintenance": False}, "_Update_At": datetime.datetime.utcnow().timestamp()}
			return status

		raw_status = json.loads(res_pc.read())
		raw_status.extend(json.loads(res.read()))
		logging.info("取得完了")
		logging.info(str(raw_status))
		#logging.info(str(raw_status))

		# 各プラットフォームのステータスをループ、ステータス辞書に加える
		status = {}
		for s in raw_status:
			p = s["Platform"]
			status[p] = {"Status": {"Connectivity": None, "Authentication": "Operational", "Leaderboard": "Operational", "Matchmaking": "Operational", "Purchase": "Operational"}, "Maintenance": None}

			status[p]["Status"]["Connectivity"] = s["Status"]
			if status[p]["Status"]["Connectivity"] == "Online": status[p]["Status"]["Connectivity"] = "Operational"

			# ImpactedFeatures をループする リストに含まれる場合は停止中なので、該当するステータスをOutageにする
			for f in s["ImpactedFeatures"]:
				status[p]["Status"][f] = "Outage"

			# Maintenance が null の場合はステータスの Maintenance に False をセットする
			if s["Maintenance"] == None:
				status[p]["Maintenance"] = False
			else:
				status[p]["Maintenance"] = s["Maintenance"]

			status[p]["_Update_At"] = datetime.datetime.utcnow().timestamp()

		#logging.info(str(status))

		logging.info("サーバーステータスの整形完了")
		logging.info(str(status))
		return status

	def update_status():
		ServerStatusManager.data = ServerStatusManager.get_server_status()

app = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")

# サーバーステータスを更新
ServerStatusManager.update_status()

@app.post("/__space/v0/actions")
def update_serverstatus(body=Body(...)):
	event = body["event"]
	if event["id"] == "update":
		ServerStatusManager.update_status()
		logging.info("Server Status Updated: " + str(ServerStatusManager.data))

@app.get("/")
async def get_serverstatus(platform: List[str] = Query(default=None)):
	status = {}

	# パラメーターが指定されていない場合は全てのプラットフォームのステータスを返す
	if platform == None:
		status = ServerStatusManager.data
		if "_last_update" in status.keys(): del status["_last_update"]
	else:
		# 指定されたプラットフォームのステータスだけ返す
		#platforms = platforms.split(",")
		for p in platform:
			d = ServerStatusManager.data.get(p)
			if d != None:
				status[p] = d

	# JSONでサーバーステータスのデータを返す
	return JSONResponse(content=jsonable_encoder(status))