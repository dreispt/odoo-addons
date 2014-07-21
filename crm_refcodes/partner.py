# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 - 2013 Daniel Reis
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

from openerp.osv import orm
from openerp.addons.base_util_refcodes import name_tools


class res_partner(orm.Model):
    _inherit = 'res.partner'

    def name_get(self, cr, uid, ids, context=None):
        return name_tools.extended_name_get(
            self, cr, uid, ids,
            '[%(ref)s] %(name)s', ['ref', 'name'], context=context)

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=100):
        return name_tools.extended_name_search(
            self, cr, user, name, args,
            operator, context=context, limit=limit, keys=['ref', 'name'])
