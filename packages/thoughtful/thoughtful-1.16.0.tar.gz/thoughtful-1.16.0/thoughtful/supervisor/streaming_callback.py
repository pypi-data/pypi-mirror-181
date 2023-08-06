from __future__ import annotations

import logging
from typing import Optional

from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Session

from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.reporting.step_report import StepReport

from thoughtful.supervisor.reporting.streaming_payloads import (  # isort:skip
    StepReportStreamingPayload,
    BotManifestStreamingPayload,
    StreamingPayload,
)

logger = logging.getLogger(__name__)


class StreamingCallback(Session):
    def __init__(self, run_id: str, callback_url: str, aws_auth: AWSRequestsAuth):
        super().__init__()
        self.run_id = run_id
        self.callback_url = callback_url
        self.auth = aws_auth

    @classmethod
    def from_env_defaults(
        cls, auth: AWSRequestsAuth, run_id: str, callback_url: str
    ) -> Optional[StreamingCallback]:
        if run_id and callback_url:
            return cls(run_id=run_id, callback_url=callback_url, aws_auth=auth)
        logger.warning("Missing job id or callback url values")

    def post(self, payload: StreamingPayload, **kwargs):
        logger.info(f"Posting to {self.callback_url} {payload}")
        try:
            response = super().post(
                self.callback_url, json=payload.__json__(), timeout=10, **kwargs
            )
            if not response.ok:
                logger.warning(
                    f"Invalid response {response.status_code}: {response.text}"
                )
            logger.info(f"Received {response.status_code}: {response.text}")
            return response
        except Exception:
            logger.exception("Could not post step payload to endpoint")

    def post_step_update(self, report: StepReport):
        return self.post(StepReportStreamingPayload(report, self.run_id))

    def post_manifest(self, manifest: Manifest):
        return self.post(BotManifestStreamingPayload(manifest, self.run_id))
