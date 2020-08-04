import json
json_file = """{
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
}"""


def hidden(jfile):
    print('call')
    if isinstance(jfile, list):
        for i, v in enumerate(jfile):
            if isinstance(v, dict):
                hidden(jfile[i])
            elif isinstance(v, list):
                hidden(jfile[i])

            elif str(v).find("https://") > -1:
                jfile[i] = None
    elif isinstance(jfile, dict):
        for key, value in jfile.items():
            if isinstance(value, dict):
                hidden(jfile[key])

            elif str(value).find("https://") > -1:
                jfile[key] = None
    return jfile


if __name__ == "__main__":
    jsd = json.loads(json_file)
    hd = hidden(jsd)
    print(json.dumps(hd))
