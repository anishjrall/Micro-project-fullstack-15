import csv
from io import StringIO
from .models import Contact

def export_contacts_csv(user):
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Job Title', 'Address', 'Birthday'])
    
    # Write contacts
    contacts = Contact.objects.filter(user=user)
    for contact in contacts:
        writer.writerow([
            contact.first_name,
            contact.last_name,
            contact.email or '',
            contact.phone_number,
            contact.company or '',
            contact.job_title or '',
            contact.address or '',
            contact.birthday.strftime('%Y-%m-%d') if contact.birthday else ''
        ])
    
    return output.getvalue()

def import_contacts_csv(user, csv_file):
    decoded_file = csv_file.read().decode('utf-8')
    io_string = StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=',')
    
    next(reader)  # Skip header
    imported_count = 0
    
    for row in reader:
        if len(row) >= 4 and row[0] and row[1]:  # At least first name, last name
            Contact.objects.create(
                user=user,
                first_name=row[0],
                last_name=row[1],
                email=row[2] if row[2] else None,
                phone_number=row[3],
                company=row[4] if len(row) > 4 and row[4] else None,
                job_title=row[5] if len(row) > 5 and row[5] else None,
                address=row[6] if len(row) > 6 and row[6] else None,
                birthday=row[7] if len(row) > 7 and row[7] else None
            )
            imported_count += 1
    
    return imported_count