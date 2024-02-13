from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import pythoncom
from pdf2docx import Converter
from docx2pdf import convert


# Home page
def index(request):
  return render(request, 'index.html')



# Converts from pdf to word format
def pdfToWord(request):
   if request.method == 'POST' and request.FILES['pdf_to_word']:
      pdf_to_word = request.FILES['pdf_to_word']

      # Check if the uploaded file is a PDF
      if not pdf_to_word.content_type == 'application/pdf':
        messages.error(request, "The uploaded file is not a PDF.")
      
      else:
        pdf_name = pdf_to_word.name
        fs = FileSystemStorage()
        filename = fs.save(pdf_to_word.name, pdf_to_word)
        pdf_path = os.path.join(settings.MEDIA_ROOT, filename)
        word_path = os.path.join(settings.MEDIA_ROOT, filename.replace('.pdf', '.docx'))

        # Convert PDF to Word
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)
        cv.close()

        # Return the converted Word file
        with open(word_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{pdf_name.replace(".pdf", ".docx")}"'
            return response

   return redirect('index')



# Converts from word docx to pdf format
def wordToPdf(request):
   if request.method == 'POST' and request.FILES['word_to_pdf']:
      word_to_pdf = request.FILES['word_to_pdf']

      # Check if the uploaded file is a word docx
      if not word_to_pdf.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        messages.error(request, "The uploaded file is not a word docx file.")

      else:
        word_name = word_to_pdf.name
        fs = FileSystemStorage()
        filename = fs.save(word_to_pdf.name, word_to_pdf)
        word_path = os.path.join(settings.MEDIA_ROOT, filename)
        pdf_path = os.path.join(settings.MEDIA_ROOT, filename.replace('.docx', '.pdf'))

        # Initialize COM
        pythoncom.CoInitialize()

        # Convert Word to PDF
        convert(word_path, pdf_path)

        # Return the converted PDF file
        with open(pdf_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{word_name.replace(".docx", ".pdf")}"'
            return response

   return redirect('index')



# About Page
def about(request):
  return render(request, 'about.html')



# Signup page
def signup(request):
  try:
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already used, Try Another.")
                return redirect('signup')
        
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken, Try Another.")
                return redirect('signup')
        
            else:
                new_user = User.objects.create_user(email=email, username=username, password=password)
                new_user.save()

                login_user = auth.authenticate(username=username, password=password)
                auth.login(request, login_user)

                user_model = User.objects.get(username=username)
                new_user_profile = UserProfile.objects.create(
                    user=user_model,
                    id_user=user_model.id,
                    address=address,
                    phone_number=phone
                )
                new_user_profile.save()

                messages.info(request, f'Welcome {username}.')
                return redirect('index')
        
        else:
            messages.info(request, "Password not the same.")
            return redirect('signup')
    else:
        return render(request, 'signup.html')
        
  except:
      return render(request, 'error.html')



# Login page
def login(request):
  try:
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials.')
            return redirect('login')
    
    else:
        return render(request, 'login.html')
  except:
      return render(request, 'error.html')



# Log Out
def logout(request):
  try:
      auth.logout(request)
      return redirect('login')
  except:
      return render(request, 'error.html')