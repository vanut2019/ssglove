# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

xmlid_renames = [
    (
        "ssg_helpdesk.helpesk_ticket_personal_rule",
        "ssg_helpdesk.helpdesk_ticket_personal_rule",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, xmlid_renames)
