import base64
import logging

import werkzeug

import odoo.http as http
from odoo.http import request

_logger = logging.getLogger(__name__)


class HelpdeskTicketController(http.Controller):
    @http.route("/ticket/close", type="http", auth="user")
    def support_ticket_close(self, **kw):
        """Close the support ticket"""
        values = {}
        for field_name, field_value in kw.items():
            if field_name.endswith("_id"):
                values[field_name] = int(field_value)
            else:
                values[field_name] = field_value
        ticket = (http.request.env["helpdesk.ticket"].sudo().search([("id", "=", values["ticket_id"])]))
        ticket.stage_id = values.get("stage_id")
        return werkzeug.utils.redirect("/my/ticket/" + str(ticket.id))

    @http.route("/new/ticket", type="http", auth="user", website=True)
    def create_new_ticket(self, **kw):
        email = http.request.env.user.email
        name = http.request.env.user.name
        list_modules = []
        categories = http.request.env["helpdesk.ticket.category"].search([("active", "=", True)])
        urgencies = http.request.env["helpdesk.ticket.urgency"].search([("active", "=", True)])
        partner_id = http.request.env["res.partner"].search([("id", "=", http.request.env.user.partner_id.parent_id.id)], limit=1)
        modules = http.request.env["helpdesk.ticket.module"].search([("active", "=", True)])
        for module in modules:
            for partner in module.partner_ids:
                if partner.id == partner_id.id:
                    list_modules.append(module.id)
        modules = modules.filtered(lambda e: e.id in list_modules or e.name == '-')
        environments = http.request.env["helpdesk.ticket.environment"].search([("active", "=", True)])
        return http.request.render(
            "helpdesk_pro.portal_create_ticket",
            {"categories": categories, "email": email, "name": name, "urgencies": urgencies, "modules": modules, "environments": environments},
        )

    @http.route("/submitted/ticket", type="http", auth="user", website=True, csrf=True)
    def submit_ticket(self, **kw):
        partner = request.env["res.partner"].sudo().search(
            [("name", "=", kw.get("name")), ("email", "=", kw.get("email"))])
        vals = {
            "partner_name": kw.get("name"),
            "company_id": http.request.env.user.company_id.id,
            "category_id": kw.get("category"),
            "type_urgency": kw.get("urgency"),
            "modules_id": kw.get("module"),
            "environment": kw.get("environment"),
            "partner_email": kw.get("email"),
            "description": kw.get("description"),
            "name": kw.get("subject"),
            "attachment_ids": False,
            "channel_id": request.env["helpdesk.ticket.channel"].sudo().search([("name", "=", "Web")]).id,
            "partner_id": partner.id,
            "client_id": partner.parent_id.id,
        }
        new_ticket = request.env["helpdesk.ticket"].sudo().create(vals)
        new_ticket.message_subscribe(partner_ids=request.env.user.partner_id.ids)
        if kw.get("attachment"):
            for c_file in request.httprequest.files.getlist("attachment"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "helpdesk.ticket",
                            "res_id": new_ticket.id,
                        }
                    )
        return werkzeug.utils.redirect("/my/tickets")