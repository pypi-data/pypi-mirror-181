#!/usr/bin/env python
#coding:utf-8
import os
import string
import json
import random
import time
import subprocess
import traceback
from threading import Thread
from paho.mqtt.client import Client
from time import sleep, strftime
from starsaiot_monit.logger import logger
from starsaiot_monit.monit.config import monitJson
from starsaiot_monit.monit.md5 import get_file_md5
from starsaiot_monit.monit.sftp import MySftp

mqtt_config = {
    "name": "Default Local Broker",
    "host": "device.starsaiot.com",
    "port": 1883,
    "keepalive": 60,
    "security": {
      "type": "basic",
      "username": "monitorAndroid",
      "password": "@ycwlmonitor3147"
    }
}

class MqttConnector(Thread):
    def __init__(self, deviceId):
        super().__init__()

        self.__mqtt_config = mqtt_config
        self.__log = logger
        self.__monitJson = monitJson.getMonitJson()

        client_id = "linux_" + deviceId + "_" + str(int(time.mktime(time.localtime(time.time()))))
        logger.info("client_id: " + client_id)
        self._client = Client(client_id)
        self.setName(mqtt_config.get("name") + 'Mqtt Broker ' + ''.join(random.choice(string.ascii_lowercase) for _ in range(5)))
        self._client.username_pw_set(self.__mqtt_config["security"]["username"],
                                     self.__mqtt_config["security"]["password"])

        # Set up external MQTT broker callbacks ------------------------------------------------------------------------
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_subscribe = self._on_subscribe
        self._client.on_disconnect = self._on_disconnect
        # self._client.on_log = self._on_log

        self._gw_subscriptions = {}

        # Set up lifecycle flags ---------------------------------------------------------------------------------------
        self._connected = False
        self.__stopped = False

    def get_name(self):
        return self.name

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        try:
            self.__connect()
        except Exception as e:
            self.__log.exception(e)
            try:
                self.close()
            except Exception as e:
                self.__log.exception(e)

        while True:
            if self.__stopped:
                break
            elif not self._connected:
                self.__connect()
            # self.__threads_manager()

            sleep(.01)
        # self.__connect()

    def __connect(self):
        while not self._connected and not self.__stopped:
            try:
                self._client.connect(self.__mqtt_config['host'],
                                     self.__mqtt_config.get('port', 1883), self.__mqtt_config['keepalive'])
                self._client.loop_start()
                if not self._connected:
                    sleep(1)
            except ConnectionRefusedError as e:
                self.__log.error(e)
                sleep(10)

    def close(self):
        self.__stopped = True
        try:
            self._client.disconnect()
        except Exception as e:
            logger.exception(e)
        self._client.loop_stop()
        self.__log.info('%s has been stopped.', self.get_name())


    def _on_connect(self, client, userdata, flags, result_code, *extra_params):
        if result_code == 0:
            self._connected = True
            self.__log.info('%s connected to %s:%s - successfully.',
                            self.get_name(),
                            self.__mqtt_config["host"],
                            self.__mqtt_config.get("port", "1883"))

            self.__log.debug("Client %s, userdata %s, flags %s, extra_params %s",
                             str(client),
                             str(userdata),
                             str(flags),
                             extra_params)

            self.subscribe("/python/test02")
            # self._client.subscribe("/device/log/1ed785944e2a5f38afd27b8d1ce0f61")
            # self.subscribe("/device/log/1ed785944e2a5f38afd27b8d1ce0f61")
            # self.sendMsg("/python/test01", "qweqweqweqw", 0)

            # topic = "/python/test01"
            # result = self._client.publish(topic, "qweweqweqeqeqeq")

    def getConneted(self):
        return self._connected

    def _on_disconnect(self, *args):
        self._connected = False
        self.__log.debug('"%s" was disconnected. %s', self.get_name(), str(args))

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        subscription = self._gw_subscriptions.get(mid)
        if subscription is not None:
            if mid == 128:
                logger.error("Service subscription to topic %s - failed.", subscription)
                del self._gw_subscriptions[mid]
            else:
                logger.debug("Service subscription to topic %s - successfully completed.", subscription)
                del self._gw_subscriptions[mid]

    def _on_message(self, client, userdata, message):
        logger.info(f"Received `{message.payload.decode()}` from `{message.topic}` topic")
        msg = json.loads(message.payload.decode())
        if message.topic == '/device/log/' + self.__monitJson['deviceId']:
            self.logHandler(msg)
        elif message.topic == '/device/app/' + self.__monitJson['deviceId']:
            self.appHandler(msg)




    def sendMsg(self, topic, data, qos):
        result = self._client.publish(topic, data, qos)
        status = result[0]
        if status == 0:
            print(topic)
            print(data)
            # logger.info(f"Send `{data}` to topic `{topic}`")
        else:
            logger.info(f"Failed to send message to topic {topic}")

    def subscribe(self, topic):
        self._gw_subscriptions[
            int(self._client.subscribe(topic, qos=1)[1])] = topic

    def logHandler(self, msg):
        current_time = strftime('%Y-%m-%d %H:%M:%S')
        msgBody = json.loads(msg['msgBody'])
        if msg['msgKey'] == 'selectDir':
            _msg = {}
            msg_body = []
            log_dir = ''
            try:
                if msgBody['logType'] == 4:
                    log_dir = os.path.abspath(os.path.join(os.getcwd())) + '/logs'
                elif msgBody['logType'] == 5:
                    log_dir = msgBody['targetPath']
                for file_name in os.listdir(log_dir):
                    fileObj = {}
                    fileObj['fileName'] = file_name
                    file_md5 = get_file_md5(log_dir + "/" + file_name)
                    fileObj['fileMd5'] = file_md5
                    msg_body.append(fileObj)
            except Exception as e:
                logger.exception(e)

            msg_body.sort(key=lambda x:x["fileName"], reverse=True)

            _msg['msgBody'] = msg_body
            _msg['deviceId'] = msg['deviceId']
            _msg['id'] = 2
            _msg['msgId'] = msg['msgId']
            _msg['msgKey'] = 'selectFile'
            _msg['msgTopic'] = '\/sys\/platform\/device\/ack'
            _msg['msgVersion'] = 'V3.0.0'
            _msg['sendTime'] = current_time
            _msg['tenantId'] = msg['tenantId']

            data = json.dumps(_msg)
            # print(data)
            self.sendMsg("/sys/platform/device/ack", data, 0)
        elif msg['msgKey'] == 'logUpload':
            self.__log_upload_msg = msg
            _msg = {}
            log_dir = ''
            try:
                if msgBody['logType'] == 4:
                    log_dir = os.path.abspath(os.path.join(os.getcwd())) + '/logs/'
                elif msgBody['logType'] == 5:
                    log_dir = msgBody['targetPath'] + '/'
            except Exception as e:
                logger.exception(e)

            file_path = (log_dir + msgBody['fileName']).replace('/', os.path.sep)
            remote_path = msgBody['sftpPath'] + msg['deviceId'] + '/' + msgBody['fileName']

            logger.info(file_path)
            logger.info(remote_path)

            my_sftp = MySftp()
            client, sftp = my_sftp.sftp_connect()
            try:
                sftp.put(file_path, remote_path, self.logUploadCallback)  # 上传文件
            except Exception as e:
                logger.exception(e)
                msg_body = {}
                msg_body['step'] = 'uploadFailure'
                msg_body['action'] = 'uploadFailure'
                msg_body['recordId'] = msgBody['recordId']
                msg_body['errorLog'] = str(e)

                _msg['msgBody'] = msg_body
                _msg['deviceId'] = msg['deviceId']
                _msg['id'] = 3
                _msg['msgId'] = msg['msgId']
                _msg['msgKey'] = 'logUpload'
                _msg['msgTopic'] = '\/sys\/platform\/device\/ack'
                _msg['msgVersion'] = 'V3.0.0'
                _msg['sendTime'] = current_time
                _msg['tenantId'] = msg['tenantId']

                data = json.dumps(_msg)
                self.sendMsg("/sys/platform/device/ack", data, 0)
            client.close()

    def get_my_key(obj):
        return obj['size']

    def logUploadCallback(self, up_byte, total_byte):
        current_time = strftime('%Y-%m-%d %H:%M:%S')
        progress = int(up_byte/total_byte * 100)
        _msg = {}
        msg_body = {}
        msg_body['step'] = 'handleUpload'
        msg_body['action'] = 'handleUpload'
        if progress >= 100:
            msg_body['step'] = 'uploadSuccess'
            msg_body['action'] = 'uploadSuccess'

        msg_body['progress'] = progress
        msg_body['recordId'] = json.loads(self.__log_upload_msg['msgBody'])['recordId']

        _msg['msgBody'] = msg_body
        _msg['deviceId'] = self.__log_upload_msg['deviceId']
        _msg['id'] = 3
        _msg['msgId'] = self.__log_upload_msg['msgId']
        _msg['msgKey'] = 'logUpload'
        _msg['msgTopic'] = '\/sys\/platform\/device\/ack'
        _msg['msgVersion'] = 'V3.0.0'
        _msg['sendTime'] = current_time
        _msg['tenantId'] = self.__log_upload_msg['tenantId']
        data = json.dumps(_msg)
        self.sendMsg("/sys/platform/device/ack", data, 0)

    def appHandler(self, msg):
        current_time = strftime('%Y-%m-%d %H:%M:%S')
        msgBody = json.loads(msg['msgBody'])
        if msg['msgKey'] == 'appUpgrade':
            _msg = {}
            msg_body = {}
            appVersionName = msgBody['appVersionName']
            packageName = msgBody['packageName']
            taskId = msgBody['taskId']

            msg_body['laterVersionCode'] = '1'
            msg_body['laterVersionName'] = '1.0.0'
            msg_body['action'] = 'installSuccess'
            msg_body['taskId'] = taskId

            _msg['msgBody'] = msg_body
            _msg['deviceId'] = msg['deviceId']
            _msg['id'] = 4
            _msg['msgId'] = msg['msgId']
            _msg['msgKey'] = 'appUpgrade'
            _msg['msgTopic'] = '\/sys\/platform\/device\/ack'
            _msg['msgVersion'] = 'V3.0.0'
            _msg['sendTime'] = current_time
            _msg['tenantId'] = msg['tenantId']
            data = json.dumps(_msg)
            self.sendMsg("/sys/platform/device/ack", data, 0)


if __name__ == '__main__':
    # run()
    mq = MqttConnector()
    mq.open()


