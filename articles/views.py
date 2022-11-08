
from django.shortcuts import render
from .models import Article
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout



def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def archive(request):
    if request.user.is_authenticated:
        link_list = [
            {"text": "Выход из аккаунта", "ref": "/logout"},
            {"text": "Создать статью", "ref": "article/new"}
        ]
    else:
        link_list = [
            {"text": "Вход", "ref": "/login"},
            {"text": "Регистрация", "ref": "/registration"}
        ]
    return render(request, 'archive.html', {"posts": Article.objects.all(), "links": link_list})

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

def login_user(request):
    if request.method == "POST":
        form = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        if form['username'] and form['password']:
            user = authenticate(username=form['username'], password=form['password'])
            if user is None:
                form['error'] = u'Такого пользователя не существует'
                return render(request, 'login.html', {'form': form})
            else:
                login(request, user)
                return redirect('archive')
        else:
            form['errors'] = u'Не все поля заполнены'
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('archive')

def registration(request):
    if request.method == "POST":
        form = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        if form["username"] and form["email"] and form["password"]:
            try:
                User.objects.get(username=form['username'])
                User.objects.get(email=form['email'])
                form['errors'] = "Логин или почта уже заняты"
                return render(request, 'registration.html', {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(form['username'], form['email'], form['password'])
                login(request, authenticate(request, username=form['username'], password=form['password']))
                return redirect('archive')
        else:
            form['errors'] = u'Не все поля заполнены!'
        return render(request, 'registration.html', {'form': form})
    else:
        return render(request, 'registration.html', {})







