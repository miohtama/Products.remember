import unittest

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False
from zope.component import getAdapter

from zope.app.annotation.interfaces import IAnnotations

from Products.remember.interfaces import IHashPW
from Products.remember.Extensions.migrations \
    import migrate_bcrypt_password_storage
from Products.remember.config import ANNOT_KEY
from Products.remember.config import HASHERS

from base import RememberTestBase
from base import RememberProfileLayer
from base import mem_data

class TestMigration(RememberTestBase):
    """
    test migration functionality for remember
    """

    def testMigrateBcryptSalts(self):
        """
        test that migrating removes the 'member_salt' attribute
        and moves it to the annotation
        """
        member = self.portal_member
        hasher = getAdapter(member, IHashPW, 'bcrypt')
        if not hasher.isAvailable():
            return

        annot = IAnnotations(member)
        salt_str = annot[ANNOT_KEY].pop('bcrypt_salt')
        member.member_salt = salt_str

        password = member.getPassword()
        htype, hashed = password.split(':', 1)
        self.failUnless(htype in HASHERS)
        member.getField('password').set(member, hashed)

        login = member.getUserName()
        credentials = {'login': login,
                       'password': mem_data[member.getId()]['password']}

        self.assertRaises(ValueError, member.verifyCredentials, credentials)
        migrate_bcrypt_password_storage(self.portal)
        self.failUnless(member.verifyCredentials(credentials))

        self.assertEqual(salt_str, annot[ANNOT_KEY]['bcrypt_salt'])

        

def test_suite():
    suite = unittest.TestSuite()
    if HAS_BCRYPT:
        suite.addTest(unittest.makeSuite(TestMigration))
    return suite