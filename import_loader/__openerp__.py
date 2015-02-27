# -*- coding: utf-8 -*-
##############################################################################
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
    'name': 'Import Loader',
    'summary': 'Use the create() method as a proxy for load()',
    'version': '3.0',
    'category': 'Tools',
    'author': 'Daniel Reis',
    'website': 'https://github.com/dreispt/odoo-addons',
    'depends': ['base'],
    'data': ['import_loader_data.xml'],
    'test': ['import_loader_test.yml'],
    'installable': True,
}
