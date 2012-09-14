# -*- coding: utf-8 -*-
##############################################################################
#
#    Daniel Reis, 2011
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

from osv import osv


def extended_name_get(ormobj, cr, uid, ids, name_mask, flds_templ, context=None):
#Usage example :
#    from base_name_tools import name_tools
#    def name_get(self, cr, uid, ids, context=None):
#        return name_tools.extended_name_get(self, cr, uid, ids, '[%(ref)s] %(name)s', ['ref', 'name'], context=context)
    flds = set(['id', ormobj._rec_name] + flds_templ)
    if ids and name_mask:
        res = list()
        for rec in ormobj.read(cr, uid, ids, flds, context=context):
            cols = dict()
            for key in rec:
                if key == ormobj._rec_name or rec[key]: 
                    #normalize (id, name) tuples
                    cols[key] =  isinstance(rec[key], tuple) and rec[key][1] or rec[key]
            if len(cols) < len(flds):
                n = rec[ormobj._rec_name]
            else:
                try:
                    n = name_mask % cols
                except:
                    n = '<name_get failed!>'
            res.append( (rec['id'], n) ) 
    else:
        res = super(osv.osv, ormobj).name_get(cr, uid, ids, context=context)
    return res


def extended_name_search(ormobj, cr, user, name='', args=None, operator='ilike', context=None, limit=100, keys=None):
#Usage example:
#    from base_name_tools import name_tools
#    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
#            return name_tools.extended_name_search(self, cr, user, name, args, operator, context=context, limit=limit, 
#                                keys=['ref','name']) #<=edit list of fields to search
#
    if not args:
        args = list()
    if not keys:
        keys = [name]
    if name:
        for key in keys:
            ids = ormobj.search(cr, user, [(key, operator, name)]+ args, limit=limit, context=context)
            if len(ids): break #Exit loop on first results
    else:
        ids = ormobj.search(cr, user, args, limit=limit, context=context)
    result = ormobj.name_get(cr, user, ids, context=context)
    return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


