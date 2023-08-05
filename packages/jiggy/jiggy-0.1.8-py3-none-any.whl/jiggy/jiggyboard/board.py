#  Board and related client

from os import environ
from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic import condecimal
import enum

from .jiggy_session import session

from .artifact_source import ArtifactSource
from ..user import Team, authenticated_user, all_teams


###
##   EvaluationResult
###

class EvaluationResult(BaseModel):
    """
    One (name: value) evaluation result pair for a particular evaluation.
    Value can be an integer, float, bool, or string.
    """
    id:       int             = Field(description='Unique result ID')
    eval_id:  int             = Field(description='The evaluation with which this result is associated')
    name:     str             = Field(description='The name of this result')
    intval:   Optional[int]   = Field(description='an integer evaluation result')
    floatval: Optional[float] = Field(description='a double float evaluation result')
    strval:   Optional[str]   = Field(description='a string evaluation result')
    boolval:  Optional[bool]  = Field(description='a boolean evaluation result')




class PostEvaluationResult(BaseModel):
    """
    One (name: value) evaluation result pair for a particular evaluation.
    Value can be an integer, float, bool, or string.
    """
    name:     str             = Field(description='The name of this result')
    intval:   Optional[int]   = Field(description='an integer evaluation result')
    floatval: Optional[float] = Field(description='a double float evaluation result')
    strval:   Optional[str]   = Field(description='a string evaluation result')
    boolval:  Optional[bool]  = Field(description='a boolean evaluation result')

    

###
##   Evaluation
###

class EvalStatus(str, enum.Enum):
    """
    The status of an evaluation.
    """
    scheduled = 'scheduled'
    running   = 'running'
    failed    = 'failed'    # failed to execute evaluation code due to runtime error
    error     = 'error'     # error occured in the evaluation code
    complete  = 'complete'


class EvaluationPatchRequest(BaseModel):
    """
    An evaluation of a specific version of code, model, and dataset.
    """
    status:           EvalStatus    = Field(index=True, description='The status of the evaluation')
    percent_complete: Optional[int] = Field(default=0, ge=0, le=100, description='The evaluation progress as an integer completeness percentage.')
    

class Evaluation(BaseModel):
    """
    An evaluation of a specific version of code, model, and dataset.
    """
    id:               int           = Field(description='Unique eval ID')
    team_id:          int           = Field(description='The Team with which this artifact series is associated.')
    board_id:         int           = Field(description='The Board with which this Evaluation is associated.')
    code_id:          int           = Field(description='The eval code used for the Evaluation')
    model_id:         int           = Field(description='The model used for the Evaluation')
    dataset_id:       int           = Field(description='The dataset used for the Evaluation')
    env_id:           int           = Field(description='The environment used for the Evaluation')
    status:           EvalStatus    = Field(description='The status of the evaluation')
    created_at:       float         = Field(description='The epoch timestamp when the Evaluation was created.')
    updated_at:       float         = Field(description='The epoch timestamp when the Evaluation was updated.')
    ipynb_output:     Optional[str] = Field(default=None, description='The uri of the ipynb output of the evaluation run')
    html_output:      Optional[str] = Field(default=None, description='The uri of the html output of the evaluation run')
    pdf_output:       Optional[str] = Field(default=None, description='The uri of the pdf output of the evaluation run')
    percent_complete: Optional[int] = Field(default=0, ge=0, le=100, description='The evaluation progress as an integer completeness percentage.')
    
    def results(self) -> dict:
        """
        return dictionary of all results for the evaluation
        """
        rsp = session.get(f"/teams/{self.team_id}/boards/{self.board_id}/evaluations/{self.id}/results")
        def er2val(er):
            if er.intval is not None:
                return er.intval
            if er.floatval is not None:
                return er.floatval
            if er.strval is not None:
                return er.strval
            if er.boolval is not None:
                return er.boolval
            return None
        return {i['name']: er2val(EvaluationResult(**i)) for i in rsp.json()['items']}
        
    
###
##   Artifact
###

class ArtifactType(str, enum.Enum):
    """
    the types of artifact we deal in
    """
    code    = 'code'     
    model   = 'model'
    dataset = 'dataset'



    
class Artifact(BaseModel):
    """
    A specific version of an Artifact that we have discovered
    """
    id:          int          = Field(description='Unique ID of a specific version of a BoardArtifact')
    team_id:     int          = Field(description='The team that owns the board.')
    board_id:    int          = Field(description='The Board with which this artifact is associated.')
    name:        str          = Field(description="The full name of the artifact including version info.")
    jiggy_type:  ArtifactType = Field(description='The type of this artifact in jiggy: "code", "dataset", or "model".')    
    created_at:  float        = Field(description='The epoch timestamp when the ArtifactVersion was created in Jiggyboard.')


###
##    ArtifactWatcher 
###


class WatcherDefault(str, enum.Enum):
    """
    Configures an ArtifactWatcher to default to processing all new versions as they are discovered or ignoring new versions.
    
    process:  process (evaluate) all new artifact versions as they are discovered.  
              This can be modified by additional WatcherRules to exclude certain versions/aliases from processing.

    ignore:   ignore all new artifact versions as they are discovered.  
              This can be modified by additional WatcherRules which enable processing for certain versions/aliases.
    """
    process  = 'process'
    ignore   = 'ignore'

    
class ArtifactWatcher(BaseModel):
    """
    An Artifact that a board is configured to use
    """
    id:           int            = Field(description='Unique ArtifactWatcher ID.')
    team_id:      int            = Field(description='The team that owns the board.')
    board_id:     int            = Field(description='The Board with which this artifact is associated.')
    name:         str            = Field(description='A versionless artifact name in the form of "entity/project/name", as known to the backend service')
    jiggy_type:   ArtifactType   = Field(description='The type of this artifact in jiggy: "code", "dataset", or "model".')
    source_id:    int            = Field(description='The backend service configuration to access artifact')
    source_type:  str            = Field(description='The type of the artifact as known to the backend service.')
    enabled:      bool           = Field(description='True if evaluation is enabled for this artifact, False if disabled.')    
    default:      WatcherDefault = Field(description="Sets the default policy to process or ignore new artifact versions. Modified by WatcherRules.")
    created_at:   float          = Field(description='The epoch timestamp when the Artifact was created.')
    updated_at:   float          = Field(description='The epoch timestamp when the Artifact was updated.')
    created_by:   int            = Field(description='The user_id that created this item.')
    updated_by:   int            = Field(description='The user_id that last modified this item.')

    def delete(self):
        session.delete(f'/teams/{self.team_id}/boards/{self.board_id}/watchers/{self.id}')



class ArtifactWatcherPostRequest(BaseModel):
    """
    Create a ArtifactWatcher
    """
    source_id:    int            = Field(description='The configuration to access artifact')
    jiggy_type:   ArtifactType   = Field(description='The type of this artifact.')
    name:         str            = Field(description='The name of the artifact as found in the Artifact Source.')
    enabled:      Optional[bool] = Field(default=True, description='True if evaluation is enabled for this artifact, False if disabled.')
    default_all:  Optional[bool] = Field(default=True, description="True to process all versions by default. False to process no versions by default. Policy modified by ArtifactWatcherRules")


class ArtifactWatcherPatchRequest(BaseModel):
    """
    Modify a ArtifactWatcher.
    """
    enabled:       Optional[bool] = Field(default=None, description='True if evaluation is enabled for this artifact, False if disabled.')
    default_all:   Optional[bool] = Field(default=None, description="True to process all versions by default. False to process no versions by default. Policy modified by ArtifactWatcherRules")
    


    
###
##  Board
###
    
class Board(BaseModel):
    """
    A very Jiggy leaderboard that tracks results across a range of different model, dataset versions, and eval code versions
    """
    id:          int    = Field(description='Unique Board ID')
    name:        str    = Field(description='The name of the Board.  Must be unique in team context.')
    team_id:     int    = Field(description='The team that owns this Board.')
    public:      bool   = Field(description='True if Board is publicly visible, False if private to a team.')
    enabled:     bool   = Field(description='True if evaluation is enabled for this Board, False if disabled.')
    created_at:  float  = Field(description='The epoch timestamp when the Board was created.')
    updated_at:  float  = Field(description='The epoch timestamp when the Board was updated.')
    created_by:  int    = Field(description='The user_id that created this item.')
    updated_by:  int    = Field(description='The user_id that last modified this item.')

    def delete(self):
        session.delete(f'/teams/{self.team_id}/boards/{self.id}')

    def create_artifact_watcher(self,
                                source:      ArtifactSource,
                                jiggy_type:  ArtifactType,
                                name:        str,
                                enabled:     bool = True,
                                default_all: bool = True) -> ArtifactWatcher:

        post_model = ArtifactWatcherPostRequest(board_id = self.id,
                                                source_id = source.id,
                                                **locals())
        
        rsp = session.post(f'/teams/{self.team_id}/boards/{self.id}/watchers', model = post_model)
        return ArtifactWatcher(**rsp.json())
                           

    def artifact_watchers(self) -> List[ArtifactWatcher]:
        rsp = session.get(f"/teams/{self.team_id}/boards/{self.id}/watchers")
        return [ArtifactWatcher(**w) for w in rsp.json()['items']]
    

    def artifacts(self) -> List[Artifact]:
        rsp = session.get(f'/teams/{self.team_id}/boards/{self.id}/artifacts')
        return [Artifact(**a) for a in rsp.json()['items']]

    def artifact(self, artifact_id) -> Artifact:
        rsp = session.get(f'/teams/{self.team_id}/boards/{self.id}/artifacts/{artifact_id}')
        return Artifact(**rsp.json())
    
    def evaluations(self, status : EvalStatus = None) -> List[Evaluation]:
        if status:
            rsp = session.get(f'/teams/{self.team_id}/boards/{self.id}/evaluations?status={status}')
        else:
            rsp = session.get(f'/teams/{self.team_id}/boards/{self.id}/evaluations')
        return [Evaluation(**e) for e in rsp.json()['items']]


    def evaluation(self, eval_id : int) -> Evaluation:
        rsp = session.get(f'/teams/{self.team_id}/boards/{self.id}/evaluations/{eval_id}')
        return Evaluation(**rsp.json())

    
class BoardPostRequest(BaseModel):
    """
    Create a Board item
    """
    name:        str             = Field(description='The name of the Board.  Must be unique in team context.')
    description: Optional[str]   = Field(description='The description of this board.')    
    public:      Optional[bool]  = Field(default=False, description='True if Board is publicly visible, False if private to a team.')
    enabled:     Optional[bool]  = Field(default=True, description='True if evaluation is enabled for this Board, False if disabled.')


class BoardPatchRequest(BaseModel):
    """
    Modify a Board item
    """
    name:        Optional[str]   = Field(default=None,  description='The name of the Board.  Must be unique in team context.')
    public:      Optional[bool]  = Field(default=None,  description='True if Board is publicly visible, False if private to a team.')
    enabled:     Optional[bool]  = Field(default=None,  description='True if evaluation is enabled for this Board, False if disabled.')
    
    



    
###
##    WatcherRule
### 

class WatcherRule(BaseModel):
    """
    A rule applied to a ArtifactWatcher that serves to configure or limit evaluation of specific versions or aliases.
    """
    id:             int           = Field(description='Unique ID')
    artifact_id:    int           = Field(description='The ArtifactWatcher this Rule is associated with')
    alias:          Optional[str] = Field(description='Configure evaluation for this alias of the artifact.')
    ignore_alias:   Optional[str] = Field(description='Ignore evaluation for this alias of the artifact.')
    version:        Optional[str] = Field(description='Configure evaluation for this specific version of the artifact.')
    ignore_version: Optional[str] = Field(description='Disable evaluation for this specific version of the artifact.')
    created_at:     float         = Field(description='The epoch timestamp when the Artifact was created.')
    updated_at:     float         = Field(description='The epoch timestamp when the Artifact was updated.')
    created_by:     int           = Field(description='The user_id that created this item.')
    updated_by:     int           = Field(description='The user_id that last modified this item.')



class WatcherRulePostRequest(BaseModel):
    """
    Used to create a WatcherRule
    """
    artifact_id:    int           = Field(description='The ArtifactWatcher this Rule is associated with')
    alias:          Optional[str] = Field(description='Configure evaluation for this alias of the artifact.')
    ignore_alias:   Optional[str] = Field(description='Ignore evaluation for this alias of the artifact.')
    version:        Optional[str] = Field(description='Configure evaluation for this specific version of the artifact.')
    ignore_version: Optional[str] = Field(description='Disable evaluation for this specific version of the artifact.')



def create_board(name:        str,
                 team:        Team = None,
                 description: str  = None,
                 public:      bool = False,
                 enabled:     bool = True) -> Board:
    """
    Create a board with the specified parameters
    
    If no team is specified, the user's default team will be used
    """
    if team is None:
        team_id = authenticated_user().default_team_id
    else:
        team_id = Team.id
    rsp = session.post(f"/teams/{team_id}/boards", model=BoardPostRequest(**locals()))
    return Board(**rsp.json())


    
def boards(team : Team = None) -> List[Board]:
    """
    Get the boards for the specified team.
    If no team is specified, the boards for all of the user's teams will be returned.
    """
    if team:
        r = session.get(f"/teams/{team.id}/boards")
        items = r.json()['items']
    else:
        items = []
        for team in all_teams():
            r = session.get(f"/teams/{team.id}/boards")
            items.extend(r.json()['items'])    
    return [Board(**b) for b in items]
    



def get_board(name : str,
          team : Team = None) -> Board:
    """
    return a board of the specified name.
    If team is None then return the board from any of the teams.  
    Note: a board name could be duplicated across multiple teams. 
    In this case this function returns the first matching name it finds.
    """
    for board in boards(team):
        if board.name == name:
            return board
    


def results(results : dict):
    """
    Record the final results of an evaluation run.
    takes a dictionary of with arbitrary key names and integer, float, string, or bool values
    """
    if not 'JIGGY_PRODUCTION_RUNTIME' in environ:
        print("Detected development evaluation run; not storing results in Jiggyboard")
        return
    
    team_id  = int(environ['JIGGY_TEAM_ID'])
    board_id = int(environ['JIGGY_BOARD_ID'])
    eval_id  = int(environ['JIGGY_EVAL_ID'])

    for key, value in results.items():
        if isinstance(value, float):
            model = PostEvaluationResult(name=key, floatval=value)
        elif isinstance(value, int):
            model = PostEvaluationResult(name=key, intval=value)
        elif isinstance(value, str):
            model = PostEvaluationResult(name=key, strval=value)
        elif isinstance(value, bool):
            model = PostEvaluationResult(name=key, boolval=value)
        else:
            print(f"Unable to record result for {key}. (Value must be of type must be float, int, str or bool.)")
            continue
        session.post(f"/teams/{team_id}/boards/{board_id}/evaluations/{eval_id}/results", model=model)
