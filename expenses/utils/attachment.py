# Expenses © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe

from .common import parse_json


# Expense
# Expense Form
# Expenses Entry
# Expenses Entry Form
@frappe.whitelist(methods=["POST"])
def delete_attach_files(doctype, name, files):
    if not files:
        return 0
    
    files = parse_json(files)
    
    if not files or not isinstance(files, list):
        return 0
    
    dt = "File"
    if (file_names := frappe.get_all(
        dt,
        fields=["name"],
        filters=[
            ["file_url", "in", files],
            ["attached_to_doctype", "=", doctype],
            ["ifnull(`attached_to_name`,\"\")", "in", [name, ""]]
        ],
        pluck="name"
    )):
        for file in file_names:
            (frappe.get_doc(dt, file)
                .delete(ignore_permissions=True))
    
    return 1


## Self Expense
def get_attachments_by_parents(parents, parent_type, parent_field):
    data = frappe.get_all(
        "Expense Attachment",
        fields=["parent", "file", "description"],
        filters=[
            ["parent", "in", parents],
            ["parenttype", "=", parent_type],
            ["parentfield", "=", parent_field]
        ]
    )
    
    if not data or not isinstance(data, list):
        return None
    
    groups = {}
    for v in data:
        k = v["parent"]
        if k not in groups:
            groups[k] = []
        
        groups[k].append({
            "file": v["file"],
            "description": v["description"],
        })
    
    return groups