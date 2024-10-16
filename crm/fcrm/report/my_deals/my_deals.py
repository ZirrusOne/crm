# Copyright (c) 2024, Korecent and contributors
# For license information, please see license.txt

import frappe


# Report function to fetch data
def execute(filters=None):
	# Define columns for the report
    columns = [
        {"label": "Name", "fieldname": "name", "fieldtype": "Data", "width": 150},
        {"label": "Organization", "fieldname": "organization", "fieldtype": "Data", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Email", "fieldname": "email", "fieldtype": "Data", "width": 200},
        {"label": "Assigned To", "fieldname": "deal_owner", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": "Last Email Communication", "fieldname": "last_email_communication", "fieldtype": "Datetime", "width": 180}
    ]
    
	# Fetch data
    data = get_assigned_deals(filters)
    return columns, data



def get_assigned_deals(filters):
	# Current user or user from filter 
    assigned_to = filters.get("user") or frappe.session.user

    conditions = ""  
    # Add condition for status if provided
    if filters.get("status"):
        conditions += f""" AND deal.status =  {filters.get("status")} """
    
    # Add condition for organization if provided
    if filters.get("organization"):
        conditions += f""" AND deal.organization =  {filters.get("organization")} """

    # Execute the SQL query to fetch the assigned deals
    return frappe.db.sql(f"""
        SELECT
            deal.name,
            deal.organization,
            deal.status,
            deal.email, 
            deal.deal_owner, 
            ass.allocated_to AS assigned_to,
            (SELECT MAX(comm.creation) 
             FROM `tabCommunication` AS comm 
             WHERE comm.reference_doctype = 'CRM Deal' 
               AND comm.reference_name = deal.name 
               AND comm.communication_medium = 'Email') AS last_email_communication
        FROM
            `tabCRM Deal` AS deal
        JOIN
            `tabToDo` AS ass
            ON ass.reference_type = 'CRM Deal' 
               AND ass.reference_name = deal.name
        WHERE
            ass.allocated_to = '{assigned_to}' and deal.deal_owner = '{assigned_to}' -- here deal_owner and allocated_to can be diffrent 
            {conditions}
        ORDER BY deal.name
    """, {
        "assigned_to": assigned_to,
        "conditions":conditions
    }, as_dict=True)
