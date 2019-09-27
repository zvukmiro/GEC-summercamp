from django.urls import path
# local django
from . import views


urlpatterns=[
    path('', views.index, name='index'),
    path('camps/', views.CampThemeListView.as_view(), name='camps'),
    path('camps/<int:pk>', views.CampThemeDetailView.as_view(), name='camp-detail'),
    path('parent/<int:pk>', views.ParentDetailView.as_view(), name='parent-detail'),
    path('child/<int:pk>', views.child_detail, name='child-detail'),
    path('child/create', views.ChildCreate.as_view(), name='add-child'),
    path('child/<int:pk>/update', views.ChildUpdate.as_view(), name='edit-child'),
    path('child/<int:pk>/delete', views.ChildDelete.as_view(), name='delete-child'),
    ]
