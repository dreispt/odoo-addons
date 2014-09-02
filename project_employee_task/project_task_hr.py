# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Hugo Santos
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

from openerp.osv import orm, fields


class project_task(orm.Model):
    _inherit = 'project.task'

    _columns = {
        'use_employee': fields.related(
            'project_id', 'use_employee',
            type='char', string="Use Employee"),
        'employee_id': fields.many2one('hr.employee', 'Employee')
    }

    def onchange_project(self, cr, uid, id, project_id, context=None):
        # on_change is necessary to populate fields on Create, before saving
        try:
            # try applying a parent's onchange, may it exist
            res = super(project_task, self).onchange_project(
                cr, uid, id, project_id, context=context) or {}
        except AttributeError:
            res = {}

        res.setdefault('value', {})
        if project_id:
            obj = self.pool.get('project.project').browse(
                cr, uid, project_id, context=context)
            res['value']['use_employee'] = (
                obj.use_employee or 'no')
        else:
            res['value']['use_employee'] = 'no'
        return res
