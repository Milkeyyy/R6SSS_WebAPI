# R6SSS Web API
![R6SSS API](https://cronitor.io/badges/MAB0MW/production/nU_tW7xGKHIHVxRrspK61JDTEP0.svg)

⛓️ URL: https://api-r6sss.milkeyyy.com/v2

🪅 Discord Bot: https://github.com/Milkeyyy/R6SSS_Discord

### エンドポイント
- `/status` - `GET`
  #### クエリーパラメーター
  - `platform`
    - `PC`
    - `PS4`
    - `PS5`
    - `XBOXONE`
    - `XBOX SERIES X`

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
          }
        },
        "Maintenance": false,
        "UpdatedAt": 1728921810.32845
      },
      "PS4": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          }
        },
        "Maintenance": false,
        "UpdatedAt": 1728921810.32848
      },
      "PS5": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          }
        },
        "Maintenance": false,
        "UpdatedAt": 1728921810.32849
      },
      "XBOXONE": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          }
        },
        "Maintenance": false,
        "UpdatedAt": 1728921810.32849
      },
      "XBOX SERIES X": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          }
        },
        "Maintenance": false,
        "UpdatedAt": 1728921810.32849
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
          }
        },
        "Maintenance": false,
        "UpdatedAt": 1728921810.32848
      },
      "PS5": {
        "Status": {
          "Connectivity": "Operational",
          "Features": {
            "Authentication": "Operational",
            "Leaderboard": "Operational",
            "Matchmaking": "Operational",
            "Purchase": "Operational"
          }
        },
        "Maintenance": false,
        "UpdatedAt": 1728921810.32849
      }
    }
  }
  ```
