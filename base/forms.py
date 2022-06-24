from django.forms import ModelForm
from .models import Room     #class Room(models.Model): 요고를 models.py에서 불러옴

class RoomForm(ModelForm):  #클래스 생성 
    class Meta:
        model = Room
        fields = '__all__'
