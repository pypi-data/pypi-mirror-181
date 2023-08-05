# Jiggy ANN Client

import os
import requests
import urllib.parse

from typing import Optional, List
from pydantic import BaseModel, Field
from time import time, sleep
import enum

import hnswlib


from .jiggy_session import JiggySession


session = JiggySession('jiggy-v0')
#session = JiggySession('jiggyann-v0')


class IndexError(Exception):
    """
    Index creation failed
    """


    
class IndexLibraries(str, enum.Enum):
    """
    The library used to create the index.
    Currently only 'hnswlib' is supported.
    """
    hnswlib = 'hnswlib'


class DistanceMetric(str, enum.Enum):
    """
    The distance metric to use for the nearest neighbor index.
    """
    cosine = 'cosine'
    ip     = 'ip'
    l2     = 'l2'

class IndexBuildState(str, enum.Enum):
    prep = "preparing data"
    indexing = "indexing vectors"
    saving = "saving index"
    complete = "index complete"
    failed = "indexing failure"

    
class Collection(BaseModel):
    
    id:    int = Field(description='Unique identifier for a particular collection.')
    name:  str = Field(description="The Collection's unique name within the team context.")

    dimension: int         = Field(default= 0, description="The dimension of the vectors in this collection.")
    team_id:   int         = Field(None, index=True, description="The team that this collection is associated with.")
    count: int             = Field(default=0, description="The number of vectors in the collection")
    created_at: float = Field(description='The epoch timestamp when the collection was created.')
    updated_at: float = Field(description='The epoch timestamp when the collection was updated.')
       
    def add(self, vector_data:[float], vector_id:int):
        """
        Add the specified vector_data to the collection and associate it with the specified vector_id.
        A collection may not have more than one vector with a given vector_id.
        Re-using a vector_id will over-write any existing  vector_id +  vector pair.
        All vectors in a collection must share the same dimension.
        """
        vector_data = [float(x) for x in vector_data]
        session.post(f"/collections/{self.id}/vectors/{vector_id}", json={'vector': vector_data})
        if not self.dimension:
            self.dimension = len(vector_data)  # record dimension

    def get(self, vector_id : int):
        """
        Return the vector with the specified vector_id from the collection
        """
        resp = session.get(f"/collections/{self.id}/vectors/{vector_id}")
        return resp.json()['vector']
        
    def delete(self, vector_id : int):
        """
        Delete the vector with the specified vector_id from the collection
        """        
        session.delete(f"/collections/{self.id}/vectors/{vector_id}")
        
    def create_index(self,
                     tag='latest',
                     target_library=IndexLibraries.hnswlib,
                     metric=DistanceMetric.cosine,
                     target_recall=None,
                     M=None,
                     ef=None):
        body = {'tag': tag,
                'target_library': target_library,
                'metric': metric,
                'target_recall': target_recall,
                'hnswlib_M':  M,
                'hnswlib_ef': ef}
        resp = session.post("/collections/%d/index" % self.id, json=body)
        return Index(**resp.json(), collection=self)
                                                            
    def delete_collection(self):
        """
        Delete the collection.
        """
        resp = session.delete("/collections/%s" % self.id)
        self.id=None
        self.name= None
        self.created_at=None
        self.updated_at=None
        self.team_id=None
        self.dimension=None


    def get_index(self, tag:str="latest"):
        data = {'tag': tag}
        resp = session.get(f"/collections/{self.id}/index?{urllib.parse.urlencode(data)}")
        items = resp.json()['items']
        if tag and items:
            return Index(**items[0], collection=self)
        return [Index(**i, collection=self) for i in items]

    def get_all_index(self):
        return self.get_index(None)

    def _update(self):
        resp = session.get(f"/collections/{self.id}")
        self.__dict__.update(resp.json())
        
    def __getattribute__(self, attr):
        if attr in ['count', 'updated_at']:
            self._update()
        return object.__getattribute__(self, attr)        

        
def create_collection(name:str, team_name=None):
    """
    Create a collection of the specified name
    Returns a Collection object.
    Raises ClientError if the specified name already exists

    'team_obj_or_name' is optional and can be either a team name or team object.
    if team is unspecified the user's default team will be used.
    """
    data = {'name': name}
    if team_name:
        data['team_id'] = team(team_name).id
    resp = session.post("/collections", json=data)
    return Collection(**resp.json())


def collection(name:str):
    """
    Get a collection by name.
    Returns a Collection Object, or None if collection name is not found
    """
    data = {'name': name}
    resp = session.get(f"/collections?{urllib.parse.urlencode(data)}")
    items = resp.json()['items']
    if len(items):
        return Collection(**items[0])
    raise Exception(f"Collection {name} not found")


def all_collections():
    resp = session.get("/collections")
    return [Collection(**i) for i in resp.json()['items']]


class Index(BaseModel):
    id: int            = Field(description='Unique identifier for a given index.')
    collection: Collection = Field(description="The containing collection")
    tag:  str = Field(description="User tag for this Index.  Uniquely identifies an index in the context of a collection.")
    name: str = Field(description="The full name for this index in the form of TEAM_NAME/COLLECTION_NAME:TAG")
    target_library:    IndexLibraries = Field(default=IndexLibraries.hnswlib, description="The library use to create the index")
    metric:        str = Field(description='The distance metric ("space" in hnswlib): "cosine", "ip", or "l2"')
    hnswlib_M:  Optional[int] = Field(default=None, description="The M value passed to hnswlib when creating the index.")
    hnswlib_ef: Optional[int]  = Field(default=None, description="The ef_construction value passed to hnswlib when creating the index.")
    hnswlib_ef_search: Optional[int] = Field(default=None, ge=10, description="The recommended ef value to use at search time.")
    target_recall: Optional[float] = Field(default=None, ge=0.5, le=1, description="The desired recall value to target for index parameter optimization.")        
    count: int = Field(description="The number of vectors included in the index.  The number of vectors in the collection at the time of index build.")
    created_at: float = Field(description='The epoch timestamp when the index was requested to be created.')
    state: IndexBuildState = Field(description = "The current build status.")
    completed_at: float = Field(description='The epoch timestamp when the index build was completed.')
    build_status: str     = Field(description='Informational status message for the index build.')
    url: Optional[str] = Field(default=None, description='The url the index can be downloaded from.  The url is valid for a limited time.')

    
    def _wait_complete(self):
        while self.state not in [IndexBuildState.failed, IndexBuildState.complete]:
            print(f"Index Status: {self.build_status}")  # XXX provide percentage completion
            data = {'tag': self.tag}
            resp = session.get(f"/collections/{self.collection.id}/index?{urllib.parse.urlencode(data)}")
            items = resp.json()['items'][0]
            self.__dict__.update(items)
            sleep(2)  # XXX update sleep time based on something like halfway toward the estimated remaining completed_at estimate
        if self.state == IndexBuildState.failed:
            raise IndexError(self.build_status)
        
            
    def hnswlib_index(self, max_elements:int = None):
        self._wait_complete()
        if not max_elements:
            max_elements = self.count
        resp = requests.get(self.url)
        assert(resp.status_code == 200)
        assert(int(len(resp.content)) == int(resp.headers['Content-Length']))
        fname = self.name.replace('/','-')
        fname += f".{self.target_library}"
        open(fname, 'wb').write(resp.content)
        ix = hnswlib.Index(space=self.metric, dim=self.collection.dimension)
        ix.load_index(fname, max_elements=max_elements)
        ef = self.hnswlib_ef_search if self.hnswlib_ef_search else self.hnswlib_ef
        ix.set_ef(ef)
        return ix

    def tests(self):
        """
        Return the IndexTest results for this index
        """
        tests = session.get(f'/collections/{self.collection.id}/index/{self.id}/tests').json()['items']
        return [IndexTest(**test, index=self) for test in tests]


class IndexTest(BaseModel):
    id:                   int = Field(description="Unique database identifier for a given index test.")
    index:              Index = Field(description="The index under test.")
    test_count:           int = Field(description="The number of vectors in the test sample.")
    test_k:               int = Field(description="The number of nearest neighbors (k) to query for each test vector.")
    recall:             float = Field(description="The recall of the index based on a comparison to exhaustive KNN.")
    qps:                float = Field(description="The estimated queries per second of the index for vector search with batchsize of 1 (a single vector at a time).")
    cpu_info:             str = Field(description="The CPU that executed the test.")
    created_at:         float = Field(description="The epoch timestamp when the test was completed.")
    hnswlib_ef: Optional[int] = Field(default=None, description="The ef value passed to hnsw_index.set_ef() for this test.")
        
    def __repr__(self):
        return f"{self.index.name:20s}: recall: {self.recall:5.3f}  QPS: {self.qps:7.1f} @ EF={self.hnswlib_ef}"
    

