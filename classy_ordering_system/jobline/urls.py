
from django.urls import path
from jobline.views import joblinexml

urlpatterns = [
    path('to-xml/<int:job_id>', joblinexml, name='create-job'),
]