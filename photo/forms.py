from django import forms
from django.forms import ModelForm
from .models import PhotoPost

class PhotoPostForm(ModelForm):
    class Meta:
        model = PhotoPost
        fields = ['category','title','comment','image1','image2']

# views.pyのform_class名
class ContactForm(forms.Form):

    # フィールド(変数宣言)を定義している
    name = forms.CharField(label='お名前')
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='件名')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # placeholderは入力場所に記載されている薄いグレーの文字
        # 17行～19行の3行でhtmlには下記の内容が記載される。
        # <input type="text" name="name"
        #         placeholder="お名前を入力して下さい"
        #         class="form-control"
        #         required id="id_name">
        self.fields['name'].widget.attrs['placeholder']  = \
            'お名前を入力してください'
        self.fields['name'].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder']  = \
            'メールアドレスを入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control'

        self.fields['title'].widget.attrs['placeholder']  = \
            'タイトルを入力してください'
        self.fields['title'].widget.attrs['class'] = 'form-control'

        self.fields['message'].widget.attrs['placeholder']  = \
            'メッセージを入力してください'
        self.fields['message'].widget.attrs['class'] = 'form-control'
