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

    ```
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
    ```
