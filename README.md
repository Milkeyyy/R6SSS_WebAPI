# R6SSS Web API
![R6SSS API](https://cronitor.io/badges/MAB0MW/production/nU_tW7xGKHIHVxRrspK61JDTEP0.svg)

⛓️ URL: https://api-r6sss.milkeyyy.com/v2

🪅 Discord Bot: https://github.com/Milkeyyy/R6SSS_Discord

### エンドポイント
- [`/status`](https://api-r6sss.milkeyyy.com/v2/status) - `GET`
  #### クエリーパラメーター
  - `platform`
    - `PC`
    - `PS4`
    - `PS5`
    - `XB1`
    - `XBSX`

### 例
- `GET` - `https://api-r6sss.milkeyyy.com/v2/status`
  ```json
  {
    "info": {
      "name": "R6SSS Web API",
      "version": "2.0.0-0",
      "author": "Milkeyyy"
    },
    "detail": "OK",
    "data": {
      "PC": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          },
          "Maintenance": false
        },
        "UpdatedAt": 1730275264.15424
      },
      "PS4": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          },
          "Maintenance": false
        },
        "UpdatedAt": 1730275264.15424
      },
      "PS5": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          },
          "Maintenance": false
        },
        "UpdatedAt": 1730275264.15424
      },
      "XB1": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          },
          "Maintenance": false
        },
        "UpdatedAt": 1730275264.15425
      },
      "XBSX": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          },
          "Maintenance": false
        },
        "UpdatedAt": 1730275264.15425
      }
    }
  }
  ```

- `GET` - `https://api-r6sss.milkeyyy.com/v2/status?platform=PS4&platform=PS5`
  ```json
  {
    "info": {
      "name": "R6SSS Web API",
      "version": "2.0.0-0",
      "author": "Milkeyyy"
    },
    "detail": "OK",
    "data": {
      "PS4": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          },
          "Maintenance": false
        },
        "UpdatedAt": 1730275323.54746
      },
      "PS5": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          },
          "Maintenance": false
        },
        "UpdatedAt": 1730275323.54747
      }
    }
  }
  ```
