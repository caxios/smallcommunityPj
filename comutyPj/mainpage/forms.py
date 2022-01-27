from django.forms import ModelForm
from mainpage.models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'