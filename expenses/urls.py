from django.conf.urls import url

from . import views

app_name = "expenses"

urlpatterns = [
    url(r'^$', views.list, name="list"),
    url(r'^month/$', views.list_months, name="months"),
    url(r'^month/(20[0-9][0-9])/$', views.list, name="year"),
    url(r'^month/(20[0-9][0-9])/(1?[0-9])/$', views.list, name="month"),

    url(r'^category/$', views.list_categories, name="categories"),
    url(r'^category/([0-9]+)/$', views.list_by_category, name="category"),

    url(r'^create/$', views.create, name="create"),
    url(r'^([0-9]+)/$', views.detail, name="detail"),
    url(r'^([0-9]+)/edit/$', views.update, name="update"),
    url(r'^([0-9]+)/delete/$', views.delete, name="delete"),
    url(r'^feedback/$', views.send_feedback, name="feedback"),
]
