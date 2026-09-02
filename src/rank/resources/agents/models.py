from __future__ import annotations

from typing import List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.model import AIModel, ModelAssignResponse, ModelListResponse
from ...types.shared import MessageResponse
from .._base import AsyncAPIResource, SyncAPIResource

_MODELS = "/models"


# ---------------------------------------------------------------------------
# AIModels (sync)
# ---------------------------------------------------------------------------


class AIModels(SyncAPIResource):
    """AI model management resource.

    Access via ``client.agents.models``.

    Example::

        # List all models
        resp = client.agents.models.list()
        for m in resp.items:
            print(m.model_name, m.company_name)

        # Get models assigned to the current user
        mine = client.agents.models.mine()

        # Retrieve a single model
        model = client.agents.models.retrieve(model_id=6)

        # Assign models to the current user
        client.agents.models.assign(model_ids=[6, 7])

        # Remove a model from the current user
        client.agents.models.remove(model_id=6)
    """

    def list(
        self,
        *,
        company: Union[int, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ModelListResponse:
        """List available AI models.

        Args:
            company: Filter models by company ID.
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"company": company, "page": page, "per_page": per_page})
        return self._client.get(
            _MODELS, params=params or None, model=ModelListResponse,
        )

    def mine(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ModelListResponse:
        """List AI models assigned to the current user.

        Args:
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"{_MODELS}/mine", params=params or None, model=ModelListResponse,
        )

    def retrieve(self, model_id: int) -> AIModel:
        """Get details of an AI model.

        Args:
            model_id: ID of the model.
        """
        return self._client.get(f"{_MODELS}/{model_id}", model=AIModel)

    def assign(self, *, model_ids: List[int]) -> ModelAssignResponse:
        """Assign AI models to the current user.

        Args:
            model_ids: List of model IDs to assign.
        """
        return self._client.post(
            f"{_MODELS}/assign",
            body={"model_ids": model_ids},
            model=ModelAssignResponse,
        )

    def remove(self, model_id: int) -> MessageResponse:
        """Remove an AI model from the current user.

        Args:
            model_id: ID of the model to remove.
        """
        return self._client.delete(
            f"{_MODELS}/mine/{model_id}", model=MessageResponse,
        )


# ---------------------------------------------------------------------------
# AIModels (async)
# ---------------------------------------------------------------------------


class AsyncAIModels(AsyncAPIResource):
    """Async variant of :class:`AIModels`."""

    async def list(
        self,
        *,
        company: Union[int, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ModelListResponse:
        params = strip_not_given({"company": company, "page": page, "per_page": per_page})
        return await self._client.get(
            _MODELS, params=params or None, model=ModelListResponse,
        )

    async def mine(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ModelListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"{_MODELS}/mine", params=params or None, model=ModelListResponse,
        )

    async def retrieve(self, model_id: int) -> AIModel:
        return await self._client.get(f"{_MODELS}/{model_id}", model=AIModel)

    async def assign(self, *, model_ids: List[int]) -> ModelAssignResponse:
        return await self._client.post(
            f"{_MODELS}/assign",
            body={"model_ids": model_ids},
            model=ModelAssignResponse,
        )

    async def remove(self, model_id: int) -> MessageResponse:
        return await self._client.delete(
            f"{_MODELS}/mine/{model_id}", model=MessageResponse,
        )
