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
#
#    Icon "Crystal Clear app ark2.png" courtesy of Everaldo Coelho:
#    http://commons.wikimedia.org/wiki/File:Crystal_Clear_app_ark2.png
#
##############################################################################

{
    'name': 'Import data pushed through SQL',
    'version': '1.2',
    'category': 'Tools',
    'description': """\
Import data pushed through SQL.
See: http://openerpmanagementsystem.blogspot.pt/2012/11/pushing-data-into-openerp.html

CHANGELOG:
1.1    
The "noupdate" column was removed. It's replaced by the new "options" columns,
allowing to signal multiple import options. An import option is activated if 
it's keyword text is found in the "option" column. 
Current supported keywords are "noupdate" and "unlink".
 
    """,
    'author':   'Daniel Reis',
    'website':  'http://openerpmanagementsystem.blogspot.pt/',
    'depends':  ['base'],
    'data':     ['import_sqlpush_data.xml',],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
