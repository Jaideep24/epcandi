import json

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase

from epcandiapp.models import AnalyticsEvent


class AdminLoginRateLimitTests(TestCase):
	def setUp(self):
		cache.clear()
		get_user_model().objects.create_superuser(
			username="admin",
			email="admin@example.com",
			password="StrongPass123!",
		)

	def test_admin_login_locked_after_five_failed_attempts(self):
		for _ in range(5):
			response = self.client.post(
				"/admin/login/",
				{"username": "admin", "password": "wrong-password"},
				REMOTE_ADDR="127.0.0.1",
			)
			self.assertIn(response.status_code, [200, 302])

		blocked = self.client.post(
			"/admin/login/",
			{"username": "admin", "password": "StrongPass123!"},
			REMOTE_ADDR="127.0.0.1",
		)
		self.assertEqual(blocked.status_code, 429)
		self.assertIn("Too many failed admin login attempts", blocked.content.decode("utf-8"))


class AnalyticsSecurityTests(TestCase):
	def setUp(self):
		cache.clear()

	def _post_event(self, payload):
		return self.client.post(
			"/api/track/",
			data=json.dumps(payload),
			content_type="application/json",
			REMOTE_ADDR="127.0.0.1",
		)

	def test_track_event_accepts_sql_injection_style_strings_safely(self):
		payload = {
			"user_id": "u_test_sql",
			"session_id": "s_test_sql",
			"event_type": "custom_event",
			"event_name": "search_query",
			"metadata": {
				"query": "' OR '1'='1; DROP TABLE users; --",
				"path": "/news/?q=' OR '1'='1",
			},
		}

		response = self._post_event(payload)
		self.assertEqual(response.status_code, 200)
		event = AnalyticsEvent.objects.latest("id")
		self.assertIn("DROP TABLE", event.metadata_json)

	def test_track_event_redacts_sensitive_and_keeps_xss_as_text(self):
		payload = {
			"user_id": "u_test_xss",
			"session_id": "s_test_xss",
			"event_type": "form_submit",
			"event_name": "contact_submit",
			"metadata": {
				"message": "<script>alert('xss')</script>",
				"password": "SuperSecret!",
				"email": "user@example.com",
			},
		}

		response = self._post_event(payload)
		self.assertEqual(response.status_code, 200)
		event = AnalyticsEvent.objects.latest("id")
		self.assertIn("<script>alert('xss')</script>", event.metadata_json)
		self.assertIn("\"password\":\"[redacted]\"", event.metadata_json)
		self.assertIn("\"email\":\"[redacted]\"", event.metadata_json)

	def test_track_event_rejects_unsupported_event_type(self):
		payload = {
			"user_id": "u_bad_event",
			"session_id": "s_bad_event",
			"event_type": "sql_injection",
		}
		response = self._post_event(payload)
		self.assertEqual(response.status_code, 400)
