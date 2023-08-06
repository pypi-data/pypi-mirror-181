"""Common models and functionality related to Dapla teams."""
from pydantic import BaseModel


class TeamInfo(BaseModel):
    """Information about a Dapla team.

    Attributes:
        name: Dapla team name, such as `demo-enhjoern-a`
        org_no: The GCP organization number
    """

    name: str
    org_no: str
