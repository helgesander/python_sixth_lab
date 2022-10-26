
from django.shortcuts import render
from .models import Article
from django.http import Http404
from django.shortcuts import redirect
from .forms import UserRegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404



def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def create_error(request):
    return render(request, 'error.html')

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
        # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
        # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                if Article.objects.filter(title=form['title']).exists():
                    return redirect('error_create_article')
        # если поля заполнены без ошибок
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('archive')
            # перейти на страницу поста
            else:
        # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})

    else:
        raise Http404

# Create your views here.

def error_registration(request):
    return render(request, 'error_registration.html')
'''
def registration(request):
    if not request.user.is_anonymous:
        #return render(request, 'registration.html')
        if request.method == "POST":
            form = {
                'login': request.POST['login'],
                'email': request.POST['email'],
                'password': request.POST['password']
            }
            if form['login'] and form['email'] and form['password']:
                try:
                    User.objects.get(username=form['login'])
                    return redirect('error_registration')
                except User.DoesNotExist:
                    User.objects.create_user(form['login'], form['email'], form['password'])
                    return render(request, 'registration.html', {'form': form})

        else:
            raise Http404

def login(request):
    return render(request, 'login.html', {})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'
    
'''

def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid:
            if User.objects.get(username=form.username):
                True
                #djsjdsd
            else:
                User.objects.create_user(form.username, form.email, form.password)
                return render(request, 'registration.html', {'form': form})





