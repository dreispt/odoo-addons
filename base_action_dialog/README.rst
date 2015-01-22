Allows for Automated Actions to raise error messages, making it possible
for them to perform validations.

In the Automated Action configure the conditions that should trigger an error.
Then use a Server Action action with Python Code, using the
``base,action.dialog`` model, with this code::

    self.error(cr, uid, 0, u'My error message.', u'My Title')
