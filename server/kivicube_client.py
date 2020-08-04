
import requests
import config
import os


class kivicube_viewer:
    def __init__(self):
        self.session = requests.session()
        self.session.verify = False
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        })

    def get_view_json(self, unique_id):
        """Get sence json, from the user perspective.

        Args:
            unique_id ([str]): sence id.

        Returns:
            [bool]: False
            [dict]: json.

        """
        url = 'https://cloud.kivicube.com/api/view/scene'

        req = self.session.get(url=url, params={'unique_id': unique_id})
        if req.status_code != 200:
            return False
        req = req.json()
        if req['code'] == 200:
            # return self._hidden_json_url(req)
            return req
        return False

    def _hidden_json_url(self, jfile):
        # can't use None to hidden, will get error.
        if isinstance(jfile, list):
            for i, v in enumerate(jfile):
                if isinstance(v, dict):
                    self._hidden_json_url(jfile[i])
                elif isinstance(v, list):
                    self._hidden_json_url(jfile[i])

                elif str(v).find("https://") > -1:
                    jfile[i] = ""
        elif isinstance(jfile, dict):
            for key, value in jfile.items():
                if isinstance(value, dict):
                    self._hidden_json_url(jfile[key])

                elif str(value).find("https://") > -1:
                    jfile[key] = ""
        return jfile

    def download_asset__file(self, file_id, download_type='marker'):
        """Downlaod asset from kivicube asset server.

        Args:
            file_id ([str]): file id.
            download_type (str, optional): marker or image. Defaults to 'marker'.


        """
        if download_type == 'marker':
            download_url = '{host}/marker/asmjs/1.0/unify/{file_id}.marker'.format(
                host=config.ASSET_HOST,
                file_id=file_id
            )
            folder = config.STATIC_MARKER_PATH
        elif download_type == 'image':
            download_url = '{host}/image/base/1.0/unify/{file_id}.jpg'.format(
                host=config.ASSET_HOST,
                file_id=file_id
            )
            folder = config.STATIC_IMAGE_PATH

        # req = self.session.get(url=download_url)
        os.system('wget {url} -P {folder}'.format(
            url=download_url,
            folder=folder
        ))

        # return False
