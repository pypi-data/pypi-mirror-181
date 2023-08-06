import logging
import traceback

import requests

logger = logging.getLogger("main")


class STFServer(object):

    def __init__(self, url=None, token=None):
        self.device_url = url
        self.devices_list = []
        self.token = token

    def requests_stf(self, uri, type='get', body=None, is_log=True):
        headers = {'Authorization': 'Bearer ' + self.token, 'User-Agent': 'User-Agent:Mozilla/5.0'}
        url = self.device_url + '/api/v1/' + uri
        if type == 'post':
            resp = requests.post(url, headers=headers, json=body, timeout=20 * 60)
        elif type == 'delete':
            resp = requests.delete(url, headers=headers, timeout=20 * 60)
        else:
            resp = requests.get(url, headers=headers, timeout=20 * 60)
        try:
            resp = resp.json()
        except Exception as e:
            logger.info(f'type = {type}, uri = {uri}, body = {body}, resp= {resp.text}, e= {e}')
            raise e
        if is_log:
            logger.info(f'type = {type}, uri = {uri}, body = {body}, resp= {resp}')
        return resp

    def get_devices(self):
        return self.requests_stf("devices", is_log=False)['devices']

    def get_device(self, serial):
        try:
            url = "devices/" + serial
            ret_json = self.requests_stf(url, is_log=False)
            if 'device' in ret_json:
                return ret_json['device']
            else:
                return None
        except Exception as e:
            return None

    def present_ios_devices(self):
        all_devices = self.get_devices()
        devices = []
        for d in all_devices:
            if d['present'] and d.get('platform', 'None').lower() == 'ios':
                d['wda_url'] = "http://" + d['webRemoteUrl'].split(':')[0] + ':' + d['wdaPort']
                devices.append(d)
        return devices

    def present_android_devices(self):
        all_devices = self.get_devices()
        devices = []
        for d in all_devices:
            if d['present'] and d.get('platform', 'None').lower() == 'android':
                devices.append(d)
        if len(devices) > 0:
            return [self.get_device(d['serial']) for d in devices]
        else:
            return []

    def get_device_info(self, serial, platform="android"):
        if platform == "android":
            for item in self.present_android_devices():
                if item['serial'] == serial:
                    return item
        elif platform == "ios":
            for item in self.present_ios_devices():
                if item['serial'] == serial:
                    return item
        return None

    def get_session_id(self, wda_url):
        """
        获取设备的session id
        """
        res = requests.get(wda_url + '/status', timeout=30)
        return res.json().get("sessionId", None)

    def launch_ios_app(self, wda_url, bundle_id, args=[]):
        """
         启动iOS APP
        """

        params = {"desiredCapabilities": {"bundleId": bundle_id}}
        if len(args) > 0:
            params['desiredCapabilities']['arguments'] = args
        try:
            resp = requests.post("{}/wda/apps/launchapp".format(wda_url),
                                 json=params, timeout=60)
            logger.info('{} launch app {} result:{}'.format(wda_url, bundle_id, resp.text))
        except Exception:
            logger.error("launch_ios_app error:{}".format(traceback.format_exc()))

    def stop_ios_app(self, wda_url, bundle_id):
        """
         停止iOS APP
        """
        try:
            resp = requests.post("{}/wda/apps/terminateapp".format(wda_url),
                                 json={"bundleId": bundle_id}, timeout=60)
            logger.info('{} stop app {} result:{}'.format(wda_url, bundle_id, resp.text))
        except Exception:
            logger.error("stop_ios_app error:{}".format(traceback.format_exc()))

    def get_device_ip(self, wda_url, platform="ios"):
        if platform == "ios":
            url = wda_url + "/status"
            resp = requests.get(url)
            if resp.status_code == 200:
                return resp.json()['value']['ios']['ip']
            else:
                return None

    def watch_alert(self, wda_url):
        defaultAlertAction = "[{\"regex\": \".*已经可以安装。$\", \"index\": 1},\
                              {\"regex\": \"^接入电源时.*可在以下时间段自动更新.*\", \"index\": 0},\
                              {\"regex\": \"^允许.*使用无线数据.*\", \"index\": 0},\
                              {\"regex\": \"^将.*用于iMessage信息和FaceTime通话.*\", \"index\": 0},\
                              {\"regex\": \"无法验证服务器身份\", \"index\": 1},\
                              {\"regex\": \".*想给您发送通知$\", \"index\": 0},\
                              {\"regex\": \"验证Apple ID\", \"index\": 0},\
                              {\"regex\": \"无法验证App\", \"index\": 0},\
                              {\"regex\": \"要信任此电脑吗.*\", \"index\": 0},\
                              {\"regex\": \".*\", \"btns\": [\"加入\",\"允许\", \"无线局域网与蜂窝.*\", \
                              \"稍后\", \"以后.*\",\"OK\",\"好\", \"关闭.*\",\"下载\",\
                              \"稍后提醒.*\",\"信任\",\"使用App时允许\",\"允许访问所有照片\"]}]"
        body = {
            'capabilities': {
                'firstMatch': [
                    {
                        'defaultAlertAction': defaultAlertAction
                    }
                ]
            }
        }
        uri = f'{wda_url}/session'
        try:
            resp = requests.post(uri, json=body, timeout=30)
            logger.info(resp.text)
            return True
        except Exception:
            logger.error("watch_alert error:{}".format(traceback.format_exc()))
            return False

    def toggleAndroidWifi(self, serial, type, wifiname="", wifipass=""):
        """
        :param serial 设备序列号
        :param type 1:连接wifi 2:关闭wifi(api<29) 3:断开指定wifi连接
        :param wifiname
        :param wifipass
        :return
        """
        body = {
            "type": type,
            "serial": serial,
            "wifiname": wifiname,
            "wifipass": wifipass
        }
        uri = "user/device/togglewifi"
        resp = self.requests_stf(uri, type="post", body=body)
        return resp

    def find_ios_bundle_id(self, serial, bundle_id):
        body = {"serial": serial}
        uri = "user/device/apps"
        app_list = self.requests_stf(uri, type="post", body=body)
        if "appList" not in app_list:
            return None
        for app_info in app_list['appList']:
            if bundle_id in app_info:
                return app_info.split(" ")[0].split(":")[1]
        return None

    def get_android_device_ip(self, serial):
        try:
            data = self.requests_stf('user/device/getwifiip?serial=' + serial)
            return data.get('ip', None)
        except Exception:
            logger.error('Failed to get android device ip: {}'.format(serial))
            return None
