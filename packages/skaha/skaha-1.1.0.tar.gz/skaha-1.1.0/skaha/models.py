"""Models for Skaha API."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, root_validator

KINDS: List[str] = ["desktop", "notebook", "carta", "headless"]
STATUS: List[str] = ["Pending", "Running", "Terminating", "Succeeded", "Error"]
VIEW: List[str] = ["all"]


class CreateSpec(BaseModel):
    """Payload specification for creating a new session.

    Args:
        BaseModel (pydantic.BaseModel): Pydantic BaseModel.

    Returns:
        object: Pydantic BaseModel object.
    """

    name: str = Field(
        ..., description="A unique name for the session.", example="skaha-test"
    )
    image: str = Field(
        ...,
        description="Container image to use for the session.",
        example="images.canfar.net/skaha/terminal:1.1.1",
    )
    cores: int = Field(1, description="Number of cores.", ge=1, le=256)
    ram: int = Field(4, description="Amount of RAM (GB).", ge=1, le=512)
    kind: str = Field(..., description="Type of skaha session.", example="headless")
    gpu: Optional[int] = Field(None, description="Number of GPUs.", ge=1, le=28)
    cmd: Optional[str] = Field(None, description="Command to run.", example="ls")
    args: Optional[str] = Field(
        None, description="Arguments to the command.", example="-la"
    )
    env: Dict[str, Any] = Field(
        ..., description="Environment variables.", example={"TEST": "test"}
    )
    replicas: int = Field(1, description="Number of sessions to launch.", ge=1, le=256)

    # Validate that cmd, args and env are only used with headless sessions.
    @root_validator(pre=True)
    def validate_headless(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that cmd, args and env are only used with headless sessions.

        Args:
            values (Dict[str, Any]): Values to validate.

        Returns:
            Dict[str, Any]: Validated values.
        """
        assert values.get("kind") in KINDS, f"kind must be one of: {KINDS}"
        if values.get("cmd") or values.get("args") or values.get("env"):
            assert (
                values.get("kind") == "headless"
            ), "cmd, args and env are only supported for headless sessions."
        return values

    class Config:
        """Pydantic config."""

        fields = {"replicas": {"exclude": True}}


class FetchSpec(BaseModel):
    """Payload specification for fetching session[s] information.

    Args:
        BaseModel (pydantic.BaseModel): Pydantic BaseModel.

    Returns:
        object: Pydantic BaseModel object.
    """

    kind: Optional[str] = Field(
        ..., description="Type of skaha session.", example="headless"
    )
    status: Optional[str] = Field(
        ..., description="Status of the session.", example="Running"
    )
    view: Optional[str] = Field(..., description="Number of views.", example="all")

    @root_validator(pre=True)
    def validate_values(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that kind, status and views are valid.

        Args:
            values (Dict[str, Any]): Values to validate.

        Returns:
            Dict[str, Any]: Validated values.
        """
        if values.get("kind"):
            assert values.get("kind") in KINDS, f"kind must be one of: {KINDS}"
        if values.get("status"):
            assert values.get("status") in STATUS, f"status must be one of: {STATUS}"
        if values.get("view"):
            assert values.get("view") in VIEW, f"views must be one of: {VIEW}"
        return values
