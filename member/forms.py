from django.contrib.auth.hashers import check_password

from django import forms
from .models import BoardMember

class LoginForm(forms.Form):
    # 입력받을 값 두개
    username = forms.CharField(error_messages={
        'required':'아이디를 입력하세요!'
    },max_length=100, label="Member name")
    password = forms.CharField(error_messages={
        'required':'비밀번호를 입력하세요!'
    },widget=forms.PasswordInput, max_length=100, label="Password")
    # 처음 값이 들어왔다 는 검증 진행
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                member = BoardMember.objects.get(username=username)
            except BoardMember.DoesNotExist:
                self.add_error('username', '아이디가 없습니다!')
                return

            if not check_password(password, member.password):
                self.add_error('password', '비밀번호가 다릅니다!')
            else:
                self.user_id = member.id


