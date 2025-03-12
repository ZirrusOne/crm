# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data  = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"fieldname": "campaign", "label": _("Campaign"), "fieldtype": "Link","options":"CRM Campaign", "width": 240},
		{"fieldname": "lead_count", "label": _("Lead Count"), "fieldtype": "Int", "width": 240},
		{"fieldname": "deal_count", "label": _("Deal Count"), "fieldtype": "Int", "width": 240},
		{"fieldname": "deal_value", "label": _("Deal Value"), "fieldtype": "Float", "width": 240},
		{"fieldname": "deal_lead", "label": _("Deal/Lead %"), "fieldtype": "Float", "width": 240},
	]

def get_data(filters):
	conditions = get_filter_conditions(filters)
	data = frappe.db.sql(f""" SELECT C.name as campaign,
		COUNT(DISTINCT (CP.reference_docname)) AS lead_count,
        COUNT(DISTINCT CASE WHEN CP.reference_docname = D.lead THEN CP.reference_docname END) AS deal_count,
        SUM(D.annual_revenue) AS deal_value,
        (COUNT(DISTINCT CASE WHEN CP.reference_docname = D.lead THEN CP.reference_docname END) * 100) / 
        COUNT(DISTINCT CP.reference_docname) AS deal_lead
        FROM `tabCRM Campaign` AS C
        INNER JOIN `tabCRM Campaign Participants` AS CP ON C.name = CP.parent
        LEFT JOIN `tabCRM Deal` AS D ON CP.reference_docname = D.lead
        WHERE CP.participant_source = 'CRM Lead' 
        AND C.status != 'Closed' {conditions} group by C.name""", as_dict=1)
	return data


def get_filter_conditions(filters):
	conditions = ""
	if filters.from_date:
		conditions += f" and date(C.creation) >= '{filters.from_date}'"
	if filters.to_date:
		conditions += f" and date(C.creation) <= '{filters.to_date}'"
	if filters.campaign:
		conditions += f" and C.name = '{filters.campaign}'"
	return conditions

