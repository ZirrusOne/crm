# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
# Scrum-71 - Recently assigned report (10-16-2024)-Anuradha
import frappe
from frappe import _
from datetime import datetime, date

def execute(filters):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "lead_name", "label": _("Lead Name"), "fieldtype": "Link","options": "Lead", "width": 220},
        {"fieldname": "organization", "label": _("Organization"), "fieldtype": "Data", "width": 200},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Link","options": "CRM Lead Status", "width": 200},
        {"fieldname": "email_id", "label": _("Email Id"), "fieldtype": "Data", "width": 200},
        {"fieldname": "assigned_to", "label": _("Assigned To"), "fieldtype": "Link", "options": "User", "width": 200},
        {"fieldname": "time_assigned", "label": _("Time Assigned"), "fieldtype": "Data", "width": 200}
    ]

def get_data(filters):
    #get filter condition
    conditions = get_filter_conditions(filters)

    #fetch lead data order by creation date
    lead_details = frappe.db.sql(f"""select  L.name as lead_name, L.organization as organization, 
                                    L.status as status, L.email as email_id, L.creation as creation
                                   from `tabCRM Lead` as L order by L.creation desc""",as_dict=1)
    
    #fetch time if creation date is today else fetch date
    for lead in lead_details:
        lead['assigned_to'] = frappe.db.get_value("ToDo", {'reference_type':'CRM Lead', 'reference_name':lead['lead_name']},'allocated_to' )
        if (lead.get('creation')).date() == date.today():
            lead['time_assigned'] = lead.get('creation').strftime('%I:%M %p')
        else:
            lead['time_assigned'] = lead.get('creation').date() 
    return lead_details

def get_filter_conditions(filters):
    conditions = ""
    if filters.from_date:
        conditions += f" date(L.creation) >= {filters.from_date}"
    if filters.to_date:
        conditions += f" and date(L.creation) <= {filters.to_date}"
    return conditions
