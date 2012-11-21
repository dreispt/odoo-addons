# -*- coding: utf-8 -*-
##############################################################################
#
#    Daniel Reis, 2012
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

from osv import fields, osv
import logging
_logger = logging.getLogger(__name__)

class import_sqlpush(osv.osv):
    _name="import.sqlpush"
    _description = 'Import Data Pushed by SQL'
    _columns = {
        'model': fields.char('Model', size=40, required=True),
        'data': fields.text('Data', required=True),
        'noupdate': fields.integer('No updates'),
        'key_ref': fields.char('Key Reference', size=100, select=1,
            help='Can be used to help the origin app to later track the outcome of the import operation.'),
        'state': fields.selection( [('draft', 'New'), ('cancel', 'Failed'), ('done','Done')], 
                                   'State', select=1), #Indexed for faster queries
        'log': fields.text('Execution Log'),
    }
    _defaults = {
        'state': 'draft',
    }

    def _install_init(self, cr, uid, ids=None, context=None):
        """Set default values on columns, to solve the fact that SQL INSERTs bypass the ORM"""
        cr.execute("ALTER TABLE ONLY import_sqlpush ALTER COLUMN state       SET DEFAULT 'draft'")
        cr.execute("ALTER TABLE ONLY import_sqlpush ALTER COLUMN create_uid  SET DEFAULT 1")
        cr.execute("ALTER TABLE ONLY import_sqlpush ALTER COLUMN create_date SET DEFAULT timezone('UTC'::text, now())")
        return  True
        
    def do_import_data(self, cr, uid, ids=None, context=None):
        """Do the import for all outstanding rows. Called by the scheduled job.
        'data' should use \n - char(10) as line separator and \t - char(9) as column separator.  
        """
        #PSQL EXAMPLE: INSERT INTO import_sqlpush (model, data) VALUES ('res.partner', E'id\tref\tname\tcomment\nres_partner_PUSHME\tPUSHME\tPushed Customer\tThis is a test')
        def end_of_batch(ok_ids):
            """Update imported records state and report progress on log"""
            _logger.info('%s imported.' % len(ok_ids))
            self.write(cr, uid, ok_ids, {'state': 'done', 'log': None})
            cr.commit() 
            ok_ids = []
            
        #_logger.info('Starting...')
        batch_size = 100
        ids     = self.search(cr, uid, [('state','=','draft')])
        ok_ids  = []
        errs    = 0
        for r in self.browse(cr, uid, ids, context=context):
            try:
                log = "get model"
                model  = self.pool.get(r.model)
                log = "get items"
                lines = [x.split('\t') for x in r.data.split('\n')]
                assert len(lines) > 1, "Data must have at least a header and a data row"
                assert len(lines[0]) == len(lines[1]), "Header and rows must have same number of cols"
                log = "try import"
                res = model.import_data(cr, uid, lines[0], lines[1:], noupdate=r.noupdate)
                ok_ids.append(r.id)
            except Exception, e:
                errs += 1
                self.write(cr, uid, [r.id], {'state': 'cancel', 'log': 'On %s: %s' % (log, e) })
            if len(ok_ids) % batch_size == 0:
                end_of_batch(ok_ids)
        if ok_ids:
            end_of_batch(ok_ids)
        if errs:
            _logger.warn('%s errors found. See the SQLPush table for details.' % errs)
        return True
    
    def do_purge(self, cr, uid, ids=None, lag=7, context=None):
        """Delete executed records older than 'lag' days"""
        cr.execute("DELETE FROM import_sqlpush WHERE state<>'draft' AND write_date < now() - interval '%d' day" % lag)
        return True
    
import_sqlpush()
