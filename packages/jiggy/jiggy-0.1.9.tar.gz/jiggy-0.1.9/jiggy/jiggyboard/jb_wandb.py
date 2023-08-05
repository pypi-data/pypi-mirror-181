#
# Jiggyboard interface to wandb
#

from os import environ
from getpass import getpass
import wandb


from ..login import window_open
from ..user import authenticated_user, all_teams, Team
from .artifact_source import ArtifactService, ArtifactSource, ArtifactSourceRequest, artifact_sources
from .jiggy_session import session
from .board import get_board, create_board


def create_artifact_source(team    : Team = None,
                           api_key : str  = None,
                           host    : str  = "api.wandb.ai") -> ArtifactSource:
    """
    Create a Weights & Biases ArtifactSource

    If team is None then will use user's default team (as specified in User.default_team_id
    api_key is the wandb api key to use to access the artifacts stored on wandb. 
    host is the wandb api hostname, defaulting to api.wandb.ai
    """
    if team is None:
        # get user default team
        # not sure this is a good idea, may want to require team
        team_id = authenticated_user().default_team_id
    else:
        team_id = Team.id

    if not api_key:
        # prompt user for wandb key
        window_open("https://%s/authorize" % host.split('.',1)[1])
        api_key = getpass("Enter your wandb.ai API Key: ")
    # api key validation will occur server side
    rsp = session.post(f'/teams/{team_id}/artifact_sources', model=ArtifactSourceRequest(host    = host,
                                                                                         api_key = api_key,
                                                                                         source  = ArtifactService.wandb))
    return ArtifactSource(**rsp.json())





def jb_wandb_setup():
    """
    Setup a wandb specific leaderboard
    Use current wandb project.
    Find existing 
    """
    if not wandb.run:
        print("Run jiggyboard.setup() after wandb.init() in order to setup a Jiggyboard to use a wandb project.")
        return
    
    api = wandb.apis.PublicApi()

    proj = api.project(wandb.run.project)

    board = get_board(wandb.run.project)
    if board:
        print(f"Found existing leaderboard: '{board.name}'")
    else:
        board = create_board(wandb.run.project)
        print(f"Created leaderboard to match current wandb project: '{board.name}'")

    try:
        wandb_store = [s for s in artifact_sources() if s.source == ArtifactService.wandb][0]
    except:
        print("Creating wandb artifact source.")
        wandb_store = create_artifact_source(api_key=api.api_key)
                
    watchers = board.artifact_watchers()
    if watchers:
        print("\nFound existing Artifact Watchers:")
        for w in watchers:
            print(f"{w.jiggy_type:8} {w.name}")
    
    print(f"\nFound the following artifact collections in wandb project '{proj.name}':")
    collections = []
    count = 0
    for atype in proj.artifacts_types():
        for c in atype.collections():
            cname = f"{c.entity}/{c.project}/{c.name}"
            collections.append(cname)
            print(f" {count:2}: {atype.name+':':16} '{cname}'")
            count += 1
                
    def setup_watcher(jiggy_type):
        artifact = ""
        while artifact not in collections:
            artifact = input(f"Enter name/number to add '{jiggy_type}' watcher in this leaderboard: ")
            artifact = artifact.rstrip()
            if not artifact:
                return
            try:
                artifact = collections[int(artifact)]
            except:
                pass
        board.create_artifact_watcher(wandb_store, jiggy_type,  artifact)

    configured_watchers = set([w.jiggy_type for w in board.artifact_watchers()])
    REQUIRED_WATCHERS = set(['model','dataset','code'])
    needed_watchers = REQUIRED_WATCHERS - configured_watchers
    for jiggy_type in list(needed_watchers):
        setup_watcher(jiggy_type)

    print("\nThe following watchers are configured:")
    for w in board.artifact_watchers():
        print(f"{w.jiggy_type:8} {w.name}")

    configured_watchers = set([w.jiggy_type for w in board.artifact_watchers()])
    needed_watchers = REQUIRED_WATCHERS - configured_watchers
    if needed_watchers:
        print(f"\nNotice: The following watcher types must still be configured for a functional leaderboard: {needed_watchers}\n")


