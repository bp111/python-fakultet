from django.shortcuts import render

def entries_list(request):
    return render(request, 'entries/entries_list.html')