
import frappe
from frappe import _
from frappe.utils import get_url,quoted
from frappe.desk.doctype.notification_log.notification_log import (
	NotificationLog,
	get_email_header,
)
from frappe.desk.doctype.notification_log.notification_log import send_notification_email as original_send_notification_email

# overriding open 
def send_notification_email(doc: NotificationLog):
	if doc.type == "Energy Point" and doc.email_content is None:
		return

	from frappe.utils import get_url_to_form, strip_html

	user = frappe.db.get_value("User", doc.for_user, fieldname=["email", "language"], as_dict=True)
	if not user:
		return

	header = get_email_header(doc, user.language)
	email_subject = strip_html(doc.subject)
	args = {
		"body_content": doc.subject,
		"description": doc.email_content,
	}

	module =  frappe.db.get_value("DocType", doc.document_type, "module")

	if doc.link:
		if module == "FCRM":
			args["doc_link"] = get_crm_url(doc.document_type, doc.document_name)
		else:
			args["doc_link"] = doc.link
	else:
		args["document_type"] = doc.document_type
		args["document_name"] = doc.document_name
		if module == "FCRM":
			args["doc_link"] = get_crm_url(doc.document_type, doc.document_name)
		else:
			args["doc_link"] = get_url_to_form(doc.document_type, doc.document_name)


  
	frappe.sendmail(
		recipients=user.email,
		subject=email_subject,
		template="new_notification",
		args=args,
		header=[header, "orange"],
		now=frappe.flags.in_test,
	)

# make function where pass example  doctype name :- CRM Lead output leads	
@frappe.whitelist()
def get_crm_url(doctype,docname):
	# Remove 'CRM' from the input string and strip any extra whitespace
	cleaned_string = doctype.replace("CRM", "").strip()
	doc_type = cleaned_string.lower() + 's'
	return  get_url(uri=f"/crm/{doc_type}/{quoted(docname)}")

def apply_patch():
    """Apply the monkey patch to override send_notification_email. because send_notification_email is not @frappe.whitlisted  """
    from frappe.desk.doctype.notification_log import notification_log
    notification_log.send_notification_email = send_notification_email
