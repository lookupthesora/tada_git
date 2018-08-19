import time
from configparser import ConfigParser
import cognitive_face
from AbstractFacialRecognitionConnector import AbstractFacialRecognitionConnector
import cognitive_face as CF


class MSFacialRecognitionConnector(AbstractFacialRecognitionConnector):
    config = ConfigParser()
    config.read('MS.ini')
    CONNECTOR_NAME = config.get('common', 'CONNECTOR_NAME')
    MS_API_KEY = config.get('cognitive', 'API_KEY')
    MS_BASE_URL = config.get('cognitive', 'FACE_API_URL')
    MS_PERSON_GROUP_ID = config.get('cognitive', 'PERSON_GROUP_ID')
    MS_PERSON_ID = config.get('cognitive', 'PERSON_ID')

    def __init__(self):
        self.msApiKey = MSFacialRecognitionConnector.MS_API_KEY
        self.msBaseUrl = MSFacialRecognitionConnector.MS_BASE_URL
        self.msPersonGroupId = MSFacialRecognitionConnector.MS_PERSON_GROUP_ID
        self.msPersonId = MSFacialRecognitionConnector.MS_PERSON_ID
        CF.Key.set(self.msApiKey)
        CF.BaseUrl.set(self.msBaseUrl)

    def getName(self):
        return MSFacialRecognitionConnector.CONNECTOR_NAME

    def compareFace(self, srcImage, targetImage):
        # 仮実装。MSは事前にウォッチリストを登録することが前提であり、事前にsrcImageは登録済み。
        # やろうと思えばpersonIdを指定して引数のsrcImageを登録する事も可能だが、ひとまず後回し。
        # MS顔検出のリクエスト
        detect = self.getFaceDetails(targetImage)
        try:
            # MS顔認証のリクエスト
            if len(detect) > 0 and 'faceId' in detect[0]:
                msVerified = CF.face.verify(detect[0]['faceId'],
                                            person_group_id=self.msPersonGroupId,
                                            person_id=self.msPersonId)
                return msVerified.get('confidence') * 100
            else:
                return 'not detected'
        except cognitive_face.util.CognitiveFaceException:
            # コール回数制限(20回/分)にかかったと見てスリープ後に再トライ
            time.sleep(60)
            try:
                # MS顔認証のリクエスト
                if len(detect) > 0 and 'faceId' in detect[0]:
                    msVerified = CF.face.verify(detect[0]['faceId'],
                                                person_group_id=MSFacialRecognitionConnector.MS_PERSON_GROUP_ID,
                                                person_id=MSFacialRecognitionConnector.MS_PERSON_ID)
                    return msVerified.get('confidence') * 100
                else:
                    return 'not detected'
            # それでもダメなら異常終了
            except:
                return 'not detected'
        except:
            return 'not detected'

    def detectAge(self, image):
        requestAttributes = 'age'
        try:
            faceDetails = self.getFaceDetails(image, requestAttributes)
            return faceDetails.get('faceAttributes').get(requestAttributes)
        except:
            return 'not detected'

    def detectGender(self, image):
        requestAttributes = 'gender'
        try:
            faceDetails = self.getFaceDetails(image, requestAttributes)
            return faceDetails.get('faceAttributes').get(requestAttributes)
        except:
            return 'not detected'

    def detectEmotion(self, image):
        self.emotionDict = super().emotionDict
        requestAttributes ='emotion'
        try:
            faceDetails = self.getFaceDetails(image, requestAttributes)
            msEmotionDict = faceDetails.get('faceAttributes').get(requestAttributes)
            # MSのAPIで得た値を戻り値用のemotionDictの値に反映。MSの値を手本にしているため、keyは同一
            for key in self.emotionDict:
                if (type(msEmotionDict.get(key)) is float):
                 self.emotionDict[key] = round(100*msEmotionDict.get(key), 2)
            return self.emotionDict
        except:
            return self.emotionDict

    # 顔検知を行うprivateメソッド
    def getFaceDetails(self, image, requestAttributes):
        try:
            # MS顔検出のリクエスト
            detect = CF.face.detect(image, face_id=True, landmarks=False, attributes=requestAttributes)
            return detect[0]
        except cognitive_face.util.CognitiveFaceException:
            # コール回数制限(20回/分)にかかったと見てスリープ後に再トライ
            time.sleep(60)
            try:
                # MS顔検出のリクエスト
                detect = CF.face.detect(image, face_id=True, landmarks=False, attributes=requestAttributes)
                return detect[0]
            # それでもダメなら異常終了
            except:
                raise Exception
        except:
            raise Exception