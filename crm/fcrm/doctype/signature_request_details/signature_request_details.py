# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from collections import namedtuple
from frappe.utils import add_to_date, cast, nowdate, validate_email_address
import frappe.utils
from frappe.utils.safe_exec import get_safe_globals
from frappe.utils import random_string

class SignatureRequestDetails(Document):
	def before_insert(self):
		self.signature_url = random_string(20)
		self.expiry_date = add_to_date(nowdate(), days=7)




@frappe.whitelist()
def get_context(doc):
	Frappe = namedtuple("frappe", ["utils"])
	return {
		"doc": doc,
		"nowdate": nowdate,
		"frappe": Frappe(utils=get_safe_globals().get("frappe").get("utils")),
	}



@frappe.whitelist(allow_guest=True)	
def get_document(signature_url):
	signature_url =  frappe.db.get_value("Signature Request Details", {"signature_url": signature_url}, "name")
	if not signature_url:
		return frappe.throw("Signature Request Details not found")

	sign_doc = frappe.get_doc("Signature Request Details", signature_url)  
 
	if sign_doc.is_signed :
		return frappe.throw("Signature already added.")
	if sign_doc.expiry_date < nowdate():
		return frappe.throw("Signature Request Details expired.")

 
	doc = frappe.get_doc(sign_doc.document_type, sign_doc.docname)

	context = get_context(doc)
	template = sign_doc.document


	return frappe.render_template(template, context)



@frappe.whitelist(allow_guest=True)
def get_signature(signature_url):
	signature_url =  frappe.db.get_value("Signature Request Details", {"signature_url": signature_url}, "name")
	if not signature_url:
		return frappe.throw("Signature Request Details not found")

	signedBy =  frappe.form_dict.signedBy
	signedDate =  frappe.form_dict.signedDate
	signatureData =  frappe.form_dict.signatureData
		
	sign_doc = frappe.get_doc("Signature Request Details", signature_url)
	if sign_doc.is_signed:
		return frappe.throw("Signature already added.")

	if sign_doc.expiry_date < nowdate():
		return frappe.throw("Signature Request Details expired.")




	sign_doc.signed_by = signedBy
	sign_doc.signed_date = frappe.utils.getdate(signedDate)
	sign_doc.signature = signatureData
	sign_doc.is_signed = 1
	sign_doc.save(ignore_permissions=True)
	frappe.db.commit()
	frappe.msgprint("Signature added successfully.")

	return sign_doc
 
























@frappe.whitelist(allow_guest=True)	
def test_context():
	todo_doc = frappe.get_doc("CRM Deal", 'CRM-DEAL-2024-00067')
	context = get_context(todo_doc)

	template = """
			<h1>CRM Deal: {{ doc.name }}</h1>
			<p><strong>Owner:</strong> {{  doc.owner }}</p>
			<p><strong>Creation Date:</strong> {{  doc.creation }}</p>
			<p><strong>Last Modified:</strong> {{  doc.modified }}</p>

			<h2>General Details</h2>
			<ul>
				<li><strong>Status:</strong> {{ doc.status }}</li>
				<li><strong>Deal Owner:</strong> {{  doc.deal_owner }}</li>
				<li><strong>Organization:</strong> {{  doc.organization }}</li>
				<li><strong>Organization Name:</strong> {{  doc.organization_name }}</li>
				<li><strong>Website:</strong> <a href="{{  doc.website }}" target="_blank">{{  doc.website }}</a></li>
				<li><strong>Currency:</strong> {{  doc.currency }}</li>
			</ul>

			<h2>Financial Details</h2>
			<ul>
				<li><strong>Probability:</strong> {{  doc.probability }}%</li>
				<li><strong>Weighted Amount:</strong> {{  doc.weighted_amount }}</li>
				<li><strong>Annual Revenue:</strong> {{  doc.annual_revenue }}</li>
			</ul>

			<h2>Additional Information</h2>
			<ul>
				<li><strong>Communication Status:</strong> {{  doc.communication_status }}</li>
				<li><strong>Industry:</strong> {{  doc.industry }}</li>
				<li><strong>No. of Employees:</strong> {{  doc.no_of_employees }}</li>
				<li><strong>Territory:</strong> {{  doc.territory }}</li>
			</ul>

			<h2>Contact Information</h2>
			<ul>
				<li><strong>Salutation:</strong> {{  doc.salutation }}</li>
				<li><strong>First Name:</strong> {{  doc.first_name }}</li>
				<li><strong>Last Name:</strong> {{  doc.last_name }}</li>
				<li><strong>Email:</strong> {{  doc.email }}</li>
				<li><strong>Mobile Number:</strong> {{  doc.mobile_no }}</li>
				<li><strong>Phone Number:</strong> {{  doc.phone }}</li>
				<li><strong>Gender:</strong> {{  doc.gender }}</li>
			</ul>

			<h2>Deal Elements</h2>


				<table class="table">
				<thead>
					<tr>
						<th>Name</th>
						<th>Deal Element</th>
						<th>Created By</th>
						<th>Creation Date</th>
						<th>Parent Deal</th>
					</tr>
				</thead>
    					{% for element in  doc.deal_elements %}
					
				<tbody><tr>
						<td>{{ element.name }}</td>
						<td>{{ element.deal_elements }}</td>
						<td>{{ element.owner }}</td>
						<td>{{ element.creation }}</td>
						<td>{{ element.parent }}</td>
					</tr></tbody>
				<tbody>
    			{% endfor %}

			</table>

			<h2>Status Change Log</h2>

					
				<table class="table">
				<thead>
					<tr>
						<th>From</th>
						<th>To</th>
						<th>Date</th>
						<th>Log Owner</th>
					</tr>
				</thead>
    					{% for log in  doc.status_change_log %}

				<tbody><tr>
						<td>{{ log.from }}</td>
						<td>{{ log.to }}</td>
						<td>{{ log.from_date }}</td>
						<td>{{ log.log_owner }}</td>
					</tr></tbody>
     					{% endfor %}

			</table>



 			"""

	return frappe.render_template(template, context)





















