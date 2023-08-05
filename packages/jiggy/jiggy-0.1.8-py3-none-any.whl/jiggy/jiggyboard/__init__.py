# Jiggyboard Client

import sys

from .artifact_source import artifact_sources

from .board import create_board, boards, get_board, results, ArtifactType, EvalStatus


import jiggy.jiggyboard.jb_wandb as wandb    
    

def setup():
    if 'wandb' in sys.modules:
        wandb.jb_wandb_setup()

        
    
    
