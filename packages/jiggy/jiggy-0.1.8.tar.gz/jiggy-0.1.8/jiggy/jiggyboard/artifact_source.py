#  Artifact Source client


from typing import Optional, List
from pydantic import BaseModel, Field
import enum

from .jiggy_session import session
from ..user import Team, authenticated_user, all_teams

class ArtifactService(str, enum.Enum):
    """
    The set of backend artifact stores that we know how to access
    """    
    wandb   = 'Weights & Biases'
    hf      = 'Hugging Face'
    jb      = 'Jiggyboard'


class ArtifactSource(BaseModel):
    """
    The sources of the models, weights, and (eval) code that we deal with
    """
    id:         int             = Field(description='Unique Configuration ID')
    team_id:    int             = Field(description='The team_id that owns this artifact source')
    source:     ArtifactService = Field(description='Source of Artifacts such as datasets and models')
    api_key:    str             = Field(description='API Key to access the datasource service')
    host:       Optional[str]   = Field(default=None, description='alterative (e.g. private) hostname')
    created_by: int             = Field(description='The user_id that created this item.')
    updated_by: int             = Field(description='The user_id that last modified this item.')

    def delete(self):
        """
        attempt to delete this ArtifactSource
        """
        session.delete(f"/teams/{self.team_id}/artifact_sources/{self.id}")
                       
    
class ArtifactSourceRequest(BaseModel):
    """
    Create an ArtifactSource
    """
    source:  ArtifactService = Field(description='Source of Artifacts such as datasets and models')
    api_key: str             = Field(description='API Key to access the datasource service')
    host:    Optional[str]   = Field(default=None, description='alterative (e.g. private) hostname')



def artifact_sources(team : Team = None) -> List[ArtifactSource]:
    """
    return list of all artifact sources
    """
    if team:
        r = session.get(f"/teams/{team.id}/artifact_sources")
        items = r.json()['items']
    else:
        items = []
        for team in all_teams():
            r = session.get(f"/teams/{team.id}/artifact_sources")
            items.extend(r.json()['items'])
    return [ArtifactSource(**i) for i in items]


