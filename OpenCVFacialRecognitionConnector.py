import os
import shutil
import requests
from AbstractFacialRecognitionConnector import AbstractFacialRecognitionConnector
from configparser import ConfigParser
import cv2
from skimage.measure import compare_ssim


class OpenCVFacialRecognitionConnector(AbstractFacialRecognitionConnector):
    config = ConfigParser()
    config.read('OpenCV.ini')
    CONNECTOR_NAME = config.get('common', 'CONNECTOR_NAME')
    IMG_SIZE = (200, 200)
    FACE_IMG_STORE_DIR = config.get('face_detect', 'FACE_STORE_DIR')

    def __init__(self):
        if os.path.exists(OpenCVFacialRecognitionConnector.FACE_IMG_STORE_DIR) == False:
            os.mkdir(OpenCVFacialRecognitionConnector.FACE_IMG_STORE_DIR)

    def getName(self):
        return OpenCVFacialRecognitionConnector.CONNECTOR_NAME

    def compareFace(self, srcImage, targetImage):
        # まずは画像ファイルの取得とローカル保存
        try:
            headers = {"Accept": "application/octet-stream"}
            srcImageName = srcImage.split('/')[-1]
            targetImageName = targetImage.split('/')[-1]
            if srcImageName == targetImageName:
                targetImageName = "t-"+srcImageName
            res1 = requests.get(srcImage, headers=headers, stream=True, verify=False)
            if res1.status_code == 200:
                with open(srcImageName, 'wb') as file:
                    res1.raw.decode_content = True
                    shutil.copyfileobj(res1.raw, file)
            res2 = requests.get(targetImage, headers=headers, stream=True, verify=False)
            if res2.status_code == 200:
                with open(targetImageName, 'wb') as file:
                    res2.raw.decode_content = True
                    shutil.copyfileobj(res2.raw, file)

            srcCvImage = cv2.imread(srcImageName)
            targetCvImage = cv2.imread(targetImageName)
            # グレースケール変換
            srcCvImage_gray = cv2.cvtColor(srcCvImage, cv2.COLOR_BGR2GRAY)
            targetCvImage_gray = cv2.cvtColor(targetCvImage, cv2.COLOR_BGR2GRAY)
            # カスケード分類器の特徴量を取得する
            cascade_path = "haarcascade_frontalface_alt.xml"
            cascade = cv2.CascadeClassifier(cascade_path)
            # 物体認識（顔認識）の実行
            srcFaceRect = cascade.detectMultiScale(srcCvImage_gray, scaleFactor=1.10, minNeighbors=1, minSize=(100, 100))
            targetFaceRect = cascade.detectMultiScale(targetCvImage_gray, scaleFactor=1.10, minNeighbors=1, minSize=(100, 100))
            # 顔だけ切り出して保存
            i = 0;
            srcDstName = []
            for srcRect in srcFaceRect:
                x = srcRect[0]
                y = srcRect[1]
                width = srcRect[2]
                height = srcRect[3]
                srcDst = srcCvImage[y:y + height, x:x + width]
                srcDstName.append(OpenCVFacialRecognitionConnector.FACE_IMG_STORE_DIR+'\\'+srcImageName+str(i)+'.jpg')
                cv2.imwrite(srcDstName[i], srcDst)
                i += 1
            i = 0;
            targetDstName = []
            for targetRect in targetFaceRect:
                x = targetRect[0]
                y = targetRect[1]
                width = targetRect[2]
                height = targetRect[3]
                targetDst = targetCvImage[y:y + height, x:x + width]
                targetDstName.append(OpenCVFacialRecognitionConnector.FACE_IMG_STORE_DIR+'\\'+targetImageName+str(i)+'.jpg')
                cv2.imwrite(targetDstName[i], targetDst)
                i += 1
            # 切り出した顔を使って比較(とりあえず上記の各ループで最初に見つかった顔同士)
            srcFaceImage = cv2.imread(srcDstName[0])
            srcFaceImage = cv2.resize(srcFaceImage, OpenCVFacialRecognitionConnector.IMG_SIZE)
            targetFaceImage  = cv2.imread(targetDstName[0])
            targetFaceImage = cv2.resize(targetFaceImage, OpenCVFacialRecognitionConnector.IMG_SIZE)

            # <ヒストグラム比較>
            src_hist = cv2.calcHist([srcFaceImage], [0], None, [256], [0, 256])
            target_hist = cv2.calcHist([targetFaceImage], [0], None, [256], [0, 256])
            similarity = cv2.compareHist(src_hist, target_hist, 0)

            # <特徴点比較>
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
            detector = cv2.AKAZE_create()
            (src_kp, src_des) = detector.detectAndCompute(srcFaceImage, None)
            (target_kp, target_des) = detector.detectAndCompute(targetFaceImage, None)
            # BFMatcherで総当たりマッチングを行う
            matches = bf.match(src_des, target_des)
            # 特徴量の距離を出し、平均を取る
            dist = [m.distance for m in matches]
            meanDist = sum(dist) / len(dist)
            return str(similarity)+'\n('+str(meanDist)+')'

        except:
            return "not detected"
