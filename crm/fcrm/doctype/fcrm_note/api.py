import frappe
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def add_attachments_on_note(note, attachments):
    if note and not isinstance(note, dict):
        note = note.as_dict()
    print(f" attachments {attachments}")
    if note.get('name'):
        doc = frappe.get_doc("FCRM Note", note.get('name'))
        if note.get('title'):
            doc.update({"title": note.get('title')})
        if note.get('content'):
            doc.update({"content": note.get('content')})
        if len(attachments) > 0:
            for attach in attachments:
                row = doc.append("attachments", {})
                row.file_url = frappe.db.get_value("File", attach.get("name"), "file_url")
         
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
    print(f"note_name: {note_name}")
    
    # Query the database to fetch name and file_url
    attachments = frappe.db.get_all(
        "CRM Note Attachments", 
        filters={'parent': note_name},
        fields=['name', 'file_url']
    )
    
    # Transform the result to use `file_name` instead of `name`
    formatted_attachments = [{'file_url': att['name'], 'file_name': att['file_url']} for att in attachments]
    
    print(f"attachments: {formatted_attachments}")
    
    # Return the formatted list or an empty list if none found
    return formatted_attachments if formatted_attachments else []
