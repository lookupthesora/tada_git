import csv
import AWSFacialRecognitionConnector
import FacePlusFacialRecognitionConnector
import MSFacialRecognitionConnector

# マッチング対象画像の設定
import OpenCVFacialRecognitionConnector

face_dict = {}
face_dict.update({'base': 'https://a185.bbbiz-nec.com/face_test/base.jpg'})
face_dict.update({'base_modify1': 'https://a185.bbbiz-nec.com/face_test/base_dash.jpg'})
face_dict.update({'base_modify2': 'https://a185.bbbiz-nec.com/face_test/base_dash2.jpg'})
face_dict.update({'base_halfsize': 'https://a185.bbbiz-nec.com/face_test/base_half.jpg'})
face_dict.update({'base_gray': 'https://a185.bbbiz-nec.com/face_test/base_gray.jpg'})
face_dict.update({'base_15': 'https://a185.bbbiz-nec.com/face_test/base_15.jpg'})
face_dict.update({'base_30': 'https://a185.bbbiz-nec.com/face_test/base_30.jpg'})
face_dict.update({'base_45': 'https://a185.bbbiz-nec.com/face_test/base_45.jpg'})
face_dict.update({'base_60': 'https://a185.bbbiz-nec.com/face_test/base_60.jpg'})
face_dict.update({'base_75': 'https://a185.bbbiz-nec.com/face_test/base_75.jpg'})
face_dict.update({'base_90': 'https://a185.bbbiz-nec.com/face_test/base_90.jpg'})
face_dict.update({'smile': 'https://www.pakutaso.com/shared/img/thumb/ME_biz20160902112315_TP_V.jpg'})
face_dict.update({'angry': 'https://www.pakutaso.com/shared/img/thumb/ME_biz20160902072715_TP_V.jpg'})
face_dict.update({'big_smile': 'https://www.pakutaso.com/shared/img/thumb/ME_biz20160902572415_TP_V.jpg'})
face_dict.update({'eye_closed': 'https://www.pakutaso.com/shared/img/thumb/OMG151018350I9A2425_TP_V4.jpg'})
face_dict.update({'sleep': 'https://www.pakutaso.com/shared/img/thumb/OMG151018420I9A2445_TP_V.jpg'})
face_dict.update({'eye_mask': 'https://www.pakutaso.com/shared/img/thumb/YUKA160421000I9A2697_TP_V.jpg'})
face_dict.update({'right_down': 'https://www.pakutaso.com/shared/img/thumb/skincareIMGL7772_TP_V.jpg'})
face_dict.update({'right_up': 'https://www.pakutaso.com/shared/img/thumb/smIMGL4147_TP_V.jpg'})
face_dict.update({'left_down': 'https://www.pakutaso.com/shared/img/thumb/tyuka170809-0011_TP_V.jpg'})
face_dict.update({'left_up': 'https://www.pakutaso.com/shared/img/thumb/pcarIMGL4679_TP_V.jpg'})
face_dict.update({'left': 'https://www.pakutaso.com/shared/img/thumb/pcarIMGL4611_TP_V.jpg'})
face_dict.update({'dark': 'https://www.pakutaso.com/shared/img/thumb/IPPAKU9116_TP_V.jpg'})
face_dict.update({'flash': 'https://www.pakutaso.com/shared/img/thumb/yuka16011220IMG_5652_TP_V.jpg'})
face_dict.update({'mountain': 'https://www.pakutaso.com/shared/img/thumb/helmet-4_TP_V.jpg'})
face_dict.update({'cap': 'https://www.pakutaso.com/shared/img/thumb/nissinIMGL0778_TP_V4.jpg'})
face_dict.update({'glasses': 'https://www.pakutaso.com/shared/img/thumb/150912025921_TP_V.jpg'})
face_dict.update({'phone': 'https://www.pakutaso.com/shared/img/thumb/ME_biz20160902450317_TP_V.jpg'})
face_dict.update({'drink': 'https://www.pakutaso.com/shared/img/thumb/YK0I9A6222_TP_V.jpg'})
face_dict.update({'long_hair': 'https://www.pakutaso.com/shared/img/thumb/yuka522052_TP_V.jpg'})
face_dict.update({'tilt': 'https://www.pakutaso.com/shared/img/thumb/YUKA863_osusume15202708_TP_V.jpg'})
face_dict.update({'brown': 'https://www.pakutaso.com/shared/img/thumb/PAK105215319_TP_V.jpg'})
face_dict.update({'blond': 'https://www.pakutaso.com/shared/img/thumb/MAKIhappa15133812_TP_V.jpg'})
face_dict.update({'different_1': 'https://www.pakutaso.com/shared/img/thumb/PASONA160306550I9A2233_TP_V.jpg'})
face_dict.update({'different_2': 'https://www.pakutaso.com/shared/img/thumb/freee151108188680_TP_V.jpg'})
face_dict.update({'different_3': 'https://www.pakutaso.com/shared/img/thumb/YUSEI_chissu_TP_V.jpg'})
face_dict.update({'different_4': 'https://www.pakutaso.com/shared/img/thumb/ADIMGL6712_TP_V.jpg'})
face_dict.update({'different_5': 'https://www.pakutaso.com/shared/img/thumb/aomidoriIMGL1536_TP_V.jpg'})
face_dict.update({'different_6': 'https://www.pakutaso.com/shared/img/thumb/CRI_IMG_6017_TP_V.jpg'})
face_dict.update({'different_7': 'https://www.pakutaso.com/shared/img/thumb/ASE_037_TP_V4.jpg'})
face_dict.update({'different_8': 'https://www.pakutaso.com/shared/img/thumb/CSS_ashiwokumuofficer1292_TP_V4.jpg'})
face_dict.update({'different_9': 'https://www.pakutaso.com/shared/img/thumb/MJ_chhukutumo15143035_TP_V4.jpg'})
face_dict.update({'different_10': 'https://www.pakutaso.com/shared/img/thumb/PAK86_hartworyoutenimotu1039_TP_V.jpg'})
face_dict.update({'different_11': 'https://www.pakutaso.com/shared/img/thumb/SAYA151005488094_TP_V.jpg'})
face_dict.update({'different_12': 'https://www.pakutaso.com/shared/img/thumb/OJS_noankuchimoto_TP_V4.jpg'})
face_dict.update({'different_similar': 'http://www.flamme.co.jp/common/profile/kasumi_arimura.jpg'})


# 処理対象コネクタクラスのリスト
listOfFacialRecognitionConnector = [FacePlusFacialRecognitionConnector.FacePlusFacialRecognitionConnector,
                                    MSFacialRecognitionConnector.MSFacialRecognitionConnector,
                                    AWSFacialRecognitionConnector.AWSFacialRecognitionConnector]

# ファイルオープン
f = open('gender_detect_comparison.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

# CSVのヘッダ2行(画像desc, URL)用のlist更新
headerList = ['image type']
urlList = ['image url']
for k, v in face_dict.items():
    headerList.append(k)
    urlList.append(v)
# CSVヘッダ書き込み
writer.writerow(headerList)
writer.writerow(urlList)

# CSVデータ更新
for connector in listOfFacialRecognitionConnector:
    try:
        ins = connector()
        # CSVデータ更新用リスト初期化・1列目設定
        dataList = [str(ins.getName())]
        print('<'+str(ins.getName())+'>')
        for k, v in face_dict.items():
            gender = str(ins.detectGender(v))
            dataList.append(gender)
            print(k+":"+gender)
        # CSV出力
        writer.writerow(dataList)
    except:
        import traceback
        traceback.print_exc()

# ファイルクローズ
f.close()
