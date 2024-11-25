import frappe
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def add_attachments_on_note(note, attachments):
    if note and not isinstance(note, dict):
        note = note.as_dict()
    print(f" note {note}")
    if note.get('name'):
        doc = frappe.get_doc("FCRM Note", note.get('name'))
        if note.get('title'):
            doc.update({"title": note.get('title')})
        if note.get('content'):
            doc.update({"content": note.get('content')})
        if len(attachments) > 0:
            for attach in attachments:
                row = doc.append("attachments", {})
                row.file_url= attach
        
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return doc.name
        
    else:
        doc = frappe.new_doc("FCRM Note")
        doc.update({
            "title": note.get('title'),
            "content": note.get('content')
        })
        if len(attachments) > 0:
            # attachments_list = []
            for attach in attachments:
               row = doc.append("attachments", {})
               row.file_url= attach
        
        doc.insert(ignore_permissions=True)
        print(f"doc {doc.as_dict()}")
        frappe.db.commit()
        return doc.name


@frappe.whitelist()
def get_attachments_from_note(note_name):
    print(f"note_name {note_name}")
    file_url = frappe.db.get_all("CRM Note Attachments", {'parent':note_name},pluck="file_url")
    print(f"file_url {file_url}")
    return file_url if len(file_url) > 0 else []
        

