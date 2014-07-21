# -*- coding: utf-8 -*-
##############################################################################
#
#    Securitas Portugal SA, Daniel Reis, 2012 - 2013
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
    'version': '2.0',
    'category': 'Tools',
    'description': """\
In some data integrations scenarios, you have API access to the ORM, but
limited to the ``create()`` and ``write()`` methods.
It's the case for Pentaho PDI/Kettle and Talend Data Integration.


This module provides a workaround to import data using the ``load()`` method:
``create`` calls on the ``import-loader`` model fire ``load`` operations on
the desired models.

Note: this module evolved from ``import_sqlpush``, available for 6.1 and is
intended to be used as a replacement technique for it.
    """,
    'author':   'Daniel Reis',
    'website':  'http://openerpmanagementsystem.blogspot.pt/',
    'depends':  ['base'],
    'data':     ['import_loader_data.xml'],
    'installable': True,
}
