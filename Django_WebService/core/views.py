import os
import numpy as np
from gtts import gTTS

import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
# https://im-nanna.tistory.com/27 //MultiValueDictKeyError에 대한 설명
# https://windybay.net/post/39/

from django.core.files.storage import FileSystemStorage

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def index(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        # image details
        image_url = fss.url(_image)
        
        # Read the image

        imag = load_img(path,target_size = (75,75))
        imag = img_to_array(imag)
        img = imag.reshape(1,75,75,3)
        img = img.astype('float32')
        test_image = img/255.0

        # load model
        model = tf.keras.models.load_model(os.getcwd() + '/3rd_cnn_1.h5')

        result = model.predict(test_image)

        # ----------------
        # LABELS
        # Banana 0
        # Chip 1
        # Heim 2
        # Onion 3
        # Oreo 4
        # Pepero 5
        # Pie 6
        # Pizza 7
        # Shrimp 8
        # Turtle 9
        # ----------------
        print("Prediction: " + str(np.argmax(result)))
            

        if (np.argmax(result) == 0):
            prediction = "바나나킥"
            info = "바나나맛이 나는 부드럽고 단 과자입니다."
        elif (np.argmax(result) == 1):
            prediction = "포카칩"
            info = "감자맛이 나는 짭조름한 생감자칩입니다."
        elif (np.argmax(result) == 2):
            prediction = "화이트하임"
            info = "화이트 초콜릿이 들어가 있는 과자입니다."
        elif (np.argmax(result) == 3):
            prediction = "양파링"
            info = "몸에 좋은 양파를 사용하여 링 모양으로 만든 과자입니다."
        elif (np.argmax(result) == 4):
            prediction = "오레오"
            info = "초코쿠키에 달콤한 크림을 함께 먹는 맛으로, 아주 단 과자입니다."
        elif (np.argmax(result) == 5):
            prediction = "아몬드빼빼로"
            info = "아몬드와 초콜릿을 같이 맛볼 수 있는 롯데의 대표과자입니다."
        elif (np.argmax(result) == 6):
            prediction = "후렌치파이"
            info = "딸기맛이 나는 파이 모양의 과자입니다."
        elif (np.argmax(result) == 7):
            prediction = "벌집핏자"
            info = "피자를 연상시키는 모양을 가진 과자입니다."
        elif (np.argmax(result) == 8):
            prediction = "새우깡"
            info = "실제 새우를 이용하여 만든 짭조름한 과자로, 대한민국 대표 과자 중 하나입니다."
        elif (np.argmax(result) == 9):
            prediction = "꼬북칩"
            info = "모양이 거북이 등껍질처럼 생긴 과자입니다."
        else:
            prediction = "인식에 실패하였습니다"

        
          
        snack_name="snack_name.mp3"
        #file_name = './assets/snack_name.mp3'
        name_tts = gTTS(text=prediction, lang="ko") # prediction에 해당하는 str값을 가져와서 음성으로 변환
        # if os.path.exists(file_name):
        #     os.remove(file_name)
        name_tts.save("./assets/"+snack_name)

        snack_info="snack_info.mp3"
        #file_info = './assets/snack_info.mp3'
        info_tts = gTTS(text=info, lang="ko") # info에 해당하는 str값을 가져와서 음성으로 변환
        # if os.path.exists(file_info):
        #     os.remove(file_info)
        info_tts.save("./assets/"+snack_info)

        
        
        return TemplateResponse(
            request,
            "index.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
                "info": info
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "index.html",
            {"message": "No Image Selected"},
        )
