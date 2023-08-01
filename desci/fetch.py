import os
import pandas as pd
import requests
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

        # make a HEAD request to fetch the headers and get the ETag containing the content hash
        session = requests.Session()
        response = session.head(url, allow_redirects=True)
        etag = response.headers.get('ETag')

        # if the ETag header is not present, raise an exception
        if etag is None:
            raise ValueError("ETag header not present in response")

        # handle 'weak' ETags, which are prefixed by 'W/'
        if etag.startswith('W/'):
            # remove the first 3 characters ('W/"') and the last character ('"')
            etag = etag[3:-1]

        # use the ETag as the cache key
        cache_file = f'cache/{etag}'

        # check if the cache option is enabled and the data is already cached
        if options.get('cache', False) and os.path.isfile(cache_file):
            print(f"Loading {dpid_path} from cache")
            with open(cache_file, 'rb') as file:
                return pickle.load(file)

        # if the data is not in the cache, make a GET request to fetch the data
        response = requests.get(url)

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

    @staticmethod
    def toCid(dpid_path, options={}):
        # handle the 'resolver' option
        resolver = options.get('resolver', 'beta')
        if resolver not in dpid.RESOLVERS:
            raise ValueError("Invalid resolver option")

        # form the final URL by combining the base URL with the provided dpid path
        url = urljoin(dpid.BASE_URL.format(
            resolver=resolver), dpid_path + '?raw')

        # make a HEAD request to fetch the headers and get the ETag containing the content hash
        session = requests.Session()
        response = session.head(url, allow_redirects=True)
        etag = response.headers.get('ETag')

        # if the ETag header is not present, raise an exception
        if etag is None:
            raise ValueError("ETag header not present in response")

        # handle 'weak' ETags, which are prefixed by 'W/'
        if etag.startswith('W/'):
            # remove the first 3 characters ('W/"') and the last character ('"')
            etag = etag[3:-1]
        else:
            # remove the first character ('"') and the last character ('"')
            etag = etag[1:-1]

        # return the ETag as the CID
        return etag
