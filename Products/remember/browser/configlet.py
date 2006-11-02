from zope.interface import Interface
from zope import schema
from zope.formlib import form
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
_  = MessageFactory('remember')

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
try: from Products.Five.formlib.formbase import PageForm
except ImportError: from zope.formlib.form import PageForm

from Products.remember.utils import getAdderUtility
from Products.remember.config import DEFAULT_MEMBER_TYPE


class IRememberConfiglet(Interface):
    default_mem_type = schema.Choice(
        title=_(u'Default Member Type'),
        description=_(u'This specifies which remember-based member '
                      u'type will be added by default when someone '
                      u'joins the site.'),
        required=True,
        vocabulary='RememberTypes',
        default=_(unicode(DEFAULT_MEMBER_TYPE)),
        )


class RememberConfiglet(PageForm):
    """
    The formlib class for the remember config page.
    """
    template = ZopeTwoPageTemplateFile('configletform.pt')

    form_fields = form.FormFields(IRememberConfiglet)

    @form.action("submit")
    def action_submit(self, action, data):
        adder = getAdderUtility(self.context)
        adder.default_member_type = data['default_mem_type']