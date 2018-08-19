from abc import ABCMeta, abstractmethod

class AbstractFacialRecognitionConnector(metaclass = ABCMeta):

    emotionDict = {'anger': 'None',
                'confusion': 'None',
                'contempt': 'None',
                'disgust': 'None',
                'fear': 'None',
                'happiness': 'None',
                'neutral': 'None',
                'sadness': 'None',
                'surprise': 'None'}

    @abstractmethod
    def __init__(self):
        print(self.__class__.__name__+"was initialized.")

    @abstractmethod
    def getName(self):
        return

    @abstractmethod
    def compareFace(self, srcImage, targetImage):
        return

    @abstractmethod
    def detectAge(self, image):
        return

    @abstractmethod
    def detectGender(self, image):
        return

    @abstractmethod
    def detectEmotion(self, image):
        return