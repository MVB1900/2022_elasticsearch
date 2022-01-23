from django.shortcuts import render
from myapp.models import Note
# Create your views here.
def search_view(request):
    context = {
        'title': "Tìm kiếm nhanh"
    }
    return render(request, 'search/search.html', context)

# Create your views here.
def read_body(request, id):
    note_body = Note.objects.get(id=id)
    context = {
        'title': note_body.title,
        'note_body': note_body
    }
    return render(request, 'search/read_body.html', context)