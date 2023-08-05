# Jiggy Client

import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3 import Retry
from requests.adapters import HTTPAdapter
import requests
from .login import window_open

JIGGY_HOST     = os.environ.get('JIGGY_HOST', 'https://api.jiggy.ai')

JIGGY_KEY_FILE = os.path.expanduser('~') + '/.jiggy'   # local file to store user entered apikey 


class ClientError(Exception):
    """
    API returned 4xx client error
    """

class ServerError(Exception):
    """
    API returned 5xx Server error
    """

    
class JiggySession(requests.Session):
    def __init__(self, jiggy_api, jiggy_host=JIGGY_HOST, *args, **kwargs):
        """
        Extend requests.Session with common Jiggy authentication, retry, and exceptions.

        jiggy_api:  The jiggy api & version to use.
                    Examples: "jiggyuser-v0", "jiggyann-v0", "jiggyboard-v0"
        
        jiggy_host: The url host prefix of the form "https:/api.jiggy.ai"
                    if jiggy_host arg is not set, will use 
                    JIGGY_HOST environment variable or "api.jiggy.ai" as final default.
        
        final url prefix are of the form "https:/{jiggy_host}/{jiggy_api}"
        """
        super(JiggySession, self).__init__(*args, **kwargs)
        self.host = jiggy_host
        if requests.head(jiggy_host+"/jiggyuser-v0/docs").status_code != 200:
            raise Exception(f"Invalid or unreachable jiggy_host: {jiggy_host}")
            
        self.prefix_url = f"{jiggy_host}/{jiggy_api}"
        self.bearer_token = None
        super(JiggySession, self).mount('https://',
                                        HTTPAdapter(max_retries=Retry(connect=5,
                                                                      read=5,
                                                                      status=5,
                                                                      redirect=2,
                                                                      backoff_factor=.001,
                                                                      status_forcelist=(500, 502, 503, 504))))

    def _set_bearer(self, jwt):
        self.bearer_token = jwt
        self.headers['Authorization'] = f"Bearer {jwt}"

    def _getjwt(self, key):        
        resp = requests.post(f"{self.host}/jiggyuser-v0/auth", json={'key': key})
        if resp.status_code == 200:
            self._set_bearer(resp.json()['jwt'])
        elif resp.status_code == 401:
            raise ClientError("Invalid API Key")
        else:
            raise ServerError(resp.content)

    def _auth(self):
        if 'JIGGY_API_KEY' in os.environ:
            self._getjwt(os.environ['JIGGY_API_KEY'])
        elif os.path.exists(JIGGY_KEY_FILE):
            self._getjwt(open(JIGGY_KEY_FILE).read())
        else:
            while True:
                window_open("https://jiggy.ai/authorize")
                key_input = input("Enter your jiggy.ai API Key: ")
                if key_input[:4] == "jgy-":
                    # try using the key to see if it is valid
                    try:
                        self._getjwt(key_input)
                        # key validated, save to key file
                        open(JIGGY_KEY_FILE, 'w').write(key_input)
                        os.chmod(JIGGY_KEY_FILE, 0o600)  # -rw-------
                        break
                    except:
                        pass
                print("Invalid API Key")

        
    def request(self, method, url, *args, **kwargs):
        if not self.bearer_token:
            self._auth()
        url = self.prefix_url + url
        #print("~~~~~~~~~~~~~~~~~~~~~~~~\n", method, url)
        # support 'model' (pydantic BaseModel) arg which we convert to json parameter
        if 'model' in kwargs:
            kwargs['json'] = kwargs.pop('model').dict()
        resp =  super(JiggySession, self).request(method, url, *args, **kwargs)
        if resp.status_code == 401:
            self.bearer_token = None
            del self.headers['Authorization']
            self._auth()
            resp =  super(JiggySession, self).request(method, url, *args, **kwargs)
        if resp.status_code in [500, 502, 503, 504]:
            pass # TODO: retry these cases        
        if resp.status_code >= 500:
            raise ServerError(resp.content)
        if resp.status_code >= 400:
            raise ClientError(resp.content)
        return resp


    
