from django.conf.urls import url
from .views import index, publisher_list
# 图书表需要引入的方法
from .views import deleteBook, editBook, deletePublisher, addBook
# 作者表
from .views import authors, addAuthor, editAuthor, deleteAuthor
# 出版社
from .views import editPublisher, addPublisher
# 用户
from .views import login, register,logout

urlpatterns = [
    url(r'^index/$', index),
    # 用户表操作
    url(r'^login/', login),
    url(r'^register/', register),
    url(r'^logout/', logout),

    # 出版社操作
    url(r'^publishers/$', publisher_list),
    url(r'^addPublisher/$', addPublisher),
    url(r'^editPublisher/$', editPublisher),
    url(r'^deletePublisher/$', deletePublisher),

    # 作者表操作
    url(r'^authors/$', authors),
    url(r'^addAuthor/$', addAuthor),
    url(r'^editAuthor/$', editAuthor),
    url(r'^deleteAuthor/$', deleteAuthor),

    # 图书表操作
    url(r'^deleteBook/$', deleteBook),
    url(r'^editBook/$', editBook),
    url(r'^addBook/$', addBook),
    url(r'^$', index),
]
