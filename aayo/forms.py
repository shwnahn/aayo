# forms.py
from django import forms

class RoomCreationForm(forms.Form):
    name = forms.CharField(max_length=100, label="방 이름")
    user_id = forms.CharField(max_length=50, label="아이디(이름)")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="비밀번호")
    cafeimage = forms.ModelChoiceField(queryset=Cafe.objects.all(), label="카페", widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(RoomCreationForm, self).__init__(*args, **kwargs)
        self.fields['cafe'].empty_label = None
        self.fields['cafe'].widget.attrs.update({
            'class': 'cafe-selection'
        })

class EnterRoomForm(forms.Form):
    guest_name = forms.CharField(max_length=100, required=True)
    room_password = forms.CharField(required=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super(EnterRoomForm, self).__init__(*args, **kwargs)
        if not self.room or not self.room.password:
            del self.fields['room_password']

    def clean_room_password(self):
        password = self.cleaned_data.get('room_password')
        if self.room and self.room.password and password != self.room.password:
            raise forms.ValidationError("비밀번호가 올바르지 않습니다.")
        return password