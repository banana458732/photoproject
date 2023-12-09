from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView
from .forms import PhotoPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import PhotoPost
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage

def my_view(request):
    messages.info(request,"My message with an <a href='https://www.youtube.com/watch?v=NxA1hlST-yM'>hyperlink</a>")

class IndexView(ListView):

    template_name ='index.html'

    queryset = PhotoPost.objects.order_by('-posted_at')

@method_decorator(login_required, name='dispatch')

class CreatePhotoView(CreateView):

    form_class = PhotoPostForm

    template_name = "post_photo.html"

    success_url = reverse_lazy('photo:post_done')

    def form_valid(self,form):

        postdata = form.save(commit=False)

        postdata.user = self.request.user

        postdata.save()

        return super().form_valid(form)

class PostSuccessView(TemplateView):

    template_name= 'post_success.html'

    paginate_by = 9

class CategoryView(ListView):

    template_name = 'index.html'

    paginate_by = 9

    def get_queryset(self):

        category_id = self.kwargs['category']

        categories= PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')
        return categories
    
class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    def get_queryset(self):
        user_id =self.kwargs['user']
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list
    
class DetailView(DetailView):
    template_name = 'detail.html'
    model = PhotoPost

class MypageView(ListView):
    template_name = 'mypage.html'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset
    
class PhotoDeleteView(DeleteView):
    # 操作の対象はPhotoPostモデル
    model = PhotoPost
    # photo_delete.htmlをレンダリングする
    template_name = 'photo_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('photo:mypage')
    
    # レコードの削除を行う
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    # contact画面
class ContactView(FormView):
    template_name = 'contact.html'

    # forms.pyのclass名
    form_class = ContactForm

    # メールを送って問題なければ、このURLにリダイレクトされる。
    success_url = reverse_lazy('photo:contact')

    # フォームのバリエーションに問題がなかったら
    # （エラーがなかったら）実行されるメソッド
    def form_valid(self, form):

        # お問い合わせで入力された値を取得して代入している。
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        # ここでメールの内容を作成している
        subject = 'お問い合わせ: {}'.format(title)
        message = \
            '送信者名: {0}\nメールアドレス:{1}\n タイトル:{2}\n メッセージ:\n{3}' \
            .format(name, email, title, message)
        
        # 差出人
        from_email = 'ngn2349602@stu.o-hara.ac.jp'
        # 宛先
        # （配列になっているのは、宛先は複数人いる場合もあるから）
        to_list = ['ngn2349602@stu.o-hara.ac.jp']

        # messageという変数にメール内容をまとめている
        # （subject:件名、body:本文、from_email:メールを送信した人、to:宛先）
        message = EmailMessage(subject=subject,
                                body=message,
                                from_email=from_email,
                                to=to_list,
                                )
        
        # メールを送るメソッド
        message.send()
        # リダイレクトされたhtmlにデータが送られる
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        return super().form_valid(form)