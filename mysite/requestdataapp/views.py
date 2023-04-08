import os

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
    return render(request, 'requestdataapp/user-bio-form.html')


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_size = fs.size(myfile.name)
        if file_size > 1024 * 1024:
            fs.delete(myfile.name)
            print(f"File {myfile.name} is too big, deleted")
            return render(request,'requestdataapp/file-too-large.html', {'error': 'File is too big'})
        else:
            print('Saved file to %s' % filename)
    return render(request, 'requestdataapp/file-upload.html')
