from configparser import ConfigParser

import requests
from AbstractFacialRecognitionConnector import AbstractFacialRecognitionConnector
# SSL warning disable
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

class FacePlusFacialRecognitionConnector(AbstractFacialRecognitionConnector):
    # Face++向けの設定
    config = ConfigParser()
    config.read('Face++.ini')
    CONNECTOR_NAME = config.get('common', 'CONNECTOR_NAME')
    DETECT_URL = config.get('face++', 'DETECT_URL')
    COMPARE_URL = config.get('face++', 'COMPARE_URL')
    API_KEY = config.get('face++', 'API_KEY')
    SECRET_KEY = config.get('face++', 'SECRET_KEY')

    def __init__(self):
        self.compareUrl = FacePlusFacialRecognitionConnector.COMPARE_URL
        self.detectUrl = FacePlusFacialRecognitionConnector.DETECT_URL
        self.apiKey = FacePlusFacialRecognitionConnector.API_KEY
        self.secretKey = FacePlusFacialRecognitionConnector.SECRET_KEY

    def getName(self):
        return FacePlusFacialRecognitionConnector.CONNECTOR_NAME

    def compareFace(self, srcImage, targetImage):
        self.postData = {'api_key': self.apiKey, 'api_secret': self.secretKey, 'image_url1': srcImage, 'image_url2': targetImage}
        try:
            # post data to server
            facePlusVerified = requests.post(self.compareUrl, data=self.postData, verify=False)
            return(facePlusVerified.json().get('confidence'))
        except:
            raise Exception

    def detectAge(self, image):
        self.postData = {'api_key': self.apiKey, 'api_secret': self.secretKey, 'image_url': image, 'return_attributes': 'age'}
        try:
            # post data to server
            res = requests.post(self.detectUrl, data=self.postData, verify=False)
            return(res.json().get('faces')[0].get('attributes').get('age').get('value'))
        except:
            return 'not detected'

    def detectGender(self, image):
        self.postData = {'api_key': self.apiKey, 'api_secret': self.secretKey, 'image_url': image, 'return_attributes': 'gender'}
        try:
            # post data to server
            res = requests.post(self.detectUrl, data=self.postData, verify=False)
            return(res.json().get('faces')[0].get('attributes').get('gender').get('value'))
        except:
            return 'not detected'

    def detectEmotion(self, image):
        self.emotionDict = super().emotionDict
        self.postData = {'api_key': self.apiKey, 'api_secret': self.secretKey, 'image_url': image, 'return_attributes': 'emotion'}
        try:
            # post data to server
            res = requests.post(self.detectUrl, data=self.postData, verify=False)
            facePlusEmotionDict = res.json().get('faces')[0].get('attributes').get('emotion')
            # MSの値を手本にしているemotionDictとkeyは同一
            for key in self.emotionDict:
                if (type(facePlusEmotionDict.get(key)) is float):
                    self.emotionDict[key] = round(facePlusEmotionDict.get(key), 2)
            return self.emotionDict
        except:
            return self.emotionDict