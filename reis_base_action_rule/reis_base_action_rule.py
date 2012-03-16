# -*- coding: utf-8 -*-
##############################################################################
#    Daniel Reis
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
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

import time
import pooler
import tools
from tools.translate import _
from tools.safe_eval import safe_eval
from osv import fields, osv

import logging
_logger = logging.getLogger(__name__)

###############################################################################
# Base Action Rule
# (extends base_action_rule.py and crm_action_rule.py)
#
#   * format_mail() allows using additional fields in the email body:
#        ref, using %(object_ref)s
#        translated state name, using %(object_state)s
#        uppercase translated state name, using %(object_STATE)s
#   * email_send() allows a custom subject line, that should be provided 
#     in the first line of the "body", using the prefix "Subject:".
#
###############################################################################

class base_action_rule(osv.osv):
    _inherit = 'base.action.rule'
    _columns = {
        'trg_evalexpr': fields.text('Evaluated expression',\
            help="""Python expression, able to use a "new" and "old" dictionaries, with the changed columns."""), 
        'email_template_id': fields.many2one('email.template', 'E-mail template',
            domain="[('model_id','=',model_id.id)]" ),
        'email_template_force': fields.boolean('Send immediately',
            help='If not checked, it will be sent the next time the e-mail scheduler runs.'),
    }

    def _create(self, old_create, model, context=None):
        """
        Return a wrapper around `old_create` calling both `old_create` and
        `post_action`, in that order.
        """
        def wrapper(cr, uid, vals, context=context):
            if context is None:
                context = {}
            #{reis: store new and old values in context, to be used in trigger expressions
            context['_action_old'] = {}
            context['_action_new'] = vals
            #print 'WRAPPER_CREATE: old= <NA> new=', vals.get('user_id')
            #print '\n= = = = = = = = = = \n....create ', vals
            #reis}
            new_id = old_create(cr, uid, vals, context=context)
            if not context.get('action'):
                self.post_action(cr, uid, [new_id], model, context=context)
            return new_id
        return wrapper
    
    def _write(self, old_write, model, context=None):
        """
        Return a wrapper around `old_write` calling both `old_write` and
        `post_action`, in that order.
        """
        def wrapper(cr, uid, ids, vals, context=context):
            if context is None:
               context = {}
            if isinstance(ids, (str, int, long)):
                ids = [ids]
            #{reis: store new and old values in context, to be used in trigger expressions
            olds = self.pool.get(model).read(cr, uid, ids, context=context)
            context['_action_old'] = olds
            context['_action_new'] = vals
            #print 'WRAPPER_WRITE: old= ', olds[0].get('user_id'), '; new=', vals.get('user_id')
            #import pdb; pdb.set_trace()
            #reis}
            old_write(cr, uid, ids, vals, context=context)
            if not context.get('action'):
                self.post_action(cr, uid, ids, model, context=context)
            return True
        return wrapper


    ###dreis extending base_action_rule.py:email_send
    #TODO: deprecated, use email_template instead
    def format_mail(self, obj, body):
        """ Format Mail """

        data = {
            'object_id': obj.id,
            'object_subject': hasattr(obj, 'name') and obj.name or '',
            'object_date': hasattr(obj, 'date') and obj.date or '',
            'object_description': hasattr(obj, 'description') and obj.description or '',
            'object_user': hasattr(obj, 'user_id') and (obj.user_id and obj.user_id.name) or '',
            'object_user_email': hasattr(obj, 'user_id') and (obj.user_id and \
                                     obj.user_id.user_email) or '',
            'object_user_phone': hasattr(obj, 'partner_address_id') and (obj.partner_address_id and \
                                     obj.partner_address_id.phone) or '',
            'partner': hasattr(obj, 'partner_id') and (obj.partner_id and obj.partner_id.name) or '',
            'partner_email': hasattr(obj, 'partner_address_id') and (obj.partner_address_id and\
                                         obj.partner_address_id.email) or '',
            #dreis: added
            'object_ref': hasattr(obj, 'ref') and obj.ref or '',  ###dreis
            'object_state': hasattr(obj, 'state') and obj.state and _(obj.state) or '',  ###dreis
            'object_STATE': hasattr(obj, 'state') and obj.state and _(obj.state).upper() or '',  ###dreis
            'object_project': hasattr(obj, 'project_id') and obj.project_id and obj.project_id.name or '',  ###dreis
            'object_categ': hasattr(obj, 'categ_id') and obj.categ_id and obj.categ_id.name or '',  ###dreis
            'object_department_ref': hasattr(obj, 'department_id') and obj.department_id and obj.department_id.ref or '',  ###dreis
            'object_partner_ref': hasattr(obj, 'partner_id') and (obj.partner_id and obj.partner_id.ref) or '',
        }
        return self.format_body(body % data)
        
    ###dreis extending crm_action_rule.py:email_send
    #TODO: deprecated, use email_template instead
    def email_send(self, cr, uid, obj, emails, body, emailfrom=tools.config.get('email_from', False), context=None):
        mail_message = self.pool.get('mail.message')
        body = self.format_mail(obj, body)
        if not emailfrom:
            if hasattr(obj, 'user_id')  and obj.user_id and obj.user_id.user_email:
                emailfrom = obj.user_id.user_email

        ###dreis: customizable Subject line, specified in the first line of the "body"
        # name = '[%d] %s' % (obj.id, tools.ustr(obj.name))
		#
        subject = body.splitlines()[0] #get first line of the body
        if subject.startswith('Subject:'): 
            name = subject.split(':', 1)[1].lstrip() #subject is text after ':'; strip leading spaces
            body = '\n'.join( body.splitlines()[1:] ) #body without the first line
        else:
            name = '[%d] %s' % (obj.id, tools.ustr(obj.name))
        ###dreis end
		
        emailfrom = tools.ustr(emailfrom)
        if hasattr(obj, 'section_id') and obj.section_id and obj.section_id.reply_to:
            reply_to = obj.section_id.reply_to
        else:
            reply_to = emailfrom
        if not emailfrom:
            raise osv.except_osv(_('Error!'), 
                    _("No E-Mail ID Found for your Company address!"))
        #rint "...email_send:", emails ###, name ###reis###
        return mail_message.schedule_with_attach(cr, uid, emailfrom, emails, name, body, model='base.action.rule', reply_to=reply_to, res_id=obj.id)

    #reis: 
    #Actions can be triggered from evaluated expression, using values from dictionaries 'old' and 'new'
    # new - is the dictionay passed to the create/write method, therefor it contains only the fields to write.
    # old - on create is an empty dict {} or None value; on write constains the values before the write is executed, given by the read() method
    #Examples:
    #   check if responsible changed to another person: not old and old['user_id']!=new['user_id']
    def do_check(self, cr, uid, action, obj, context={}):
        ok = super(base_action_rule, self).do_check(cr, uid, action, obj, context=context)
        if action.trg_evalexpr:
            old = None
            #Find in the list this obj's old 
            for x in context.get('_action_old', []):
                old = x.get('id') == obj.id and x
            #Convert tuples (id, name) into id only
            for x in old or []:
                if type(old[x]) == tuple:
                    old[x] = old[x][0]
            #Build dict with new and old and eval the expression
            eval_dict = {
                'old': old,
                'new': context.get('_action_new')}
            try:
                ok = safe_eval(action.trg_evalexpr, {}, eval_dict)
            except (ValueError, KeyError, TypeError):
                ok = False
            #Debug Log
            if ok: 
                _logger.debug('Activated rule %s on record id %d.' % (action.name, obj.id) )
                #print '********************************************************************'
                #print '\n==== Rule:', action.name, action.trg_evalexpr, '===='  '\n---- old:: ', eval_dict['old'], '\n---- new::', eval_dict['new'] 
        return ok

    #reis: 
    #Action able to send e-mails using email_template; 
    #Bonus: messages sent are recorded in the communication history.
    def do_action(self, cr, uid, action, model_obj, obj, context=None):
        super(base_action_rule, self).do_action(cr, uid, action, model_obj, obj, context=context)
        if action.email_template_id:
            mail_template = self.pool.get('email.template')
            mail_message = self.pool.get('mail.message')
            msg_id = mail_template.send_mail(cr, uid, action.email_template_id, obj.id, context=context)
            #mail_template does not set the e-mail date by itself!
            mail_message.write(cr, uid, [msg_id], {'date': time.strftime('%Y-%m-%d %H:%M:%S'),}, context=context)
            #send immediatly, if the option is checked
            if action.email_template_force:
                mail_message.send(cr, uid, [msg_id], context=context)
        return True

base_action_rule()

#Force register hooks on user Login, to not depend on scheduler
#BUG https://bugs.launchpad.net/openobject-addons/+bug/944197
class users(osv.osv):
    _inherit = "res.users"
    
    def login(self, db, login, password):
        #Perform login
        user_id = super(users, self).login(db, login, password)
        #Register hooks 
        cr = pooler.get_db(db).cursor()
        rule_pool = pooler.get_pool(db).get('base.action.rule')
        rule_ids = rule_pool.search(cr, 1, [])
        rule_pool._register_hook(cr, 1, rule_ids)
        rule_ids = None 
        cr.close()
        #End
        return user_id
users()
