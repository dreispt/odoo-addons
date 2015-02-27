# -*- coding: utf-8 -*-
##############################################################################
#
#    Daniel Reis, 2012 - 2015
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

import logging
_logger = logging.getLogger(__name__)


def jsontext2object(text):
    val_map = {'null': '', 'Null': '', 'true': '1', 'false': '0'}
    data_list = eval(text, val_map)
    return data_list


class ImportLoader(models.TransientModel):
    _name = 'import.loader'
    _description = 'Import Loader'

    data = fields.Text('Data', required=True)
    state = fields.Selection(
        [('wait', 'Async Import'),
         ('open', 'Immediate Import'),
         ('cancel', 'Import Failed'),
         ('done', 'Import Done')],
        'State',
        default='open',
        index=True)
    log = fields.Text('Execution Log')
    xmlid = fields.Text('XML Id Info', readonly=True)
    fast_load = fields.Boolean('Fast Load?', default=False)

    @api.model
    def _fix_model_data(self):
        sql = "update ir_model_data set module='__export__' where module=''"
        self.env.cr.execute(sql)
        self.env.cr.commit()

    @api.model
    def _get_res_id(self, xmlid, silent=False):
        # TODO: handle xmlids with "module.name"
        value = xmlid.strip()
        if value:
            sql = "select res_id from ir_model_data " \
                  "where name=%s order by res_id"
            self.env.cr.execute(sql, (value,))
            res_id = self.env.cr.fetchone()
            if not res_id and not silent:
                _logger.warn('XMLId %s not found', value)
            return res_id and res_id[0] or None

    @api.model
    def _set_xml_id(self, xmlid, res_id, model):
        if self._get_res_id(xmlid, silent=True):
            return False
        else:
            return self.env['ir.model.data'].create({
                'name': xmlid,
                'model': model,
                'res_id': res_id,
                'module': '__export__'})

    @api.model
    def _preprocess_data(self, data_dict, model_name, fast_load):
        """ Fix issues with IDs and XML IDs.
        Removes empty 'id' and '.id' fields, to avoid issues with load()
        Ensure XMLIds have a module.xmlid form, prepending __export__.

        Takes a data dictionary and the model name.
        Returns a data dictionary. No side effects.
        """
        res = {}
        for field, value in data_dict.items():
            if field in ['id', '.id'] and not value:
                # Just in case, ignore id=0 columns
                # See https://github.com/odoo/odoo/pull/2258
                continue
            if field.endswith('/id') or field == 'id' and value:
                if fast_load:
                    value = self._get_res_id(value, silent=field == 'id')
                    field = field[:-3] or '.id'
                else:
                    value = '__export__.%s' % str(value).strip()
            # load values must be str
            res[field] = value if fast_load else str(value)

        return res

    @api.model
    def _load_one(self, data_dict, fast_load):
        assert '_model' in data_dict, \
               'A _model key is required in the data dictionary'
        model_name = data_dict.pop('_model')
        model = self.env[model_name]
        xmlid = data_dict.get('id', '')
        data_dict = self._preprocess_data(data_dict, model_name, fast_load)
        if not fast_load:
            flds = data_dict.keys()
            cols = data_dict.values()
            res = model.load(flds, [cols])
            state = 'cancel' if res.get('messages') else 'done'
        else:
            rec_id = data_dict.pop('.id', None)
            if rec_id:
                model.browse(rec_id).write(data_dict)
                res = [{'ids': rec_id}]
            else:
                new_rec = model.create(data_dict)
                self._set_xml_id(xmlid, new_rec.id, model_name)
                res = [{'ids': new_rec.id}]
            state = 'done'
        if state == 'cancel':
            _logger.warn(res)
        return res, state, xmlid

    @api.one
    def do_import(self):
        """ Load the data into the target model.

        The data field contains a list of the rows to import.
        Each line is a dictionary mapping fields to values.
        Lines should have a ``_model`` key to identify the target model.
        External IDs/XML IDs are supported.

        The loading uses the ORM load() method, so the data supports
        the same features as standard CSV file lading, such as External IDs.
        Alternatively, a simpler custom fast load is available, that bypasses
        load() and uses create() and write() directly.
        """
        raw_data = jsontext2object(self.data)
        res_data = [self._load_one(x, self.fast_load) for x in raw_data]
        res_state = min([state for log, state, xmlid in res_data])
        res_log = ', '.join([str(log) for log, state, xmlid in res_data])
        res_xmlid = ', '.join([xmlid or '' for log, state, xmlid in res_data])
        _logger.debug(
            'Imported %s with result state %s.' % (res_xmlid, res_state))
        return self.write(
            {'state': res_state, 'log': res_log, 'xmlid': res_xmlid})

    @api.model
    def create(self, values):
        """
        On new record creation, execute the corresponding data import
        if the state is 'open' or empty.
        The ``data`` field is expected to have a list of dictionaries.
        """
        rec = super(ImportLoader, self).create(values)
        if rec.state == 'open':
            rec.do_import()
        return rec

    @api.model
    def do_cron_import(self):
        """ Finds all pending 'wait' import documents and imports them. """
        to_import = self.search([('state', '=', 'wait')])
        if not len(to_import):
            return False
        _logger.info('Loading %s records.' % len(to_import))
        for rec in to_import:
            try:
                rec.do_import()
            except Exception, e:
                _logger.error(e)
                rec.write({'state': 'cancel', 'log': e})
            self.env.cr.commit()
        _logger.debug('Import finished.')
        return True
