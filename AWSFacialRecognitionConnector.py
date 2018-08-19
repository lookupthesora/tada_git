import shutil
import requests
from AbstractFacialRecognitionConnector import AbstractFacialRecognitionConnector
import botocore.vendored.requests.packages.urllib3 as urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# boto3をインポートする前に上記インポートしておかないとwarnが消えない
import boto3
from configparser import ConfigParser

class AWSFacialRecognitionConnector(AbstractFacialRecognitionConnector):
    config = ConfigParser()
    config.read('AWS.ini')
    CONNECTOR_NAME = config.get('common', 'CONNECTOR_NAME')
    BUCKET_NAME = config.get('s3', 'BUCKET_NAME')
    rekognition = ''

    def __init__(self):
        # AWS API初期化
        self.rekognition = boto3.client('rekognition', 'ap-northeast-1', verify=False)
        self.awsBucketName = AWSFacialRecognitionConnector.BUCKET_NAME

    def getName(self):
        return AWSFacialRecognitionConnector.CONNECTOR_NAME

    def compareFace(self, srcImage, targetImage):
        # AWSはまずS3のバケットに全画像を上げないといけない
        # まずは画像ファイルの取得とs3 upload
        self.imageUploader(srcImage)
        self.imageUploader(targetImage)
        # ようやくAPIが叩ける
        try:
            awsVerified = self.rekognition.compare_faces(
                SourceImage={'S3Object': {'Bucket': self.awsBucketName, 'Name': srcImage.split('/')[-1], }},
                TargetImage={'S3Object': {'Bucket': self.awsBucketName, 'Name': targetImage.split('/')[-1], }},
                SimilarityThreshold=0
            )
            return awsVerified['FaceMatches'][0].get('Similarity')
        except:
            return "not detected"

    def detectAge(self, image):
        # AWSはまずS3のバケットに全画像を上げないといけない
        # まずは画像ファイルの取得とs3 upload
        self.imageUploader(image)
        # 顔検知
        try:
            faceDetails = self.getFaceDetails(image.split('/')[-1])
            ageRange = str(faceDetails.get('AgeRange').get('Low')) + '~' + \
                       str(faceDetails.get('AgeRange').get('High'))
            return ageRange
        except:
            return 'not detected'

    def detectGender(self, image):
        # AWSはまずS3のバケットに全画像を上げないといけない
        # まずは画像ファイルの取得とs3 upload
        self.imageUploader(image)
        # 顔検知
        try:
            faceDetails = self.getFaceDetails(image.split('/')[-1])
            gender = str(faceDetails.get('Gender').get('Value')) + ' (' + \
                       str(faceDetails.get('Gender').get('Confidence'))+')'
            return gender
        except:
            return 'not detected'

    def detectEmotion(self, image):
        self.emotionDict = super().emotionDict
        # AWSはまずS3のバケットに全画像を上げないといけない
        # まずは画像ファイルの取得とs3 upload
        self.imageUploader(image)
        # 顔検知
        try:
            faceDetails = self.getFaceDetails(image.split('/')[-1])
            awsEmotionsList = faceDetails.get('Emotions')
            # AWSのemotion値は各項目ごとに独立なconfidence値であるため、値の和で正規化し、割合とする
            sumOfConfidenceValues = 0
            for awsEmotion in awsEmotionsList:
                sumOfConfidenceValues += awsEmotion.get('Confidence')
            for awsEmotion in awsEmotionsList:
                if (awsEmotion.get('Type') == 'HAPPY'):
                    self.emotionDict['happiness'] = round(100*awsEmotion.get('Confidence')/sumOfConfidenceValues, 2)
                elif (awsEmotion.get('Type') == 'SAD'):
                    self.emotionDict['sadness'] = round(100*awsEmotion.get('Confidence')/sumOfConfidenceValues, 2)
                elif (awsEmotion.get('Type') == 'ANGRY'):
                    self.emotionDict['anger'] = round(100*awsEmotion.get('Confidence')/sumOfConfidenceValues, 2)
                elif (awsEmotion.get('Type') == 'CONFUSED'):
                    self.emotionDict['confusion'] = round(100*awsEmotion.get('Confidence')/sumOfConfidenceValues, 2)
                elif (awsEmotion.get('Type') == 'DISGUSTED'):
                    self.emotionDict['disgust'] = round(100*awsEmotion.get('Confidence')/sumOfConfidenceValues, 2)
                elif (awsEmotion.get('Type') == 'SURPRISED'):
                    self.emotionDict['surprise'] = round(100*awsEmotion.get('Confidence')/sumOfConfidenceValues, 2)
            return self.emotionDict
        except:
            return self.emotionDict

    # 画像をs3にアップロードするprivateメソッド
    def imageUploader(self, image):
        try:
            headers = {"Accept": "application/octet-stream"}
            res1 = requests.get(image, headers=headers, stream=True, verify=False)
            if res1.status_code == 200:
                with open(image.split('/')[-1], 'wb') as file:
                    res1.raw.decode_content = True
                    shutil.copyfileobj(res1.raw, file)
            # 続いて取ってきたファイルをS3にupload
            s3 = boto3.resource('s3', verify=False)
            s3.Bucket(self.awsBucketName).upload_file(image.split('/')[-1], image.split('/')[-1])
        except:
            raise Exception

    # 顔検知を行うprivateメソッド
    def getFaceDetails(self, imageName):
        try:
            awsDetection = self.rekognition.detect_faces(
                Image={'S3Object': {'Bucket': self.awsBucketName, 'Name': imageName, }},
                Attributes=['ALL',]
            )
            return awsDetection['FaceDetails'][0]
        except:
            raise Exception