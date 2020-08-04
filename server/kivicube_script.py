from kivicube_account import kivicube_account
from kivicube_client import kivicube_viewer
import logging
import util
import redis
import json
import time
import config
import threading
logging.basicConfig(level=logging.INFO)

console = logging.StreamHandler()
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
kivicube_log = logging.getLogger("kivicube_function")
red_string = redis.StrictRedis.from_url(
    url=config.REDIS_URL, db=4, charset="utf-8", decode_responses=True)


def create_AR_to_output(user, viewer, detection_image, show_image):
    """create AR

    Args:
        user ([kivicube_account]): kivicube_account class must be login.
        viewer ([kivicube_viewer]): Just requests client.
        detection_image ([str]): filename
        show_image ([str]): filename

    Returns:
        [dict]: {
                "code": 200,
                "data": {
                    "unique_id": "GHhkKRzhpwCbem7km3qaKdKzjHNIrst8",
                    "mode": "image2d-tracking",
                    "status": 2,
                    "setting": {
                        "metadata": {
                            "html_title": "Dhp9NhMFM9ajC",
                            "share": {
                                "title": "Dhp9NhMFM9ajC",
                                "description": "hi 9",
                                "picture": null,
                                "picture_url": "https://kivicube-resource.kivisense.com/sharePicture/default.png"
                            }
                        },
                        "gyroscope": false,
                        "jump_scan": false,
                        "unsupport_webrtc": {
                            "downgrade_web3d": false,
                            "choose_image_scan": false
                        },
                        "deny_camera_downgrade_web3d": false,
                        "experience_camera": "open",
                        "render_camera": {
                            "target": {
                                "x": 0,
                                "y": 0,
                                "z": 0
                            },
                            "position": {
                                "x": -2.698924,
                                "y": 1.876875,
                                "z": 2.818165
                            },
                            "horizontal_fov": 60
                        },
                        "env_map": {
                            "built_in_type": "main-extra",
                            "reflectivity": 1
                        },
                        "first_page": {
                            "background_image": null,
                            "logo": null,
                            "hide_logo_and_scene_name": false,
                            "button": null,
                            "background_image_url": "",
                            "logo_url": "",
                            "button_url": ""
                        }
                    },
                    "name": "fv",
                    "marker": [
                        {
                            "id": 1,
                            "type": "match",
                            "asset_unique_id": "04BnWhh4VaA1FL0WsRfTGCtxwgnWP-HX"
                        }
                    ],
                    "event": [],
                    "object": [
                        {
                            "id": 1,
                            "name": "UDJU4BxwehIpx",
                            "type": "image",
                            "asset_unique_id": "HXJiMV0DnKQB-mBnvcOKaZd-KC9goFwl",
                            "position": {
                                "x": 0,
                                "y": 1.051,
                                "z": 0
                            },
                            "rotation": {
                                "x": -90,
                                "y": 0,
                                "z": 0
                            },
                            "scale": {
                                "x": 1,
                                "y": 1,
                                "z": 1
                            },
                            "visibility": true,
                            "event": [],
                            "setting": []
                        }
                    ],
                    "collection": {
                        "unique_id": "g8yld_",
                        "name": "kZ1Hm3gFogexsV1F"
                    },
                    "asset": [
                        {
                            "id": 12065,
                            "title": "dec.jpg",
                            "identify": "04BnWhh4VaA1FL0WsRfTGCtxwgnWP-HX",
                            "type": "marker",
                            "description": "",
                            "updatedAt": 1574595050,
                            "suffix": "jpg",
                            "thumbnails": "https://kivicube-thumbnail.kivisense.com/marker/04BnWhh4VaA1FL0WsRfTGCtxwgnWP-HX.jpg?unique=1574595050",
                            "info": {
                                "width": 512,
                                "height": 512,
                                "level": 3,
                                "RP": "512x512",
                                "format": "jpg",
                                "name": "dec.jpg",
                                "size": 32959
                            },
                            "marker": "https://kivicube-asset.kivisense.com/marker/base/1.0/unify/04BnWhh4VaA1FL0WsRfTGCtxwgnWP-HX.jpg?OSSAccessKeyId=LTAIEq1suktu3c0O&Expires=1574681451&Signature=ZZ4FpzAQ35Jflc1dXZcCNTfHs5A%3D",
                            "materialPackStatus": 2,
                            "level": 3,
                            "width": 512,
                            "height": 512
                        },
                        {
                            "id": 12064,
                            "title": "maple.jpg",
                            "identify": "HXJiMV0DnKQB-mBnvcOKaZd-KC9goFwl",
                            "type": "image",
                            "description": "",
                            "updatedAt": 1574595049,
                            "suffix": "jpg",
                            "thumbnails": "https://kivicube-thumbnail.kivisense.com/image/HXJiMV0DnKQB-mBnvcOKaZd-KC9goFwl.jpg?unique=1574595049",
                            "info": {
                                "width": 600,
                                "height": 396,
                                "RP": "600x396",
                                "format": "jpg",
                                "name": "maple.jpg",
                                "size": 117737
                            },
                            "image": "https://kivicube-asset.kivisense.com/image/base/1.0/unify/HXJiMV0DnKQB-mBnvcOKaZd-KC9goFwl.jpg?OSSAccessKeyId=LTAIEq1suktu3c0O&Expires=1574681451&Signature=kOrlnnmkoS7CoDEWW5jBGS7e75Q%3D",
                            "materialPackStatus": null,
                            "width": 600,
                            "height": 396
                        }
                    ],
                    "thumbnail_url": "https://kivicube-thumbnail.kivisense.com/marker/04BnWhh4VaA1FL0WsRfTGCtxwgnWP-HX.jpg?unique=1574595050"
                },
                "message": ""
            }
        [bool]: False.
    """
    show_image_response = user.upload_asset(
        file=open(show_image, 'rb'), upload_type='image')
    detection_image_response = user.upload_asset(
        file=open(detection_image, 'rb'), upload_type='marker')
    if show_image_response == None or detection_image_response == None:
        return False
    user_project = user.get_project(force_renew=True)
    if len(user_project) < 1:
        user.create_project()
        user_project = user.get_project(force_renew=True)

    url = 'https://cloud.kivicube.com/api/editor/create-scene'

    post_data_template = '{{"unique_id":-1,"mode":"image2d-tracking","collection":{{"name":"{project_name}","unique_id":"{project_id}"}},"status":2,"setting":{{"metadata":{{"html_title":"{title}","share":{{"title":"{title}","description":"hi 9","picture_url":""}}}},"gyroscope":false,"jump_scan":false,"unsupport_webrtc":{{"downgrade_web3d":false,"choose_image_scan":false}},"deny_camera_downgrade_web3d":false,"experience_camera":"open","render_camera":{{"target":{{"x":0,"y":0,"z":0}},"position":{{"x":-2.6989239999999994,"y":1.8768750000000003,"z":2.818164999999999}},"horizontal_fov":60}},"env_map":{{"built_in_type":"main-extra","reflectivity":1}},"first_page":{{"background_image_url":"","logo_url":"","hide_logo_and_scene_name":false,"button_url":""}}}},"name":"{random_text}","marker":[{{"id":1,"type":"match","asset_unique_id":"{marker_id}"}}],"event":[],"object":[{{"name":"{random_text}","type":"image","id":1,"visibility":true,"rotation":{{"x":-90,"y":0,"z":0}},"scale":{{"x":1,"y":1,"z":1}},"position":{{"x":0,"y":1.051,"z":0}},"setting":{{"self_rotate":false,"auto_play":false,"loop":false,"full_screen":false,"animation_name":""}},"asset_unique_id":"{asset_id}","event":[]}}]}}'

    data = post_data_template.format(
        project_name=user_project[0]['name'],
        project_id=user_project[0]['uniqid'],
        title=util.randStr(13),
        marker_id=detection_image_response['identify'],
        asset_id=show_image_response['identify'],
        random_text=util.randStr(13),
    )

    req = user.session.post(url=url, data=data, headers={
        "content-type": "application/json; charset=UTF-8"})
    # create done.

    if req.status_code == 200:
        req_json = req.json()
        if req_json['code'] != 200:
            kivicube_log.warning(msg='CreateAR error.')
            return False

    marker_convert = threading.Thread(target=user.marker_convert, args=(
        detection_image_response['identify'],))
    marker_convert.start()
    # kivicube_log.warning(msg=req_json['data']['unique_id'])

    # download asset to host
    view_json = viewer.get_view_json(unique_id=req_json['data']['unique_id'])
    if view_json == False:
        kivicube_log.warning(msg='Get view json error.')
        return False

    threading.Thread(target=viewer.download_asset__file,
                     args=(show_image_response['identify'], 'image')).start()

    # wait marker make.
    wait_time = 0
    while marker_convert.isAlive():
        time.sleep(1)
        wait_time += 1
        kivicube_log.debug(msg="wait marker convert")
        if wait_time > 30:
            kivicube_log.warning(msg='marker convert timeout ')
            break
    threading.Thread(target=viewer.download_asset__file,
                     args=(detection_image_response['identify'], 'marker')).start()
    # save sence file to redis
    red_string.set(name=req_json['data']
                   ['unique_id'], value=json.dumps(view_json))

    # WARRING
    # delete sence, if marker convert change to async,
    # need check have any effective after delete
    user.delete(uid=req_json['data']['unique_id'])

    return req_json['data']['unique_id']


if __name__ == "__main__":
    kivicube_user = kivicube_account(
        username='', password='')
    kivi_viewer = kivicube_viewer()
    kivicube_user.delete(delete_type='sence')
    # kivicube_user.delete(delete_type='asset')
    create_AR_to_output(user=kivicube_user, viewer=kivi_viewer, detection_image='dec.jpg',
                        show_image='maple.jpg')
