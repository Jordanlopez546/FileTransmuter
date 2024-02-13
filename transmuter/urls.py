from .views import *
from django.urls import path


urlpatterns = [
  path('', index, name='index'),
  path('about/', about, name='about'),
  path('signup', signup, name='signup'),
  path('login', login, name='login'),
  path('pdfToWord', pdfToWord, name='pdfToWord'),
  path('wordToPdf', wordToPdf, name='wordToPdf'),
  # path('pdfToPpt', pdfToPpt, name='pdfToPpt'),
  # path('pptToPdf', pptToPdf, name='pptToPdf'),
  # path('pptToWord', pptToWord, name='pptToWord'),
  # path('wordToPpt', wordToPpt, name='wordToPpt'),
]