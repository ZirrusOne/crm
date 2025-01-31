import frappe
from frappe import _
from crm.fcrm.doctype.crm_notification.crm_notification import notify_user


<<<<<<< HEAD
	if doc.reference_type in ["CRM Lead", "CRM Deal", "CRM Task", "Contact"] and doc.reference_name and doc.allocated_to:
		notify_assigned_user(doc)

def on_update(doc, method):
=======
def after_insert(doc, method):
    if (
        doc.reference_type in ["CRM Lead", "CRM Deal"]
        and doc.reference_name
        and doc.allocated_to
    ):
        fieldname = "lead_owner" if doc.reference_type == "CRM Lead" else "deal_owner"
        lead_owner = frappe.db.get_value(
            doc.reference_type, doc.reference_name, fieldname
        )
        if not lead_owner:
            frappe.db.set_value(
                doc.reference_type, doc.reference_name, fieldname, doc.allocated_to
            )

    if (
        doc.reference_type in ["CRM Lead", "CRM Deal", "CRM Task"]
        and doc.reference_name
        and doc.allocated_to
    ):
        notify_assigned_user(doc)


def on_update(doc, method):
    if (
        doc.has_value_changed("status")
        and doc.status == "Cancelled"
        and doc.reference_type in ["CRM Lead", "CRM Deal", "CRM Task"]
        and doc.reference_name
        and doc.allocated_to
    ):
        notify_assigned_user(doc, is_cancelled=True)

>>>>>>> SCRUM-9-Frappe

	if doc.has_value_changed("status") and doc.status == "Cancelled" and doc.reference_type in ["CRM Lead", "CRM Deal", "CRM Task", "Contact"] and doc.reference_name and doc.allocated_to:
		notify_assigned_user(doc, is_cancelled=True)
	
def notify_assigned_user(doc, is_cancelled=False):
    _doc = frappe.get_doc(doc.reference_type, doc.reference_name)
    owner = frappe.get_cached_value("User", frappe.session.user, "full_name")
    notification_text = get_notification_text(owner, doc, _doc, is_cancelled)

<<<<<<< HEAD

	message = _("Your assignment on {0} {1} has been removed by {2}").format(
		doc.reference_type,
		doc.reference_name,
		owner
	) if is_cancelled else _("{0} assigned a {1} {2} to you").format(
		owner,
		doc.reference_type,
		doc.reference_name
	)
=======
    message = (
        _("Your assignment on {0} {1} has been removed by {2}").format(
            doc.reference_type, doc.reference_name, owner
        )
        if is_cancelled
        else _("{0} assigned a {1} {2} to you").format(
            owner, doc.reference_type, doc.reference_name
        )
    )
>>>>>>> SCRUM-9-Frappe

    redirect_to_doctype, redirect_to_name = get_redirect_to_doc(doc)

    notify_user(
        {
            "owner": frappe.session.user,
            "assigned_to": doc.allocated_to,
            "notification_type": "Assignment",
            "message": message,
            "notification_text": notification_text,
            "reference_doctype": doc.reference_type,
            "reference_docname": doc.reference_name,
            "redirect_to_doctype": redirect_to_doctype,
            "redirect_to_docname": redirect_to_name,
        }
    )


def get_notification_text(owner, doc, reference_doc, is_cancelled=False):
    name = doc.reference_name
    doctype = doc.reference_type

<<<<<<< HEAD
	if doctype.startswith("CRM "):
		doctype = doctype[4:].lower()
	else:
		doctype = doctype.lower()

	if doctype in ["lead", "deal", "contact"]:
		if doctype == "lead":
			name = reference_doc.lead_name  
		elif doctype == "deal":
			name = reference_doc.organization or name
		elif doctype == "contact":
			name = reference_doc.name
		
		if is_cancelled:
			return f"""
				<div class="mb-2 leading-5 text-gray-600">
					<span>{ _('Your assignment on {0} {1} has been removed by {2}').format(
						doctype,
						f'<span class="font-medium text-gray-900">{ name }</span>',
						f'<span class="font-medium text-gray-900">{ owner }</span>'
					) }</span>
				</div>
			"""
=======
    if doctype.startswith("CRM "):
        doctype = doctype[4:].lower()

    if doctype in ["lead", "deal"]:
        name = (
            reference_doc.lead_name or name
            if doctype == "lead"
            else reference_doc.organization or reference_doc.lead_name or name
        )

        if is_cancelled:
            return f"""
                <div class="mb-2 leading-5 text-ink-gray-5">
                    <span>{ _('Your assignment on {0} {1} has been removed by {2}').format(
                        doctype,
                        f'<span class="font-medium text-ink-gray-9">{ name }</span>',
                        f'<span class="font-medium text-ink-gray-9">{ owner }</span>'
                    ) }</span>
                </div>
            """
>>>>>>> SCRUM-9-Frappe

        return f"""
            <div class="mb-2 leading-5 text-ink-gray-5">
                <span class="font-medium text-ink-gray-9">{ owner }</span>
                <span>{ _('assigned a {0} {1} to you').format(
                    doctype,
                    f'<span class="font-medium text-ink-gray-9">{ name }</span>'
                ) }</span>
            </div>
        """

    if doctype == "task":
        if is_cancelled:
            return f"""
                <div class="mb-2 leading-5 text-ink-gray-5">
                    <span>{ _('Your assignment on task {0} has been removed by {1}').format(
                        f'<span class="font-medium text-ink-gray-9">{ reference_doc.title }</span>',
                        f'<span class="font-medium text-ink-gray-9">{ owner }</span>'
                    ) }</span>
                </div>
            """
        return f"""
            <div class="mb-2 leading-5 text-ink-gray-5">
                <span class="font-medium text-ink-gray-9">{ owner }</span>
                <span>{ _('assigned a new task {0} to you').format(
                    f'<span class="font-medium text-ink-gray-9">{ reference_doc.title }</span>'
                ) }</span>
            </div>
        """


def get_redirect_to_doc(doc):
<<<<<<< HEAD
	if doc.reference_type in ["CRM Task"] :
		reference_doc = frappe.get_doc(doc.reference_type, doc.reference_name)
		return reference_doc.reference_doctype, reference_doc.reference_docname
=======
    if doc.reference_type == "CRM Task":
        reference_doc = frappe.get_doc(doc.reference_type, doc.reference_name)
        return reference_doc.reference_doctype, reference_doc.reference_docname
>>>>>>> SCRUM-9-Frappe

    return doc.reference_type, doc.reference_name
