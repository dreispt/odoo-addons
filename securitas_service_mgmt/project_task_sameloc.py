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

from openerp import models, fields, api


class Task(models.Model):
    _inherit = 'project.task'

    sameloc_tasks = fields.One2many(
        'project.task',
        string='Other Open Tasks',
        compute='_compute_sameloc_tasks')

    @api.one
    def _compute_sameloc_tasks(self):
        if self.location_id:
            query = [('stage_id.fold', '=', False),
                     ('id', '!=', self.id),
                     ('location_id', '=', self.location_id.id)]
            self.sameloc_tasks = self.search(query)
