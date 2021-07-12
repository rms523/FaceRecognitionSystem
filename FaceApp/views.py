from django.shortcuts import render
from deepface import DeepFace

# Create your views here.

def processImage(request):
    result = DeepFace.verify("C:\\Users\\machina\\Pictures\\Camera Roll\\Rahul1.jpg", "C:\\Users\\machina\\Pictures\\Camera Roll\\Rahul2.jpg")
    print (result['verified'])
    return render(request, 'Dashboard/index.html', result)

def webStream(request):
    DeepFace.stream(db_path = "C:\\Users\\machina\\Desktop\\Project\\FaceRecognitionSystem\\Dashboard\\static\\images") #, model_name="VGG-Face")
    return render(request, 'Dashboard/index.html')

