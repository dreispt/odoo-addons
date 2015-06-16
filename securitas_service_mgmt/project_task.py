# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 - 2014 Daniel Reis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api


class Task(models.Model):
    _inherit = 'project.task'

    location_street = fields.Char('Street', related='location_id.street')
    task_id = fields.Char(compute='_compute_task_id', store=True, index=True)

    @api.one
    @api.depends('create_uid')
    def _compute_task_id(self):
        self.task_id = str(self.id) #Choosing type string makes the field able to be export
