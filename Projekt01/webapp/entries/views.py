from django.shortcuts import render
from .models import JournalEntry

def entries_list(request):
    journal_entries = JournalEntry.objects.all().order_by('-entry_date')
    return render(request, 'entries/entries_list.html', { 'entries': journal_entries })

def entry_page(request, slug):
    journal_entry = JournalEntry.objects.get(slug=slug)
    return render(request, 'entries/entry_page.html', { 'entry': journal_entry })