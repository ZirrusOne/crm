import frappe

from crm.api.doc import get_assigned_users, get_fields_meta
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script


@frappe.whitelist()
def get_lead(name):
	lead = frappe.get_doc("CRM Lead", name).as_dict()

	lead["fields_meta"] = get_fields_meta("CRM Lead")
	lead["_form_script"] = get_form_script('CRM Lead')
	lead["_assign"] = get_assigned_users("CRM Lead", lead.name, lead.owner)
	organization_name = frappe.db.get_value("CRM Lead", lead.name, "organization") 
	if organization_name:
		lead['partner_leads'] = frappe.get_list("CRM Lead", filters=[["organization",'=',organization_name],['status','!=','Contacted'],['converted','!=',1]], fields=["name"])
	else:
		lead['partner_leads'] = []
	return lead
