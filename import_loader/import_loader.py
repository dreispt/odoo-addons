# -*- coding: utf-8 -*-
##############################################################################
#
#    Daniel Reis, 2012 - 2014
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

from openerp.osv import fields, orm
from openerp.tools.safe_eval import safe_eval as eval


class import_loader(orm.Model):
    _name = 'import.loader'
    _description = 'Import Loader'
    _columns = {
        'data': fields.text('Data', required=True),
        'xmlid': fields.text('XML Id', readonly=True),
        'state': fields.selection(
            [('draft', 'New'), ('cancel', 'Failed'), ('done', 'Done')],
            'State', select=1),
        'log': fields.text('Execution Log'),
    }
    _defaults = {
        'state': 'draft',
    }

    def create(self, cr, uid, values, context=None):
        """On new record creation, execute the corresponding data import"""

        # TODO: support for option flags
        xmlids_list = []
        log_list = []
        data_list = eval(
            values.get('data'),
            {'null': '', 'Null': '', 'true': '1', 'false': '0'})

        for rec in data_list:
            model_name = rec.pop('_model')
            model = self.pool[model_name]  # Exit loudly on error

            if '.id' in rec and not rec.get('.id'):
                rec.pop('.id')

            fields = rec.keys()
            columns = [str(x) for x in rec.values()]

            res = model.load(cr, uid, fields, [columns], context=context)
            if 'ids' not in res:
                raise orm.except_orm(repr(res))

            if 'id' in rec:
                xmlids_list.append(rec['id'])
            log_list.append(res)

        values.update({
            'state': 'done',
            'log': repr(log_list),
            'xmlid': ','.join(xmlids_list)})
        res = super(import_loader, self).create(
            cr, uid, values, context=context)
        return res

    def do_purge(self, cr, uid, ids=None, lag=7, context=None):
        """Delete processed records older than `lag` days"""
        cr.execute(
            "DELETE FROM import_loader WHERE state<>'draft'"
            " AND write_date < now() - interval '%d' day" % lag)
        return True
