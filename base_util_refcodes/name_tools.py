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

from openerp.osv import orm


def extended_name_get(obj, cr, uid, ids, name_mask, flds_templ, context=None):
    """
    Flexible name_get() method, able to replace the ORM's default.
    `name_mask`: the display template for the name. For example:
                    '[%(ref)s] %(name)s'
    `flds_templ`: the field names used in the template. Example:
                     ['ref', 'name']

    Usage example:

    from base_name_tools import name_tools
    def name_get(self, cr, uid, ids, context=None):
        return name_tools.extended_name_get(self, cr, uid, ids,
           '[%(ref)s] %(name)s', ['ref', 'name'], context=context)
    """
    if not ids:
        return []
    if not name_mask:
        return super(orm.Model, obj).name_get(cr, uid, ids, context=context)
    # Ensure ids is a list, so that read() also returns a list
    if not isinstance(ids, list):
        ids = [ids]
    flds_templ = list(set(flds_templ + [obj._rec_name]))
    res = []
    for rec in obj.read(cr, uid, ids, flds_templ, context=context):
        for key in flds_templ:
            if isinstance(rec[key], tuple):
                # Tuple values (id, name) are replaced by the name
                rec[key] = rec[key][1]
            if not rec[key]:
                del rec[key]
        try:
            n = name_mask % rec
        except:
            n = rec[obj._rec_name]  # fallback to default name
        res.append((rec['id'], n))
    return res


def extended_name_search(obj, cr, user, name='', args=None, operator='ilike',
                         context=None, limit=100, keys=None):
    """
    Flexible name_search() method, able to replace the ORM's default.
    Just set `keys` to the list of fields you want to be searched.

    Usage example:
    from base_name_tools import name_tools
    def name_search(self, cr, user, name='', args=None, operator='ilike',
        context=None, limit=100):
            return name_tools.extended_name_search(self, cr, user, name, args,
               operator, context=context, limit=limit,
               keys=['ref','name']) #<=edit list of fields to search
    """
    args = args or []
    keys = keys or [name]
    if name:
        for key in keys:
            ids = obj.search(cr, user, [(key, operator, name)] + args,
                             limit=limit, context=context)
            if len(ids):
                break  # Exit loop on first results
    else:
        ids = obj.search(cr, user, args, limit=limit, context=context)
    result = obj.name_get(cr, user, ids, context=context)
    return result
