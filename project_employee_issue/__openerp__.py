# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Hugo Santos
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
    'name': 'Project Issues for Employees',
    'summary': 'Handle employee related service requests',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """\
Allow to related project Issues to Employees.
With this you can handle HR service desk requests, such as requests to
change personal data or payroll related complains.""",
    'author': 'Hugo Santos',
    'depends': [
        'project_employee_base',
        'project_issue',
        ],
    'data': [
        'project_issue_hr.xml',
        ],
    'installable': True,
}
