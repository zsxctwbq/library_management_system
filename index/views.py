from django.shortcuts import render, HttpResponse, redirect
from requests import get
from bs4 import BeautifulSoup
from .models import Publisher, Book, Author, User
from random import randint
# 用户登录校验
from django.contrib.auth.decorators import login_required
from django.contrib import auth

# user-agent池子
user_agent_list = [
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
    'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
]
headers = {"User-Agent": user_agent_list[randint(0, len(user_agent_list) - 1)]}


# 首页
@login_required
def index(request):
    all_book = Book.objects.all().order_by('id')
    return render(request, 'index/index.html', {
        'all_book': all_book,
    })


# 用户登录
def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        upwd = request.POST.get('upwd')
        user = auth.authenticate(username=uname, password=upwd)
        if user:
            # 验证通过,将用户封装到session
            auth.login(request, user)
            return redirect(index)
    return render(request, 'index/login.html')


# 用户注册
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        upwd = request.POST.get('upwd')
        upwd1 = request.POST.get('upwd1')
        # 如果密码不为空且确认
        if upwd and uname and upwd == upwd1:
            User.objects.create_user(username=uname, password=upwd)
            return redirect(login)
    return render(request, 'index/register.html')


# 用户注销
def logout(request):
    auth.logout(request)
    return redirect(login)


# 删除图书
def deleteBook(request):
    # 根据id删除图书后跳转到首页
    try:
        id = request.GET.get('id', '')
        Book.objects.get(id=id).delete()
    except Exception as e:
        print(e)
    return redirect(index)


# 增加图书
def addBook(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        try:
            p = Publisher.objects.get(id=publisher)
            b = Book.objects.create(title=name, publisher=p)
            # 判断作者是否存在
            if not Author.objects.filter(name=author):
                Author.objects.create(name=author)
        except Exception as e:
            print(e)
        return redirect(index)
    publisher_list = Publisher.objects.all().order_by('id')
    return render(request, 'index/addBook.html', {
        'publisher_list': publisher_list
    })


# 编辑图书
def editBook(request):
    if request.method == 'POST':
        # 接受书名和出版社,进行更新
        id = request.POST.get('id', '')
        book_title = request.POST.get('book_title', '')
        publisher = request.POST.get('publisher', '')
        pub_obj = None
        try:
            # publisher = int(publisher)
            pub_obj = Publisher.objects.get(id=publisher)
        except Exception as e:
            print(e)
        try:
            book = Book.objects.get(id=id)
            book.title = book_title
            book.publisher = pub_obj
            book.save()
            return redirect(index)
        except Exception as e:
            print(e)
    edit_id = request.GET.get('id', '')
    edit_book_obj = Book.objects.get(id=edit_id)
    publisher_list = Publisher.objects.all().order_by('id')
    return render(request, 'index/editBook.html', {
        'publisher_list': publisher_list,
        'book_obj': edit_book_obj,
    })


# 出版社列表
def publisher_list(request):
    publisher_list = Publisher.objects.all().order_by('id')
    return render(request, 'index/publishers.html', {
        'publisher_list': publisher_list,
    })


# 添加出版社
def addPublisher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        addr = request.POST.get('addr')
        if not Publisher.objects.filter(name=name, addr=addr):
            Publisher.objects.create(name=name, addr=addr)
        return redirect(publisher_list)
    return render(request, 'index/addPublisher.html')


# 删除出版社
def deletePublisher(request):
    id = request.GET.get('id')
    try:
        Publisher.objects.get(id=id).delete()
    except Exception as e:
        print(e)
    return redirect(publisher_list)


# 编辑出版社
def editPublisher(request):
    # 处理表单数据
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        addr = request.POST.get('addr')
        try:
            p = Publisher.objects.get(id=id)
            p.name = name
            p.addr = addr
            p.save()
            return redirect(publisher_list)
        except Exception as e:
            print(e)

    # 得到要编辑的出版社id
    id = request.GET.get('id')
    try:
        p = Publisher.objects.get(id=id)
    except Exception as e:
        print(e)
    return render(request, 'index/editPublisher.html', {
        'publisher': p,
    })


# 作者列表
def authors(request):
    authors = Author.objects.all().order_by('id')
    return render(request, 'index/authors.html', {
        'authors': authors,
    })


# 添加作者
def addAuthor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not Author.objects.filter(name=name):
            Author.objects.create(name=name)
        return redirect(authors)
    return render(request, 'index/addAuthor.html')


# 编辑作者
def editAuthor(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        try:
            a = Author.objects.get(id=id)
            a.name = name
            a.save()
            return redirect(authors)
        except Exception as e:
            print(e)
    id = request.GET.get('id')
    author = []
    try:
        author = Author.objects.get(id=id)
    except Exception as e:
        print(e)
    return render(request, 'index/editAuthor.html', {
        'author': author,
    })


# 删除作者
def deleteAuthor(request):
    id = request.GET.get('id')
    try:
        Author.objects.get(id=id).delete()
    except Exception as e:
        print(e)
    return redirect(authors)
