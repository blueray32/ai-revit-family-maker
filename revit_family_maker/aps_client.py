"""
APS (Autodesk Platform Services) Client
Handles authentication and Design Automation API interactions
"""

import asyncio
import time
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


@dataclass
class APSToken:
    """APS OAuth token"""

    access_token: str
    expires_at: float
    token_type: str = "Bearer"

    @property
    def is_expired(self) -> bool:
        """Check if token is expired (with 5-minute buffer)"""
        return time.time() >= (self.expires_at - 300)


class APSClient:
    """Client for APS Design Automation API"""

    def __init__(self, client_id: str, client_secret: str, region: str = "us-east"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.base_url = "https://developer.api.autodesk.com"
        self.da_base = f"{self.base_url}/da/{region}/v3"
        self._token: Optional[APSToken] = None

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def authenticate(self) -> APSToken:
        """Get 2-legged OAuth token with automatic retry"""
        if self._token and not self._token.is_expired:
            return self._token

        url = f"{self.base_url}/authentication/v2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "code:all",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, data=data)
            response.raise_for_status()
            result = response.json()

            expires_at = time.time() + result.get("expires_in", 3600)
            self._token = APSToken(
                access_token=result["access_token"],
                expires_at=expires_at,
                token_type=result.get("token_type", "Bearer"),
            )

            print(f"✅ APS authenticated, token expires in {result.get('expires_in', 3600)}s")
            return self._token

    def _headers(self, token: APSToken) -> Dict[str, str]:
        """Get HTTP headers with bearer token"""
        return {
            "Authorization": f"{token.token_type} {token.access_token}",
            "Content-Type": "application/json",
        }

    async def create_workitem(
        self,
        activity_id: str,
        arguments: Dict[str, Dict],
        timeout: int = 600,
    ) -> Dict:
        """
        Create and submit a Design Automation WorkItem

        Args:
            activity_id: Fully qualified activity ID (e.g., "nickname.ActivityName+alias")
            arguments: WorkItem arguments (inputs/outputs)
            timeout: Max execution time in seconds (default: 600 = 10 minutes)

        Returns:
            WorkItem response with job ID and status

        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        token = await self.authenticate()

        workitem = {
            "activityId": activity_id,
            "arguments": arguments,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.da_base}/workitems",
                headers=self._headers(token),
                json=workitem,
            )
            response.raise_for_status()
            result = response.json()

            print(f"✅ WorkItem created: {result['id']}")
            return result

    @retry(
        retry=retry_if_exception_type(httpx.RequestError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
    )
    async def get_workitem_status(self, workitem_id: str) -> Dict:
        """
        Get WorkItem status

        Args:
            workitem_id: WorkItem ID

        Returns:
            WorkItem status response
        """
        token = await self.authenticate()

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.da_base}/workitems/{workitem_id}",
                headers=self._headers(token),
            )
            response.raise_for_status()
            return response.json()

    async def poll_workitem(
        self,
        workitem_id: str,
        max_wait: int = 600,
        poll_interval: int = 5,
    ) -> Dict:
        """
        Poll WorkItem until completion or timeout

        Args:
            workitem_id: WorkItem ID
            max_wait: Maximum wait time in seconds
            poll_interval: Seconds between polls

        Returns:
            Final WorkItem status

        Raises:
            TimeoutError: If WorkItem doesn't complete in time
            RuntimeError: If WorkItem fails
        """
        start_time = time.time()
        last_status = None

        while time.time() - start_time < max_wait:
            status = await self.get_workitem_status(workitem_id)
            current_status = status.get("status")

            # Print status updates
            if current_status != last_status:
                print(f"📊 WorkItem status: {current_status}")
                last_status = current_status

            if current_status == "success":
                print("✅ WorkItem completed successfully")
                return status
            elif current_status == "failedInstructions":
                error_msg = f"WorkItem failed: {status.get('reportUrl', 'No report')}"
                print(f"❌ {error_msg}")
                raise RuntimeError(error_msg)
            elif current_status == "cancelled":
                raise RuntimeError("WorkItem was cancelled")

            # Still processing
            await asyncio.sleep(poll_interval)

        raise TimeoutError(f"WorkItem did not complete within {max_wait} seconds")

    async def download_file(self, url: str) -> bytes:
        """
        Download file from signed URL

        Args:
            url: Signed URL (from WorkItem output)

        Returns:
            File contents as bytes
        """
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content

    async def upload_file(self, url: str, content: bytes) -> None:
        """
        Upload file to signed URL

        Args:
            url: Signed URL (from OSS or WorkItem input)
            content: File contents as bytes
        """
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.put(
                url,
                content=content,
                headers={"Content-Type": "application/octet-stream"},
            )
            response.raise_for_status()

    async def get_signed_url(
        self,
        bucket_key: str,
        object_key: str,
        access: str = "read",
        expires_in: int = 3600,
    ) -> str:
        """
        Get signed URL for OSS object

        Args:
            bucket_key: OSS bucket key
            object_key: Object key within bucket
            access: Access type ("read" or "write")
            expires_in: URL expiration in seconds

        Returns:
            Signed URL
        """
        token = await self.authenticate()

        url = f"{self.base_url}/oss/v2/buckets/{bucket_key}/objects/{object_key}/signed"
        params = {"access": access}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers=self._headers(token),
                params=params,
            )
            response.raise_for_status()
            result = response.json()
            return result["signedUrl"]

    async def create_workitem_and_wait(
        self,
        activity_id: str,
        arguments: Dict[str, Dict],
        max_wait: int = 600,
    ) -> Tuple[Dict, Dict[str, bytes]]:
        """
        Convenience method: create WorkItem, wait for completion, download outputs

        Args:
            activity_id: Activity ID
            arguments: WorkItem arguments
            max_wait: Max wait time in seconds

        Returns:
            Tuple of (final_status, downloaded_files)
            where downloaded_files is dict of {output_name: file_content}
        """
        # Create WorkItem
        workitem = await self.create_workitem(activity_id, arguments)
        workitem_id = workitem["id"]

        # Poll until complete
        final_status = await self.poll_workitem(workitem_id, max_wait)

        # Download outputs
        outputs = {}
        for output_name, output_info in final_status.get("arguments", {}).items():
            if isinstance(output_info, dict) and "url" in output_info:
                print(f"📥 Downloading {output_name}...")
                content = await self.download_file(output_info["url"])
                outputs[output_name] = content
                print(f"✅ Downloaded {output_name} ({len(content)} bytes)")

        return final_status, outputs


# Singleton client instance
_aps_client: Optional[APSClient] = None


def get_aps_client(client_id: str, client_secret: str, region: str = "us-east") -> APSClient:
    """Get or create singleton APS client"""
    global _aps_client
    if _aps_client is None or _aps_client.client_id != client_id:
        _aps_client = APSClient(client_id, client_secret, region)
    return _aps_client
