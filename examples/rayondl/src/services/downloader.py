"""
Rayon Presentation Downloader Service
Downloads PDFs directly via GraphQL API with Cognito authentication.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from pycognito import Cognito

COGNITO_USER_POOL_ID = "eu-west-1_vvlteusJn"
COGNITO_CLIENT_ID = "4fefc7faiinhvc4sj6pns12ram"
GRAPHQL_ENDPOINT = "https://graphql.rayon.design/graphql"


class RayonError(Exception):
    """Base exception for Rayon API errors."""


class NoPresentationError(RayonError):
    """Raised when model has no presentation/PDF available."""


@dataclass
class Model:
    id: str
    presentation_url: str
    created_at: str

    @property
    def folder_name(self) -> str:
        """Extract folder ID from URL (first UUID in path)."""
        # URL: https://models.rayon.design/{folder_id}/0/presentations/{file_id}.pdf
        parts = self.presentation_url.split("/")
        for part in parts:
            if len(part) == 36 and part.count("-") == 4:
                return part
        return self.id

    @property
    def filename(self) -> str:
        """Extract filename from URL (last part, without query params)."""
        path = self.presentation_url.split("?")[0]  # Remove query params
        return path.split("/")[-1]


@dataclass
class RayonClient:
    """Client for interacting with the Rayon API."""

    email: str
    password: str
    _cognito: Cognito = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        self._cognito = Cognito(
            user_pool_id=COGNITO_USER_POOL_ID,
            client_id=COGNITO_CLIENT_ID,
            username=self.email,
        )

    def _ensure_auth(self) -> None:
        """Ensure the client is authenticated, renewing token if needed."""
        if not self._cognito.access_token:
            self._cognito.authenticate(password=self.password)
            return

        try:
            self._cognito.renew_access_token()
        except Exception:
            self._cognito.authenticate(password=self.password)

    @property
    def access_token(self) -> str:
        """Get a valid access token, authenticating if necessary."""
        self._ensure_auth()
        return self._cognito.access_token

    def _gql(self, operation: str, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query against the Rayon API."""
        response = httpx.post(
            GRAPHQL_ENDPOINT,
            headers={
                "content-type": "application/json",
                "authorization": self.access_token,
                "x-amz-user-agent": "aws-amplify/3.0.7",
                "Origin": "https://www.rayon.design",
            },
            json={
                "operationName": operation,
                "variables": variables or {},
                "query": query,
            },
        )
        return response.json()

    def get_model(self, model_id: str) -> Model:
        """Fetch model presentation information by ID."""
        query = """
            query GetModelPresentationVersionUri($modelId: ID!) {
                getModelPresentationUri(modelId: $modelId) {
                    url
                    createdAt
                }
            }
        """
        data = self._gql("GetModelPresentationVersionUri", query, {"modelId": model_id})

        if errors := data.get("errors"):
            error = errors[0]
            error_type = error.get("errorType", "Error")
            message = error.get("message", "Unknown error")
            raise RayonError(f"{error_type}: {message}")

        presentation = data.get("data", {}).get("getModelPresentationUri")
        if not presentation or not presentation.get("url"):
            raise NoPresentationError(f"No presentation available for model {model_id}")

        return Model(
            id=model_id,
            presentation_url=presentation["url"],
            created_at=presentation["createdAt"],
        )

    def download(
        self,
        model: Model,
        output_dir: Path | str = ".",
        on_progress: "Callable[[int, int], None] | None" = None,
    ) -> Path:
        """Download model presentation PDF to the specified directory.

        Args:
            model: The model to download
            output_dir: Directory to save the file
            on_progress: Optional callback(downloaded_bytes, total_bytes)
        """
        output_path = Path(output_dir) / model.folder_name
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / model.filename

        with httpx.stream(
            "GET", model.presentation_url, follow_redirects=True
        ) as response:
            response.raise_for_status()
            total = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(file_path, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if on_progress:
                        on_progress(downloaded, total)

        return file_path

    async def download_async(
        self,
        model: Model,
        output_dir: Path | str = ".",
        on_progress: "Callable[[int, int], None] | None" = None,
    ) -> Path:
        """Async version of download with progress callback."""
        output_path = Path(output_dir) / model.folder_name
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / model.filename

        async with httpx.AsyncClient(follow_redirects=True) as client:
            async with client.stream("GET", model.presentation_url) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length", 0))
                downloaded = 0

                with open(file_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if on_progress:
                            on_progress(downloaded, total)

        return file_path
