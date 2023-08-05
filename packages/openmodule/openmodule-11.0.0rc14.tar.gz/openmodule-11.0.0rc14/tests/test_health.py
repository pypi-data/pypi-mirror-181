from unittest import TestCase

from openmodule.core import init_openmodule, shutdown_openmodule
from openmodule_test.health import HealthTestMixin


class HealthTestCase(HealthTestMixin, TestCase):
    topics = ["healthpong"]

    def setUp(self):
        super().setUp()
        self.core = init_openmodule(context=self.zmq_context(), config=self.zmq_config())
        self.addCleanup(shutdown_openmodule)
        self.wait_for_health()

    def tearDown(self):
        super().tearDown()

    def test_health_is_answering(self):
        health = self.get_health()
        self.assertEqual(health["pong"]["status"], "ok")

    def test_status_and_message(self):
        self.core.health.add_check("test", "Test", "for testing")
        self.core.health.add_check("test2", "Test2", "another for testing")
        health = self.get_health()
        self.assertEqual(health["pong"]["status"], "ok")
        self.core.health.check_fail("test2", message="error2")
        health = self.get_health()
        self.assertEqual(health["pong"]["status"], "error")
        self.assertEqual(health["pong"]["message"], "error2")
        self.core.health.check_success("test2")
        self.core.health.check_fail("test", message="error")
        health = self.get_health()
        self.assertEqual(health["pong"]["status"], "error")
        self.assertEqual(health["pong"]["message"], "error")
