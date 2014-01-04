from django.test.client import RequestFactory

from libs.utils.log import audit_log, Actions
from apps.main.models import AuditLog
from test_base import TestBase


class TestAuditLog(TestBase):
    def test_audit_log_call(self):
        account_user = self._create_user("alice", "alice")
        self._create_user_and_login("bob", "bob")
        request = RequestFactory().get("/")
        # create a log
        audit = {}
        audit_log(Actions.FORM_PUBLISHED, self.user, account_user,
                  "Form published", audit, request)
        # function should just run without exception so we are good at this
        # point query for this log entry
        sort = {"created_on": -1}
        cursor = AuditLog.query_mongo(
            account_user.username, None, None, sort, 0, 1)
        record = cursor.next()
        self.assertEqual(record['account'], "alice")
        self.assertEqual(record['user'], "bob")
        self.assertEqual(record['action'], Actions.FORM_PUBLISHED)
