# -*- coding: utf-8 -*-
{
    'name': 'Securitas Service Management Customizations',
    'version': '8.0',
    "category": "Project Management",
    'description': """
Customization for Securitas implementation.
""",
    'author': 'Daniel Reis',
    'data': [
        'project_task_view.xml',
        'project_task_sameloc_view.xml',
        'securitas_menu.xml',
    ],
    'depends': [
        'project',
        'project_task_department',
        'service_desk',
    ],
    'installable': True,
    'application': True,
}
