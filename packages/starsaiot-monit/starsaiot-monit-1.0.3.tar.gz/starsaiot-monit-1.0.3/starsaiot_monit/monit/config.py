import os
from time import sleep

import requests, json
from starsaiot_monit.logger import logger

class Config:
    def __init__(self):
        logger.info("config init ..")

        self._conf_dir = os.path.abspath(os.path.join(os.getcwd())) + '/config'
        self._monitJson = self.setMonitJson()
        # self.dynamicRegister()

    def setMonitJson(self):
        with open(self._conf_dir + '/monit.json', 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def getMonitJson(self):
        if self._monitJson == {}:
            with open(self._conf_dir + '/monit.json', 'r', encoding='utf-8') as f:
                return json.loads(f.read())
        return self._monitJson

    def dynamicRegister(self):
        url = 'http://device.starsaiot.com:9600/hercules/open/api/v1/device/monitor/dynamicRegister'
        data = json.dumps({
            'deviceSn': '20221210',
            'deviceName': '20221210test',
            'runFirewareVersion': '0.1.0',
            'devModel': '1',
            'runAppVersionCode': '1',
            'runAppVersionName': '0.1.0',
        })
        # 设置请求头
        headers = {"content-type": "application/json"}
        response = requests.post(url, data, headers = headers)
        text = json.loads(response.text)
        logger.info(text)
        if(response.status_code == 200 and text['success']):
            self._monitJson['deviceId'] = text['content']['deviceId']
            self._monitJson['deviceToken'] = text['content']['deviceToken']
            with open(self._conf_dir + '/monit.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(self._monitJson))

monitJson = Config()