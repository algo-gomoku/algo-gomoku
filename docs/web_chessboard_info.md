## 棋盘标识

系统可支持同时执行多场比赛。

web调用主程序时，传入一个id作为本盘的标识。

主程序查看标识的棋局是否已结束。如果已结束，清理棋盘，并生成一个新的棋盘。

## 数据交互

为了让web端能获取到棋盘的数据，需要将棋盘信息按指定格式保存。

```json
{
    "players": [
        {
            "name": "pysnow530",
            "piece_char": "●",
            "used_time": 3.2
        },
        {
            "name": "jinguoliang",
            "piece_char": "○",
            "used_time": 3.0
        }
    ],
    "chessboard": [
        [" ", "○", " ", ...],
        ...
    ],
    "next": {
        "piece_char": "●",
        "position": {
            "x": 3,
            "y": 3
        }
    },
    "result": "ongoing"     // "player1 win", "player2 win", "draw"
}
```

此信息保存在data/ID.json中。
