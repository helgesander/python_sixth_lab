
from django.shortcuts import render
from .models import Article
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login



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

def login(request):
    if request.method == "POST":
        form = {
            'username': request.POST['username'], 'password': request.POST['password'],
        }
        if form['username'] and form['password']:
            if not User.objects.filter(username=form['username']):
                form['does_not_exist'] = u'Такого пользователя не существует'
            else:
                user = authenticate(username=form['username'], password=form['password'])
                if user is not None:
                    login(request, user)
                else:
                    form['bad_login'] = u'Аутентификация не прошла успешно, попробуйте позднее'
        else:
            form['error'] = u'Не все поля заполнены'
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {})

def logout(request):
    pass

def registration(request):
    if request.method == "POST":
        form =  {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        if form['username'] and form['email'] and form['password']:
            User.objects.create_user(form['username'], form['email'], form['password'])
            return redirect('archive')
        else:
            form['error'] = u'Не все поля заполнены!'
        return render(request, 'registration.html', {'form': form})
    else:
        return render(request, 'archive.html', {})







