# Library to download constellation data from hoshi-miru.com's API
# Web page: https://hoshi-miru.com/
# API doc: https://hoshimiru.docs.apiary.io
# API token: https://livlog.xyz/sso/login

import requests, json
from typing import Optional, Dict, Any

_URL = "https://livlog.xyz/hoshimiru/constellation"

# Returns constellation data as a list
#   lat, lon: Signed decimal lat and lon
#   date: "YYYY-MM-DD" format
#   hour, minute: Two-digit 24-hour format; e.g. "20" and "00" for 8pm
#
def getConstellationData(lat: int, lon: int,
                         date: str, hour: str, minute: str,
                         apiToken: str):
    headers= {"Accept" : "application/json",
              "Authorization" : "Bearer " + apiToken }
    params={
        "lat": lat,
        "lng": lon,
        "date": date,
        "hour": hour,
        "min": minute,
#         "id": id,  # 星座のID
        "disp": "off" # 水平線より下を表示するかどうか
    }
    # https://app.livlog.xyz/hoshimiru/constellation?lat=35.6581&
    #   lng=139.7414&date=2020-01-15&hour=20&min=00&id=1&disp=on
    response = requests.get(_URL, headers=headers, params=params)
    if response.status_code == 200:
        print("Data downloaded from hoshi-miru.com:",
              "lat=", lat, "lon=", lon,
              "datetime=", date, hour, minute)
        return response.json()["results"]
    else:
        print("API Response Error. Status code: " + str(response.status_code))
        return None

def trackConstellationLocations(constellationId: int,
                                lat: int, lon: int,
                                date: str, hour: str, minute: str,
                                apiToken: str):
    headers= {"Accept" : "application/json",
              "Authorization" : "Bearer " + apiToken }
    params={
        "lat": lat,
        "lng": lon,
        "date": date,
        "hour": hour,
        "min": minute,
        "id": constellationId,
        "disp": "on" # 水平線より下を表示するかどうか
    }
    # https://app.livlog.xyz/hoshimiru/constellation?lat=35.6581&
    #   lng=139.7414&date=2020-01-15&hour=20&min=00&id=1&disp=on
    response = requests.get(_URL, headers=headers, params=params)
    if response.status_code == 200:
#         print("Data downloaded from hoshi-miru.com:",
#               "Constellation ID=", constellationId,
#               "lat=", lat, "lon=", lon,
#               "datetime=", date, hour, minute)
        results = response.json()["results"]
        if results != None:
            return response.json()["results"]
        else:
            return None # No search hit
    else:
        print("API Response Error. Status code: " + str(response.status_code))
        return None

def bearingToDirectionName(bearingDecimalAngle: float):
    directionName = ["北","北北東","北東", "東北東",
                     "東", "東南東", "南東", "南南東",
                     "南", "南南西", "南西", "西南西",
                     "西", "西北西", "北西", "北北西",
                     "北"];
    directionIndex = round((bearingDecimalAngle)/22.5)
    return directionName[directionIndex]

def pitchToPitchName(pitchAngleDecimal: float):
    pitchName = ["水平線上","30度位","45度位", "60度位", "真上"]
    if pitchAngleDecimal >=0 and pitchAngleDecimal < 22.5:
        return pitchName[0]
    elif pitchAngleDecimal >=22.5 and pitchAngleDecimal < 37.5:
        return pitchName[1]
    elif pitchAngleDecimal >= 37.5 and pitchAngleDecimal < 52.5:
        return pitchName[2]
    elif pitchAngleDecimal >= 52.5 and pitchAngleDecimal < 67.5:
        return pitchName[3]
    elif pitchAngleDecimal >= 67.5 and pitchAngleDecimal <= 90:
        return pitchName[4]

def findConstellations(constellationsList,
                       bearingDecimal: float = None, pitchDecimal: float = None):
#     print(bearingToDirectionName(bearingAngleDecimal), pitchToPitchName(pitchAngleDecimal))
    foundConstellations = []
    for c in constellationsList:
        if c["direction"] == bearingToDirectionName(bearingDecimal) and \
           c["altitude"] == pitchToPitchName(pitchDecimal):
            foundConstellations.append(c)
    return foundConstellations

# print(pitchToPitchName(37.5))

# print(bearingToDirectionName(90))

# [{'altitude': '水平線の近く',
#   'altitudeNum': 21.59,
#   'confirmed': '0',
#   'content': '秋の代表的な星座。21時に正中する時期は、11月下旬。銀河系の隣の銀河・アンドロメダ大銀河があることで有名。設定者はプトレマイオス。',
#   'direction': '北西',
#   'directionNum': 310.52,
#   'drowing': '[8961|8976|8965|8762|8965|154|15|165|215|165|337|603|337|269|226|335|464]',
#   'eclipticalFlag': '0',
#   'enName': 'Andromeda',
#   'id': '1',
#   'jpName': 'アンドロメダ座',
#   'origin': 'エチオペアをケフェウス王とカシオペア王妃が支配していた時のこと、2人には絶世の美女アンドロメダ姫がいました。カシオペアはアンドロメダがあまりに美しいので、その事を自慢しすぎて海の妖精たちの嫉妬を買ってしまいます。海の妖精たちの話を聞いた海の神・ポセイドンは怒り、化け鯨ティアマトに人々を襲わせました。困ったケフェウス王は神にお伺いを立てると、アンドロメダをいけにえに捧げよ、と迫られます。王は、苦渋の決断の末、国民を守るためにアンドロメダを海岸の岩に鎖でつなぎました。やがて、化け鯨がやってきてアンドロメダに向かって突き進んできました。その瞬間、若者・ペルセウスが立ちはだかりました。彼は化け鯨を退治し、アンドロメダを開放したのです。（ペルセウス座も合わせてご覧ください）',
#   'ptolemyFlag': '1',
#   'roughly': '秋の代表的な星座。',
#   'ryaku': 'and',
#   'season': '秋',
#   'starIcon': 'https://rad-pegasus-bb29eb.netlify.app/www/hoshimiru/icon/and.png',
#   'starImage': 'https://rad-pegasus-bb29eb.netlify.app/www/hoshimiru/img/and.png'},
#  {...},
#  {...}]

# ID	星座
# 1	アンドロメダ
# 2	ポンプ
# 3	ふうちょう
# 4	わし
# 5	みずがめ
# 6	さいだん
# 7	おひつじ
# 8	ぎょしゃ
# 9	うしかい
# 10	ちょうこくぐ
# 11	きりん
# 12	やぎ
# 13	りゅうこつ
# 14	カシオペヤ
# 15	ケンタウルス
# 16	ケフェウス
# 17	くじら
# 18	カメレオン
# 19	コンパス
# 20	おおいぬ
# 21	こいぬ
# 22	かに
# 23	はと
# 24	かみのけ
# 25	みなみのかんむり
# 26	かんむり
# 27	コップ
# 28	みなみじゅうじ
# 29	からす
# 30	りょうけん
# 31	はくちょう
# 32	いるか
# 33	かじき
# 34	りゅう
# 35	こうま
# 36	エリダヌス
# 37	ろ
# 38	ふたご
# 39	つる
# 40	ヘルクレス
# 41	とけい
# 42	うみへび
# 43	みずへび
# 44	インディアン
# 45	とかげ
# 46	しし
# 47	うさぎ
# 48	てんびん
# 49	こじし
# 50	おおかみ
# 51	やまねこ
# 52	こと
# 53	テーブルさん
# 54	けんびきょう
# 55	いっかくじゅう
# 56	はえ
# 57	じょうぎ
# 58	はちぶんぎ
# 59	へびつかい
# 60	オリオン
# 61	くじゃく
# 62	ペガスス
# 63	ペルセウス
# 64	ほうおう
# 65	がか
# 66	みなみのうお
# 67	うお
# 68	とも
# 69	らしんばん
# 70	レチクル
# 71	ちょうこくしつ
# 72	さそり
# 73	たて
# 74	へび
# 75	ろくぶんぎ
# 76	や
# 77	いて
# 78	おうし
# 79	ぼうえんきょう
# 80	みなみのさんかく
# 81	さんかく
# 82	きょしちょう
# 83	おおぐま
# 84	こぐま
# 85	ほ
# 86	おとめ
# 87	とびうお
# 88	こぎつね
