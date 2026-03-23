from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JournalEntry
from .forms import JournalEntryForm

@login_required(login_url="/users/login/")
def entries_list(request):
    journal_entries = JournalEntry.objects.filter(user=request.user).order_by('-entry_date')
    return render(request, 'entries/entries_list.html', { 'entries': journal_entries })

@login_required(login_url="/users/login/")
def entry_new(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)            

            base_count = JournalEntry.objects.filter(user=request.user).count() + 1
            new_slug = f"{request.user.username}-{base_count}"                    
            while JournalEntry.objects.filter(slug=new_slug).exists():
                base_count += 1
                new_slug = f"{request.user.username}-{base_count}"
            new_entry.slug = new_slug
            new_entry.user = request.user            

            new_entry.save()
            form.save_m2m()
            return redirect('entries:list')
    else:
        form = JournalEntryForm()

    return render(request, 'entries/entry_new.html', {'form': form})

@login_required(login_url="/users/login/")
def entry_page(request, slug):
    journal_entry = get_object_or_404(JournalEntry, slug=slug, user=request.user)
    return render(request, 'entries/entry_page.html', { 'entry': journal_entry })

@login_required(login_url="/users/login/")
def entry_edit(request, slug):
    entry = get_object_or_404(JournalEntry, slug=slug, user=request.user)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entries:page', slug=entry.slug)
    else:
        form = JournalEntryForm(instance=entry)

    return render(request, 'entries/entry_edit.html', {'form': form, 'entry': entry})

@login_required(login_url="/users/login/")
def entry_delete(request, slug):
    entry = get_object_or_404(JournalEntry, slug=slug, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('entries:list')
    
    return render(request, 'entries/entry_delete.html', {'entry': entry})