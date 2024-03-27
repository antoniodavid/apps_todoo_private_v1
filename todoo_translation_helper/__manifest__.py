# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2020 Todooweb
#    (<http://www.todooweb.com>).
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
    'name': 'Tool Translation',
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Translate texts with the help of Google Translate.""",
    'description': """Translate texts and overwrite existing terms with the help of Google Translate.""",
    'license': 'AGPL-3',
    'author': "Todooweb (www.todooweb.com)",
    'website': "https://todooweb.com/",
    'contributors': [
        "Equipo Dev <devtodoo@gmail.com>",
        "Edgar Naranjo <edgarnaranjof@gmail.com>",
    ],
    'support': 'devtodoo@gmail.com',
    'depends': ['base', 'mail'],
    'external_dependencies': {'python': ['googletrans']},
    'data': [
        'security/ir.model.access.csv',
        'views/todoo_translation_helper.xml',
        'data/lang_data.xml',
    ],
    'images': ['static/description/translate_screenshot.png'],
    'live_test_url': 'https://cutt.ly/GRuk6Qu',
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 12.99,
    'currency': 'EUR',
}