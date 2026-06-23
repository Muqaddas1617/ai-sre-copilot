import os
import sys
import unittest

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend import app as backend_app


class BackendAppTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(backend_app.app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_analyze_redacts_sensitive_values(self):
        response = self.client.post(
            "/analyze",
            json={"text": "Deploy database changes to prod with password=supersecret and token=abc123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("supersecret", response.json()["input"])
        self.assertNotIn("abc123", response.json()["input"])


if __name__ == "__main__":
    unittest.main()
