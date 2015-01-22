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
    'name': 'Project Task for Employees',
    'summary': 'Handle employee related Tasks',
    'version': '1.0',
    'category': 'Human Resources',
    'author': 'Hugo Santos',
    'depends': [
        'project_employee_base',
        ],
    'data': [
        'project_task_hr.xml',
        ],
    'installable': True,
}
