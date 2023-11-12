from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('entry/', views.entry, name="entry"),
    path('logout/', views.logout_view, name="logout"),
    path('process/', views.result_processor, name="process"),
    path('results/', views.admin_viewer, name="results"),
    path('viewer/<int:student_id>/', views.result_viewer, name="viewer"),
    path('master_datasheet/', views.masterdatasheet, name="datasheet"),
    path('error/', views.error, name="error"),
    path('export/', views.export, name="export"),
    path('verify/', views.verify, name="verify"),
    path('register/', views.registration, name="register"),
    path('success/', views.success, name="success"),
    path('check/', views.check_result, name="checker"),
]

