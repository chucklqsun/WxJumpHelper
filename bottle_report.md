# wxagame_bottlereport
## 最后更新时间(last update)
```
01/08/2018
```
## 数据格式(Data Format)
```
{
    "base_req": {
        "session_id": "xxxxxx",     //your session
        "fast": 1,
        "client_info": {
        "platform": "android",
            "brand": "Xiaomi",
            "model": "MI 5s",
            "system": "Android 7.0"
    },
    "report_list": []       //reportList.push
}
```


## 流水线(Pipeline)
Type: 0->10->2->1

# 明细(Details)
## enterReport
### 示例(Example)
```
{
    "ts": 1234567890,       //时间戳(timestamp)
    "type": 0,
    "scene": 1089
}
```

## quitReport
### 示例(Example)
```
{
    "ts": 1234567890,       //时间戳(timestamp)
	"type": 1,
	"duration": 65      //time gap between type0 ts and current ts
}
```


## playGameReport
### 示例(Example)
```
{
    "ts": 1234567890,       //时间戳(timestamp)
    "type": 2,
    "score": 1,             //当前分数(current score)
    "best_score": 100000,   //历史最佳(history best)
    "break_record": 0,      // if score > best_score , = 1 else 0
    "duration": 10,         // time gap between last type10 ts and current ts
    "times": 67             // your Nth time play game
}
```

## playAudienceReportStart
### 示例(Example)
```
{
    "ts": 1234567890,       //时间戳(timestamp)
    "type": 10
}
```
