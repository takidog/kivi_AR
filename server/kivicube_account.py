import requests
import logging
import util

logging.basicConfig(level=logging.DEBUG)

console = logging.StreamHandler()
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
kivicube_log = logging.getLogger("kivicube_account")


class kivicube_account:
    def __init__(self, username=None, password=None):
        self.session = requests.session()
        # self.session.verify = False

        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            "origin": 'https://cloud.kivicube.com',
            'sec-fetch-mode': 'cors'
        })
        if not self.csrf():
            kivicube_log.warning(msg='Fail get csrf.')
            raise ValueError()

        if not self.login(username=username, password=password):
            kivicube_log.warning(msg='Login fail.')
            raise ValueError()
        self.project = None

    def login(self, username, password, type='email'):
        """login ro kivicube.
        now only support email login.
        Args:
            username ([str]): email.
            password ([str]): password.
            type (str, optional): login type.. Defaults to 'email'.

        Returns:
            [bool]: Login status.
        """
        url = 'https://cloud.kivicube.com/account/login/email'
        data = {
            "password": password,
            "captcha": "",
            "email": username
        }

        res = self.session.post(url=url, json=data)
        if res.status_code != 200:
            return False
        if res.json()['code'] != 200:
            return False
        elif res.json()['code'] == 200:
            self.csrf(login_status=True)
            return True
        return False

    def csrf(self, login_status=False):
        """renew csrf token.

        Args:
            login_status (bool, optional): when after login will use another csrf url. Defaults to False.

        Returns:
            [bool]: [description]
        """
        if login_status == True:
            url = 'https://cloud.kivicube.com/user/infood'
            key_name = 'csrf'
        else:
            url = 'https://cloud.kivicube.com/common/csrf'
            key_name = '_csrf'
        csrf = self.session.get(url=url)
        if csrf.status_code == 200:
            csrf_json = csrf.json()
            if csrf_json['code'] != 200:
                return False
            elif csrf_json['code'] == 200:
                self.session.headers.update({
                    "x-csrf-token": csrf_json['data'][key_name]
                })
                return True
        return False

    def create_project(self, project_name=None):
        """create project 

        Args:
            project_name ([str], optional): Set project name, if not set will random. Defaults to None.

        Returns:
            [str]: project name.
            [bool]: False.
        """
        create_url = 'https://cloud.kivicube.com/project/create'
        data = {
            "sdkType": "vuforia",
            "functionType": "web3d",
            "name": project_name if project_name != None else util.randStr(
                16),
            "description": "",
            "coverPicture": None
        }
        req = self.session.post(url=create_url, json=data)
        if req.json()['code'] == 200:
            return data['name']
        return False

    def get_project(self, force_renew=False):
        """Get project list.

        Args:
            self ([type]): [description]

        Returns:
            [list]:{ 
                "id": 2703,
                "uniqid": "b9scml",
                "name": "test3sdadlkp",
                "status": 1,
                "public": 0,
                "shareToPublicProject": 0,
                "appTrackingMode": "cloud",
                "functionType": "web3d",
                "description": "",
                "coverPicture": "https://kivicube-resource.kivisense.com/projectCoverPicture/s3ywr5nl8cM5pt9ZFzP49i4n5NjIeEGC.jpg",
                "tags": [],
                "viewCount": 0,
                "qrcodeUrl": "https://kivicube-resource.kivisense.com/projectQrcode/b9scml.jpg",
                "shareUrl": "https://www.kivicube.com/projects/b9scml",
                "defaultScene": null,
                "defaultSceneType": null,
                "scenes": []
            }
        """
        if self.project != None and force_renew is False:
            return self.project

        project_list_url = 'https://cloud.kivicube.com/project/search'
        req = self.session.get(url=project_list_url)
        if req.status_code != 200:
            logging.debug(msg='Get project list fail')
            return None
        req_json = req.json()
        if req_json['code'] == 200:
            self.project = req_json['data']
            return self.project

    def get_all_asset(self):
        """Get all asset.

        Returns:
            [list]: {
                    "id": 8943,
                    "title": "Allosaurus",
                    "identify": "IAPdfXWF9spxPgWGDPx-Lp2hYP3_eOrr",
                    "type": "model",
                    "description": "",
                    "updatedAt": 1572924428,
                    "suffix": "zip",
                    "thumbnails": "https://kivicube-resource.kivisense.com/model.png?unique=1572924428",
                    "info": {
                        "modelInfo": [],
                        "hierarchy": [],
                        "meta": [],
                        "format": "zip",
                        "name": "Allosaurus",
                        "size": 28339554
                    },
                    "model": "https://kivicube-asset.kivisense.com/model/base/1.0/unify/IAPdfXWF9spxPgWGDPx-Lp2hYP3_eOrr.zip?OSSAccessKeyId=LTAIEq1suktu3c0O&Expires=1574674749&Signature=jtdkPwxSBOf50ZcdDk4BZqYq%2BQ4%3D",
                    "materialPackStatus": 2,
                    "gltf": "https://kivicube-asset.kivisense.com/model/gltf/2.0/unify/IAPdfXWF9spxPgWGDPx-Lp2hYP3_eOrr/IAPdfXWF9spxPgWGDPx-Lp2hYP3_eOrr.gltf",
                    "import": 1,
                    "imported": false,
                    "update": false,
                    "verifyStatus": 0,
                    "useCount": 1
                }
        """
        url = 'https://cloud.kivicube.com/materials/gets'
        params = {
            "expand": "import,imported,update,useCount,verifyStatus,materialPackStatus"}

        req = self.session.get(url=url, params=params)
        if req.status_code == 200:
            return req.json()['data']['items']

    def get_all_sence(self):
        """Get sence list.

        Returns:
            [list]: {
                    "unique_id": "gRoz2Xx0AKhDjTyz1WRfFBx2wlaA5AGy",
                    "mode": "image2d-tracking",
                    "name": "fv",
                    "status": 2,
                    "thumbnail_url": "https://kivicube-thumbnail.kivisense.com/marker/f8KDOczODzZyE_bJ8y6dY872OU13zN_f.jpg?unique=1574533839",
                    "marker_url": ["https://kivicube-thumbnail.kivisense.com/marker/f8KDOczODzZyE_bJ8y6dY872OU13zN_f.jpg?unique=1574533839"],
                    "match_level": 4,
                    "asset_convert_status": null
                }
        """
        url = 'https://cloud.kivicube.com/api/scene/index'

        req = self.session.get(url=url)
        if req.status_code == 200:
            return req.json()['data']['items']

    def delete(self, delete_type='project', **kwargs):
        """delete project, sence, asset.
        use uid to kwargs, will delete uid sence.

        Args:
            delete_type (str, optional): project or asset or sence.
                     Defaults to 'project'.
        """
        if kwargs.get('uid', False):
            url = 'https://cloud.kivicube.com/api/scene/delete'
            self.session.delete(
                url=url, params={'id': kwargs.get('uid', False)})
        if delete_type == "project":
            kivicube_log.debug(msg='delete all project ')
            delete_data = self.get_project(force_renew=True)
            key_name = "id"
            method = 'post'
            url = 'https://cloud.kivicube.com/project/delete'
        elif delete_type == "asset":
            kivicube_log.debug(msg='delete all asstet')
            delete_data = self.get_all_asset()
            key_name = "id"
            method = 'delete'
            url = 'https://cloud.kivicube.com/materials/delete'  # asset
        elif delete_type == 'sence':
            kivicube_log.debug(msg='delete all sence')
            delete_data = self.get_all_sence()
            key_name = "unique_id"
            method = 'delete'
            url = 'https://cloud.kivicube.com/api/scene/delete'
        if method == 'post':
            for i in delete_data:
                self.session.post(url=url, params={'id': i[key_name]})
        elif method == 'delete':
            for i in delete_data:
                self.session.delete(url=url, params={'id': i[key_name]})

    def upload_asset(self, file, upload_type='marker'):
        """Upload livicube asset.

        Args:
            file ([open]): open('abc.jpg','rb'), If use in backend, use tempfile library.
            upload_type (str, optional): Marker or normal image. Defaults to 'marker'.

        Returns:
            [dict]: asset data
            image {'id': 12045, 'title': 'maple.jpg', 'identify': 'arbaxfV_KBgy44_LBS-8y-cUaOLRM9nI', 'type': 'image', 'description': None, 'updatedAt': 1574593589, 'suffix': 'jpg', 'thumbnails': 'https://kivicube-thumbnail.kivisense.com/image/arbaxfV_KBgy44_LBS-8y-cUaOLRM9nI.jpg?unique=1574593589', 'info': {'width': 600, 'height': 396, 'RP': '600x396', 'format': 'jpg', 'name': 'maple.jpg', 'size': 117737}, 'image': 'https://kivicube-asset.kivisense.com/image/base/1.0/unify/arbaxfV_KBgy44_LBS-8y-cUaOLRM9nI.jpg?OSSAccessKeyId=LTAIEq1suktu3c0O&Expires=1574679989&Signature=OOhRAyPECPfdQzqFRgK6Oq6h69s%3D', 'materialPackStatus': None, 'width': 600, 'height': 396}
            marker{'id': 12051, 'title': 'maple.jpg', 'identify': 'Jr4530jD3mx59OXz9jKO-9UIlgvsuvLU', 'type': 'marker', 'description': None, 'updatedAt': 1574594504, 'suffix': 'jpg', 'thumbnails': 'https://kivicube-thumbnail.kivisense.com/marker/Jr4530jD3mx59OXz9jKO-9UIlgvsuvLU.jpg?unique=1574594504', 'info': {'width': 600, 'height': 396, 'level': 5, 'RP': '600x396', 'format': 'jpg', 'name': 'maple.jpg', 'size': 83007}, 'marker': 'https://kivicube-asset.kivisense.com/marker/base/1.0/unify/Jr4530jD3mx59OXz9jKO-9UIlgvsuvLU.jpg?OSSAccessKeyId=LTAIEq1suktu3c0O&Expires=1574680904&Signature=IZhPmasxww8ZLsb1V8G6g%2FlMwXo%3D', 'materialPackStatus': 2, 'level': 5, 'width': 600, 'height': 396}
        """
        url = 'https://cloud.kivicube.com/materials/upload'
        files = {'file': file}
        if upload_type == 'marker':
            values = {'type': 'marker'}
        elif upload_type == 'image':
            values = {'type': 'image'}
        req = self.session.post(url=url, files=files, data=values)
        if req.status_code == 200:
            req_json = req.json()
        if req_json['code'] == 200:
            return req_json['data']
        else:
            kivicube_log.debug(msg='Upload file error, error msg: {}'.format(
                "".join(i for i in req_json['message']['file'])))
        return None

    def marker_convert(self, marker_id):
        """Call kivicube to create marker file.
        
        Args:
            marker_id ([str]): marker id.
        """        
        url = 'https://cloud.kivicube.com/api/asset/marker-convert'
        self.session.get(url=url, params={"identify": marker_id})


if __name__ == "__main__":
    user = kivicube_account(
        username='', password='')

    print(user.get_project())
