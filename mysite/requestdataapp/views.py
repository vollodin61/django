import os

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from requestdataapp.templates.requestdataapp.forms import UserBioForm, UploadFileForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", '')
    b = request.GET.get("b", '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        "result": result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':  # and request.FILES.get('myfile'):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES['myfile']
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            file_size = fs.size(myfile.name)
            if file_size > 1024 * 1024 * 100:
                fs.delete(myfile.name)
                print(f"File {myfile.name} is too big, deleted")
                return render(request,'requestdataapp/file-too-large.html', {'error': 'File is too big'})
            else:
                print('Saved file to %s' % filename)
    else:
        form = UploadFileForm()
    context = {
        'form': form
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)
