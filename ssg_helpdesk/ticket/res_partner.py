from odoo.ticket.common import SavepointCase


class Partner(SavepointCase):
    def setUp(self):
        super(Partner, self).setUp()
        self.partner_obj = self.env["res.partner"]
        self.ticket_obj = self.env["helpdesk.ticket"]
        self.stage_id_closed = self.env.ref("ssg_helpdesk.helpdesk_ticket_stage_done")
        self.parent_id = self.partner_obj.create({"name": "Parent 1"})
        self.child_id_1 = self.partner_obj.create({"name": "Child 1"})
        self.child_id_2 = self.partner_obj.create({"name": "Child 2"})
        self.child_id_3 = self.partner_obj.create({"name": "Child 3"})
        self.tickets = []
        self.parent_id.child_ids = [
            (4, self.child_id_1.id),
            (4, self.child_id_2.id),
            (4, self.child_id_3.id),
        ]
        for i in [69, 155, 314, 420]:
            self.tickets.append(
                self.ticket_obj.create(
                    {
                        "name": "Nice ticket {}".format(i),
                        "description": "Nice ticket {} description".format(i),
                    }
                )
            )
        self.parent_id.helpdesk_ticket_ids = [(4, self.tickets[0].id)]
        self.child_id_1.helpdesk_ticket_ids = [(4, self.tickets[1].id)]
        self.child_id_2.helpdesk_ticket_ids = [(4, self.tickets[2].id)]
        self.child_id_3.helpdesk_ticket_ids = [(4, self.tickets[3].id)]
        self.child_id_3.helpdesk_ticket_ids[-1].stage_id = self.stage_id_closed

    def ticket_count(self):
        self.assertEqual(self.parent_id.helpdesk_ticket_count, 4)

    def ticket_active_count(self):
        self.assertEqual(self.parent_id.helpdesk_ticket_active_count, 3)

    def ticket_string(self):

        self.assertEqual(self.parent_id.helpdesk_ticket_count_string, "3 / 4")
