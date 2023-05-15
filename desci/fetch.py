import os
import pandas as pd
import requests
import hashlib
import pickle
import os.path
from urllib.parse import urljoin


class dpid:
    BASE_URL = "https://{resolver}.dpid.org/"
    RESOLVERS = ['beta', 'beta-dev']

    @staticmethod
    def fetch(dpid_path, options={}):
        # handle the 'resolver' option
        resolver = options.get('resolver', 'beta')
        if resolver not in dpid.RESOLVERS:
            raise ValueError("Invalid resolver option")

        # form the final URL by combining the base URL with the provided dpid path
        url = urljoin(dpid.BASE_URL.format(
            resolver=resolver), dpid_path + '?raw')

        response = requests.get(url)

        # generate a unique hash for the content to use as the cache key
        content_hash = hashlib.md5(response.content).hexdigest()
        cache_file = f'cache/{content_hash}'

        # check if the cache option is enabled and the data is already cached
        if options.get('cache', False) and os.path.isfile(cache_file):
            print(f"Loading {dpid_path} from cache")
            with open(cache_file, 'rb') as file:
                return pickle.load(file)

        # get the final URL after all redirects
        final_url = response.url

        file_extension = os.path.splitext(final_url)[-1].lower()

        if file_extension == '.py':
            with open('temp.py', 'w') as file:
                file.write(response.text)
            module = __import__('temp')
            os.remove('temp.py')
            result = module
        elif file_extension == '.txt':
            result = response.text
        elif file_extension == '.csv':
            import io
            s = io.StringIO(response.content.decode('utf-8'))
            result = pd.read_csv(s)
        else:
            result = response

        # if the cache option is enabled, cache the data
        if options.get('cache', False):
            if not os.path.exists('cache'):
                os.makedirs('cache')
            with open(cache_file, 'wb') as file:
                pickle.dump(result, file)

        return result
