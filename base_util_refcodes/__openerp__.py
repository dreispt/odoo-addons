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
{
    'name': 'Configurable model name_get() descriptions',
    'version': '1.2',
    "category": "Tools",
    'description': """\
Configurable model name_get() descriptions.
Provides reusable python methods that simplify custom object name rendering:

Methods provided:
-----------------
name_tools.extended_name_get():
    Given a template mask and a list of fields names, render the name_get().
    All fields need to have value for the template to be applied.
    If not, uses the default name_ger (e.g. _rec_name)

name_tools.name_search():
    Performs the search on a given list of fields.

Usage example:
--------------
    from base_name_tools import name_tools

    def name_get(self, cr, uid, ids, context=None):
        return name_tools.extended_name_get(self, cr, uid, ids,
            '[%(ref)s] %(name)s', ['ref', 'name'], context=context)
        #   ^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^
        #       template mask       field list

    def name_search(self, cr, user, name='', args=None, operator='ilike',
        context=None, limit=100):
        return name_tools.extended_name_search(self, cr, user, name, args,
            operator, context=context, limit=limit, keys=['ref', 'name'])
        #                                           ^^^^^^^^^^^^^^^^^^^^
        #                                           field list to search
    """,
    'author': 'Daniel Reis',
    'depends': ['base'],
    'images': [
        'images/refcode_hr_demo.png',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
