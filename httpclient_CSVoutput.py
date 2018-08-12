import requests
import json
import datetime
import csv

# SSL warning disable
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# 最終的にCSVに書き出す用の辞書
dictForCsv = {}

# CSVのヘッダ用のlist
headerList = []

# 一定時間APIをたたき続けるループ
endTime = datetime.datetime.now() + datetime.timedelta(seconds=5)
while True:
    if datetime.datetime.now() >= endTime:
        break
    url='https://10.165.8.58:24229/alerts?limit=10'
    headers = {"content-type": "application/json"}
    res = requests.get(str(url), headers=headers, auth=('rootuser', 'rootuser'), verify=False)
    data = res.json()
    for line in data:
        if line['alertType'] == 'crowd-count':

            # timestampをキーにする
            key = line['timestamp']
            # CSVヘッダに追加
            headerList.append('timestamp')

            # sensorId
            value = str(line['sensorId'])
            # CSVヘッダに追加
            headerList.append('sensorId')

            # regionごとの混雑値
            for region in line['appSpecificAlert']['regions']:
                value += (", "+str(region['crowdInfo']['indexOfRange']))
                # CSVヘッダに追加
                headerList.append(region['name']+":indexOfRange")

            # frameId    
            value += (", "+str(line['appSpecificAlert']['frame_id']))
            # CSVヘッダに追加
            headerList.append('frameId')
                              
            # 辞書型なのでkeyが重複するエントリは無し。ループの中でvalueが毎回更新されるだけ
            dictForCsv.update({key:value})

# タイムアウト後に値を書き出し
# まずはファイルをオープン
f = open('output.csv', 'w')

# 1行目にヘッダ書き込み(Listに最初に登場した順でSet化)
writer = csv.writer(f, lineterminator='\n')
writer.writerow(sorted(set(headerList), key=headerList.index))

# timestamp順に並ぶようにkeyでソートしながら書き出し
for k,v in sorted(dictForCsv.items()):
    f.write(k+", "+v+"\n")

# ファイルクローズ
f.close()
