# -*- coding: utf-8 -*-
##############################################################################
#
#    Daniel Reis
#    2011
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

#import pdb
import os
import logging
import sys
import datetime
from osv import fields, osv

CONNECTORS = []
try:
    import pyodbc
    CONNECTORS.append( ('pyodbc', 'ODBC') )
except:
    logging.getLogger('Import ODBC').info('ODBC libraries not available. Please install "unixodbc" and "python-pyodbc" packages.')

try:
    import cx_Oracle
    CONNECTORS.append( ('cx_Oracle', 'Oracle') )
except:
    logging.getLogger('Import ODBC').info('Oracle libraries not available. Please install "cx_Oracle" python package.')

 
class import_odbc_dbsource(osv.osv):
    _name="import.odbc.dbsource"
    _description = 'Import Database Source'
    _columns = {
        'name': fields.char('Datasource name', required=True, size=64),
        'conn_string': fields.text('Connection string'),
        'password': fields.char('Password' , size=40),
        'dbtable_ids': fields.one2many('import.odbc.dbtable', 'dbsource_id', 'Import tables'),
        'connector': fields.selection(CONNECTORS, 'Connector', required=True),
    }

    #Run all imports
        #Open connection
        #Get all tables to import
        #For each table, run table import (dbtable model)
        #Close connection
        
    def conn_open(self, cr, uid, id1):
        #Get dbsoource record
        data = self.browse(cr, uid, id1)
        #Build the full connection string
        connStr = data.conn_string
        if data.password:
            if '%s' not in data.conn_string:
                connStr += ';PWD=%s'
            connStr = connStr % data.password
        #Try to connect
        if data.connector == 'cx_Oracle':
            os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'
            conn = cx_Oracle.connect(connStr)
        else:
            conn = pyodbc.connect(connStr)
        #If no exception raise, return ok
        return conn


    def connection_test(self, cr, uid, ids, context=None):
        #Perform the test for each selected "dbsource"
        data = self.browse(cr, uid, ids)
        for obj in data:
            #pdb.set_trace()
            conn = self.conn_open(cr, uid, obj.id)
            conn.close()            
        #If no exception raise, return ok
        return True
    
    def import_run(self, cr, uid, ids, context=None):
        #Prepare objects to be used
        table_obj = self.pool.get('import.odbc.dbtable')
        #Import each selected dbsource
        data = self.browse(cr, uid, ids)
        for obj in data:
            #Get list of tables
            table_ids = [x.id for x in obj.dbtable_ids]
            #Run import
            table_obj.import_run( cr, uid, table_ids)
        return True
    
import_odbc_dbsource()


class import_odbc_dbtable(osv.osv):
    _name="import.odbc.dbtable"
    _description = 'Import Table Data'
    _order = 'exec_order'
    _columns = {
        'name': fields.char('Datasource name', required=True, size=64),
        'enabled': fields.boolean('Execution enabled'),
        'dbsource_id': fields.many2one('import.odbc.dbsource', 'Database source', required=True),
        'sql_source': fields.text('SQL', required=True, help='Column names must be valid "import_data" columns.'),
        'model_target': fields.many2one('ir.model','Target object'),
        'noupdate': fields.boolean('No updates', help="Only create new records; disable updates to existing records."),
        'exec_order': fields.integer('Execution order', help="Defines the order to perform the import"),
        'last_sync': fields.datetime('Last sync date', help="Datetime for the last succesfull sync. Later changes on the source may not be replicated on the destination"),
        'last_run': fields.datetime('Last run', readonly=True),
        'last_record_count': fields.integer('Last record count', readonly=True),
        'last_error_count': fields.integer('Last error count', readonly=True),
        'last_log': fields.text('Last run log', readonly=True),
    }
    _defaults = {
        'enabled': True,
        'exec_order': 10,
        ###'last_sync': datetime.datetime(1900,1,1,0,0,0)
    }

    def import_run(self, cr, uid, ids=None, context=None):
        #Prepare support objects
        dbsource_obj = self.pool.get('import.odbc.dbsource')
        logger = logging.getLogger('Import ODBC')
        logger.debug('Starting import run...')

        #Build id list, if none is provided
        if not ids:
            ids = self.search(cr, uid, [('enabled', '=', True)])
        
        #Consider each dbtable:
        data = self.browse(cr, uid, ids)
        for obj in data:
            #Now without seconds (avoid problems with SQL smalldate)
            dt_now = datetime.datetime.now()
            dt_now = dt_now.replace(second=0, microsecond=0)
            #Prepare log to write
            log = { 
                'last_run': dt_now,
                'last_record_count': 0,
                'last_error_count': 0,
                'last_log': ''
                }
                
            #Skip if it's inactive
            if not obj.enabled or not obj.sql_source:
                log['last_log'] = 'Pass.'

            #Import table, if it's active
            else:
                #Prepare SQL sentence; replace every "?" with the last_sync date
                sql = obj.sql_source
                dt  = obj.last_sync
                params = tuple( [dt] * sql.count('?') )
                #Open source connection
                conn = dbsource_obj.conn_open(cr, uid, obj.dbsource_id.id)
                #Get source data cursor
                db_cursor = conn.cursor()
                db_cursor.execute(sql, params)
                #Build column list from cursor, and add an extra "xml_id" column
                cols = [x[0] for x in db_cursor.description]
                cols.append("id")
                
                #Get destination object
                model = obj.model_target.model
                model_obj = self.pool.get(model)
                #Setup prefix to use in xml_ids 
                xml_prefix = model.replace('.', '_') + "_id_"
                
                #Import each row:
                for row in db_cursor:
                    #Build data row
                    datarow = []
                    for col in row:
                        if type(col) == str:
                            ###OLD: datarow.append(col.decode('iso-8859-1').encode('utf-8').strip() )
                            datarow.append( col.strip() )
                        else:
                            datarow.append( str(col) )
                    #Add "xml_id" column to row
                    datarow.append( xml_prefix + datarow[0] )
                    
                    #Import the row; on error, write line to the log
                    log['last_record_count'] += 1
                    try:
                        #print datarow, 'NLS_LANG=', os.environ['NLS_LANG'] ###
                        model_obj.import_data(cr, uid, cols, [datarow], noupdate=obj.noupdate)
                        #logger.debug('...OK %s' % ([datarow]) ) 
                    except:
                        logger.warn('%s =>\t%s' % (str(sys.exc_info()[1]), datarow) )
                        log['last_log'] += '\n%s: %s' % (datarow[-1], str(sys.exc_info()[1]) )
                        log['last_error_count'] += 1
                    #Inform progress on long Imports, every 100 rows
                    if log['last_record_count'] % 100 == 0:
                        logger.info('...%s rows processed...' % (log['last_record_count']) )
                    
                #Finished importing all rows
                logger.info('Imported %s , %s rows, %s errors' % (model, log['last_record_count'], log['last_error_count'] ) )
                #Close the connection
                conn.close()
                #If no errors, write new sysnc date
                if log['last_error_count'] == 0:
                    log['last_sync'] = log['last_run']
                    log['last_log'] += 'Done.'
                
            #Write run log, either if the table import is active or inactive
            self.write(cr, uid, [obj.id], log)

        #Finished
        return True

    def import_schedule(self, cr, uid, ids, context=None):
        cron_obj = self.pool.get('ir.cron')
        new_create_id = cron_obj.create(cr, uid, {
            'name': 'Import ODBC tables',
            'interval_type': 'hours',
            'interval_number': 1, 
            'numbercall': -1,
            'model': 'import.odbc.dbtable',
            'function': 'import_run', 
            'doall': False,
            'active': True
            })
        return {
            'name': 'Import ODBC tables',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'ir.cron',
            'res_id': new_create_id,
            'type': 'ir.actions.act_window',
            }
        
import_odbc_dbtable()
