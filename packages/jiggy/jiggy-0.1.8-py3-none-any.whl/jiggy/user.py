# Jiggy Client

import os
from typing import Optional, List
from pydantic import BaseModel, Field
import enum

from .jiggy_session import JiggySession


session = JiggySession('jiggyuser-v0')
    

###
## API Key
###


class  ApiKey(BaseModel):
    key:         str           = Field(default=None, description='The api key.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description of the key.')
    created_at:  float         = Field(description='The epoch timestamp when the key was created.')
    last_used :  float         = Field(description='The epoch timestamp when the key was last used to create a JWT.')
    
###
## User
###

class User(BaseModel):
    id:              int = Field(description='Internal user_id')
    username:        str = Field(min_length=3, max_length=39, description='Unique name for the user.')
    auth0_userid:    str = Field(description='Auth0 userid.  This can be None for anonymous accounts created via api key')
    default_team_id: int = Field(description='The default team for this user')


class UserPostRequest(BaseModel):
    username:        str = Field(min_length=3, max_length=39, description='Unique name for the user.')
    

class UserPostPatchRequest(BaseModel):
    default_team_id: Optional[int] = Field(description='The default team for this user')
    username:        Optional[str] = Field(min_length=3, max_length=39, description='Unique name for the user.')

    
###
## Team
###

class Team(BaseModel):
    id:          int           = Field(description='Internal team id')
    name:        str           = Field(min_length=3, max_length=39, description='Unique name for this team.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description.')
    created_at:  float         = Field(description='The epoch timestamp when the team was created.')
    updated_at:  float         = Field(description='The epoch timestamp when the team was updated.')


class TeamRole(str, enum.Enum):
    admin   = 'admin'
    member  = 'member'
    service = 'service'
    view    = 'view'
    

class TeamPostRequest(BaseModel):
    name:        str           = Field(min_length=3, max_length=39, description='Unique name for this team.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description.')

class TeamMemberPostRequest(BaseModel):
    username:    str           = Field(description='The user_id of a member to invite to the team.')
    role:        TeamRole      = Field(description='The users role in the team')

class TeamMember(BaseModel):
    id:                  int      = Field(description="Unique membership id")
    username:            str      = Field(description="Member username")
    created_at:          float    = Field(description='The epoch timestamp when the membership was created.')
    updated_at:          float    = Field(description='The epoch timestamp when the membership was updated.')
    invited_by_username: str      = Field(description="The username that invited this member to the team.")
    role:                TeamRole = Field(description="The user's role in the team")
    accepted:            bool     = Field(description='True if the user has accepted the team membership.')
    
        
###
##  Teams
###
class Team(BaseModel):
    id:          int           = Field(description='Internal team id')
    name:        str           = Field(min_length=3, max_length=39, description='Unique name for this team.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description.')
    created_at:  float         = Field(description='The epoch timestamp when the team was created.')
    updated_at:  float         = Field(description='The epoch timestamp when the team was updated.')

    def members(self) -> List[TeamMember]:
        return [TeamMember(**tm) for tm in session.get(f'/teams/{self.id}/members').json()['items']]
    
    def add_member(self, username : str, role : TeamRole) -> TeamMember:
        """
        invite the specified username to this team with the corresponding TeamRole
        """
        rsp = session.post(f"/teams/{self.id}/members", json={"username": username, 'role':role})
        return TeamMember(**rsp.json())

    def delete_member(self, username : str):
        """
        attempt to remove the specified username from this team
        """
        member = [m for m in self.members() if m.username == username]
        if not member:
            raise Exception(f"{username} not found in Team")
        session.delete(f"/teams/{self.id}/members/{member[0].id}")

    def set_default(self):
        """
        Set this team as the user's default team.
        """
        user_id = authenticated_user().id
        session.patch(f"/users/{user_id}", json={'default_team_id': self.id})
        

def all_teams() -> List[Team]:
    """
    return all Teams that the user is a member of
    """
    resp = session.get('/teams')
    return [Team(**i) for i in resp.json()['items']]


def team(name_or_id) -> Team:
    """
    get team by name or id
    raises Exception if an exact match for name is not found
    """
    teams = [t for t in session.get('/teams').json()['items'] if t['name'] == name_or_id or t['id'] == name_or_id]
    if len(teams):
        return Team(**teams[0])
    raise Exception(f'Team "{name}" not found')


def api_keys() -> List[ApiKey]:
    return [ApiKey(**i) for i in session.get('/apikey').json()['items']]


def authenticated_user() -> User:
    """
    return the authenticated user's User object
    """
    return User(**session.get("/users/current").json())


def create_team(name : str) -> Team:
    resp = session.post("/teams", json={"name":name})
    return Team(**resp.json())



