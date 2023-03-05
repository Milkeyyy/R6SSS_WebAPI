# R6SSS Web API
![R6SSS API](https://cronitor.io/badges/MAB0MW/production/nU_tW7xGKHIHVxRrspK61JDTEP0.svg)

URL: https://api.r6sss.milkeyyy.com

- [**🪅 Discord Bot**](https://github.com/Milkeyyy/R6SServerStatusBot)
- [**📃 ドキュメント** (適当)](https://api.r6sss.milkeyyy.com/docs)

### 例
- `GET` - `https://api.r6sss.milkeyyy.com`
```json
{"PC":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false},"Stadia":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false},"PS4":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false},"PS5":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false},"XBOXONE":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false},"XBOX SERIES X":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false}}
```

- `GET` - `https://api.r6sss.milkeyyy.com?platform=PS4&platform=PS5`
```json
{"PS4":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false},"PS5":{"Status":{"Connectivity":"Operational","Authentication":"Operational","Leaderboard":"Operational","Matchmaking":"Operational","Purchase":"Operational"},"Maintenance":false}}
```

#### パラメーターに指定できるプラットフォーム
プラットフォームを指定しない場合は、すべてのプラットフォームのサーバーステータスを取得できます。
- 正常に更新されるプラットフォーム
  - `PC` (Stadia の情報も含む)
  - `PS4` (PS5 の情報も含む)
  - `XBOXONE` (Xbox Series X/S の情報も含む)
- 以下のプラットフォームは、サーバーが停止していたり、メンテナンスが行われている場合でも、Ubisoftのサーバーから取得できる情報が更新されないため、ステータスが正常に更新されません。 
  - `Stadia`
  - `PS5`
  - `XBOX SERIES X`
