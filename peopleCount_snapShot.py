import requests
import datetime
import csv
import shutil

# SSL warning disable
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

# 最終的にCSVに書き出す用の辞書
dictForCsv = {}

# CSVのヘッダ用のlist
headerList = []

# スナップショット習得条件とするcount値
thresholdCount = 2

# 一定時間APIをたたき続けるループ
timer = 300
endTime = datetime.datetime.now() + datetime.timedelta(seconds=timer)
while True:
    if datetime.datetime.now() >= endTime:
        break
    alertUrl = 'https://10.165.8.55:22281/alerts?limit=1'
    headers = {"content-type": "application/json"}
    res = requests.get(str(alertUrl), headers=headers, auth=('rootuser', 'rootuser'), verify=False)
    data = res.json()
    for line in data:
        if line['alertType'] == 'people-counting-out' or line['alertType'] == 'people-counting-in':

            # timestampをキーにする
            timestamp = line['timestamp']
            key = timestamp
            # CSVヘッダに追加
            headerList.append('timestamp')

            # sensorId
            sensorId = line['sensorId']
            value = str(sensorId)
            # CSVヘッダに追加
            headerList.append('sensorId')

            # count値
            count = line['appSpecificAlert']['count']
            value += (", " + str(count))
            # CSVヘッダに追加
            headerList.append("count")

            # frameId
            frame_id = line['appSpecificAlert']['frame_id']
            value += (", " + str(frame_id))
            # CSVヘッダに追加
            headerList.append('frameId')

            # 辞書型なのでkeyが重複するエントリは無し。ループの中でvalueが毎回更新されるだけ
            dictForCsv.update({key: value})

            # count値が閾値を超えていた場合はスナップショットを取得
            if count >= thresholdCount:
                snapShotUrl = 'https://10.165.8.55:3000/sensors/' + str(sensorId) + '/snapshot/raw'
                headers2 = {"Accept": "application/octet-stream"}
                res2 = requests.get(str(snapShotUrl), headers=headers2, auth=('rootuser', 'rootuser'),
                                    verify=False, stream=True)
                if res2.status_code == 200:
                    with open(str(frame_id)+".jpg", 'wb') as file:
                        res2.raw.decode_content = True
                        shutil.copyfileobj(res2.raw, file)

# タイムアウト後に値を書き出し
# まずはファイルをオープン
f = open('people_counting.csv', 'w')

# 1行目にヘッダ書き込み(Listに最初に登場した順でSet化)
writer = csv.writer(f, lineterminator='\n')
writer.writerow(sorted(set(headerList), key=headerList.index))

# timestamp順に並ぶようにkeyでソートしながら書き出し
for k, v in sorted(dictForCsv.items()):
    f.write(k + ", " + v + "\n")

# ファイルクローズ
f.close()
