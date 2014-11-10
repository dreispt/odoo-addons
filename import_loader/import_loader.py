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

from openerp import models, fields, api
from openerp.tools.safe_eval import safe_eval as eval


class import_loader(models.TransientModel):
    _name = 'import.loader'
    _description = 'Import Loader'
    data = fields.Text('Data', required=True)
    xmlid = fields.Text('XML Id', readonly=True)
    state = fields.Selection(
        [('draft', 'New'), ('cancel', 'Failed'), ('done', 'Done')],
        'State', default='draft', index=True)
    log = fields.Text('Execution Log')

    @api.model
    def create(self, values):
        """On new record creation, execute the corresponding data import"""

        # TODO: support for option flags
        xmlids_list = []
        log_list = []
        data_list = eval(
            values.get('data'),
            {'null': '', 'Null': '', 'true': '1', 'false': '0'})
        assert isinstance(data_list, list)

        cr, uid, ctx = self.env.cr, self.env.uid, self.env.context
        for rec in data_list:
            assert isinstance(rec, dict)
            assert rec.get('_model')
            model_name = rec.pop('_model')
            model = self.pool[model_name]  # Exit loudly on error

            if '.id' in rec and not rec.get('.id'):
                rec.pop('.id')

            fields = rec.keys()
            columns = [str(x) for x in rec.values()]

            res = model.load(cr, uid, fields, [columns], context=ctx)
            if 'ids' not in res:
                raise Exception(repr(res))

            if 'id' in rec:
                xmlids_list.append(rec['id'])
            log_list.append(res)

        values.update({
            'state': 'done',
            'log': repr(log_list),
            'xmlid': ','.join(xmlids_list)})
        res = super(import_loader, self).create(values)
        return res
