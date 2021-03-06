import time

from odoo.ticket import common


class HelpdeskTicket(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(HelpdeskTicket, cls).setUpClass()
        helpdesk_ticket = cls.env["helpdesk.ticket"]
        cls.user_admin = cls.env.ref("base.user_root")
        cls.user_demo = cls.env.ref("base.user")
        cls.stage_closed = cls.env.ref("ssg_helpdesk.helpdesk_ticket_stage_done")

        cls.ticket = helpdesk_ticket.create(
            {"name": "Test 1", "description": "Ticket test"}
        )

    def helpdesk_ticket_datetimes(self):
        old_stage_update = self.ticket.last_stage_update

        self.assertTrue(
            self.ticket.last_stage_update,
            "Helpdesk Ticket: Helpdesk ticket should "
            "have a last_stage_update at all times.",
        )

        self.assertFalse(
            self.ticket.closed_date,
            "Helpdesk Ticket: No closed date "
            "should be set for a non closed "
            "ticket.",
        )

        time.sleep(1)

        self.ticket.write({"stage_id": self.stage_closed.id})

        self.assertTrue(
            self.ticket.closed_date,
            "Helpdesk Ticket: A closed ticket " "should have a closed_date value.",
        )
        self.assertTrue(
            old_stage_update < self.ticket.last_stage_update,
            "Helpdesk Ticket: The last_stage_update "
            "should be updated at every stage_id "
            "change.",
        )

        self.ticket.write({"user_id": self.user_admin.id})
        self.assertTrue(
            self.ticket.assigned_date,
            "Helpdesk Ticket: An assigned ticket " "should contain a assigned_date.",
        )

    def helpdesk_ticket_number(self):
        self.assertNotEqual(
            self.ticket.number,
            "/",
            "Helpdesk Ticket: A ticket should have " "a number.",
        )
        ticket_number_1 = int(self.ticket._prepare_ticket_number(values={})[2:])
        ticket_number_2 = int(self.ticket._prepare_ticket_number(values={})[2:])
        self.assertEqual(ticket_number_1 + 1, ticket_number_2)

    def helpdesk_ticket_copy(self):
        old_ticket_number = self.ticket.number

        copy_ticket_number = self.ticket.copy().number

        self.assertTrue(
            copy_ticket_number != "/" and old_ticket_number != copy_ticket_number,
            "Helpdesk Ticket: A new ticket can not "
            "have the same number than the origin ticket.",
        )

    def helpdesk_ticket_message_new(self):
        Partner = self.env["res.partner"]
        Ticket = self.env["helpdesk.ticket"]

        newPartner = Partner.create(
            {
                "name": "??o??n V??n ??t",
                "email": "utdv@ssglove.vn",
            }
        )
        title = "Helpdesk ticket message new"
        msg_id = "utdv@ssglove.vn"
        msg_dict = {
            "message_id": msg_id,
            "subject": title,
            "email_from": "??o??n V??n ??t <utdv@ssglove.vn>",
            "to": "utdv@ssglove.vn",
            "cc": "utdv@ssglove.vn",
            "recipients": "utdv@ssglove.vn+utdv@ssglove.vn",
            "partner_ids": [newPartner.id],
            "body": "This the body",
            "date": "2022-07-16",
        }
        try:
            t = Ticket.message_new(msg_dict)
        except Exception as error:
            self.fail("%s: %s" % (type(error), error))
        self.assertEqual(t.name, title, "The ticket should have the correct title.")

        title = "New title"
        update_vals = {"name": title}
        try:
            t.message_update(msg_dict, update_vals)
        except Exception as error:
            self.fail("%s: %s" % (type(error), error))
        self.assertEqual(
            t.name, title, "The ticket should have the correct (new) title."
        )
