# -*- coding: utf-8 -*-
##############################################################################
#
#   Daniel Reis, 2013
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Base Action Dialog',
    'version': '1.0',
    "category": "Tools",
    'description': """
Allows for Automated Actions to raise error messages, making it possible
for them to perform validations.

In the Automated Action configure the conditions that should trigger an error.
Then use a Server Action action with Python Code, using the
``base,action.dialog`` model, with this code::

    self.error(cr, uid, 0, u'My error message.', u'My Title')

""",
    'author': 'Daniel Reis',
    'depends': ['base'],
    'data': ['security/ir.model.access.csv'],
    'installable': True,
}
