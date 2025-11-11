from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import Contact
from .forms import ContactForm

# Import utils functions safely
try:
    from .utils import export_contacts_csv, import_contacts_csv
except ImportError:
    # Fallback functions if utils.py doesn't exist
    import csv
    from io import StringIO
    
    def export_contacts_csv(user):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Job Title', 'Address', 'Birthday'])
        contacts = Contact.objects.filter(user=user)
        for contact in contacts:
            writer.writerow([
                contact.first_name, contact.last_name, contact.email or '',
                contact.phone_number, contact.company or '', contact.job_title or '',
                contact.address or '', contact.birthday.strftime('%Y-%m-%d') if contact.birthday else ''
            ])
        return output.getvalue()
    
    def import_contacts_csv(user, csv_file):
        decoded_file = csv_file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=',')
        next(reader)
        imported_count = 0
        for row in reader:
            if len(row) >= 4 and row[0] and row[1]:
                Contact.objects.create(
                    user=user, first_name=row[0], last_name=row[1],
                    email=row[2] if row[2] else None, phone_number=row[3],
                    company=row[4] if len(row) > 4 and row[4] else None,
                    job_title=row[5] if len(row) > 5 and row[5] else None,
                    address=row[6] if len(row) > 6 and row[6] else None,
                    birthday=row[7] if len(row) > 7 and row[7] else None
                )
                imported_count += 1
        return imported_count

@login_required
def contact_list(request):
    query = request.GET.get('q')
    filter_type = request.GET.get('filter', 'all')
    
    contacts = Contact.objects.filter(user=request.user)
    
    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(company__icontains=query)
        )
    
    if filter_type == 'favorites':
        contacts = contacts.filter(is_favorite=True)
    elif filter_type == 'recent':
        contacts = contacts.order_by('-created_at')[:10]
    elif filter_type == 'birthdays':
        contacts = [contact for contact in contacts if contact.days_until_birthday is not None and contact.days_until_birthday <= 30]
    
    # Get upcoming birthdays
    upcoming_birthdays = []
    for contact in Contact.objects.filter(user=request.user):
        if contact.days_until_birthday is not None and contact.days_until_birthday <= 30:
            upcoming_birthdays.append(contact)
    
    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts, 
        'query': query,
        'filter_type': filter_type,
        'upcoming_birthdays': upcoming_birthdays[:5]
    })

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, '✅ Contact added successfully!')
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Add New Contact'})

@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Contact updated successfully!')
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Edit Contact'})

@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, '🗑️ Contact deleted successfully!')
        return redirect('contact_list')
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})

@login_required
def toggle_favorite(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.is_favorite = not contact.is_favorite
    contact.save()
    action = "added to" if contact.is_favorite else "removed from"
    messages.success(request, f'⭐ Contact {action} favorites!')
    return redirect('contact_list')

@login_required
def export_contacts(request):
    csv_data = export_contacts_csv(request.user)
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_contacts.csv"'
    return response

@login_required
def import_contacts(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            imported_count = import_contacts_csv(request.user, csv_file)
            messages.success(request, f'✅ {imported_count} contacts imported successfully!')
        except Exception as e:
            messages.error(request, f'❌ Error importing contacts: {str(e)}')
        return redirect('contact_list')
    
    return render(request, 'contacts/import_contacts.html')