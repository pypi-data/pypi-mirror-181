# -*- coding: utf-8 -*-
from enum import Enum, unique
import json
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError
import base64
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

__version__ = '2.9.8'
__all__ = ['RequestType', 'Core', 'aes_decrypt', 'jd_concat']


@unique
class RequestType(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'


_timeout = (3.05, 27)   # 超时时间, 连接超时 和 读取超时
# _timeout = None


class Core:
    def __init__(self,
                 api_key=None,      # 秘钥 key
                 logger=None,       # 日志
                 proxy=None,        # 代理
                 gate_way='',       # 网关， 网关 + path 构成请求接口地址
                 ):
        self._proxy = proxy
        self._api_key = api_key
        self._gate_way = gate_way
        self._logger = logger

    def request(self, path, method=RequestType.GET, data=None, files=None, headers=None,
                show_url=True, show_response=True, force_data=False,
                show_request=True, show_rsp=True):
        """
        请求 POST 、GET
        :param path:            接口 路径， 网关 + path 构成请求接口地址
        :param method:          POST、GET(default method)
        :param data:            请求数据
        :param files:           请求文件
        :param headers:         请求头
        :param show_request:    是否显示请求信息，包括 url， POST/GET类型，头部，请求参数。 True-显示， False-不显示
        :param show_url:        是否在日志显示 url。 优先级小于 show_request
        :param show_rsp:        是否在日志显示接口返回所有内容（状态码，header，text）。 True-显示， False-不显示
        :param show_response:   是否在日志显示接口返回内容。优先级小于 show_rsp
        :param force_data:      按 字节方式传递 data
        :return:    (status_code, message)
        """
        if headers is None:
            headers = {}
        if files:
            headers.update({'Content-Type': 'multipart/form-data'})
        else:
            headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update({'User-Agent': 'jd-wechatpay v3 python sdk'})
        netloc = path.find("://", 4, 8)  # http:// or https://.  '://' start begin 4 or 5
        if netloc > 0:  # path 为完成 url，含有域名
            url = path
        else:  # path 为路径
            url = jd_concat(self._gate_way, path)   # 网关 + 路径 构成 发送 url
        if self._logger and show_request:  # 显示请求信息
            if show_url:
                self._logger.debug('Request url: %s' % url)
            self._logger.debug('Request type: %s' % method.value)
            self._logger.debug('Request headers: %s' % headers)
            self._logger.debug('Request params: %s' % data)
        try:
            if method == RequestType.GET:
                response = requests.get(url=url, params=data, headers=headers, proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.POST:
                para_json = None if force_data or files else data
                para_byte = data if force_data or files else None
                if force_data and isinstance(para_byte, (str, dict)):   # 字符串、字典 转 byte
                    para_byte = json.dumps(para_byte, ensure_ascii=False).encode("utf-8")
                response = requests.post(url=url, json=para_json, data=para_byte, headers=headers, files=files,
                                         proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.PATCH:
                response = requests.patch(url=url, json=data, headers=headers, proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.PUT:
                response = requests.put(url=url, json=data, headers=headers, proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.DELETE:
                response = requests.delete(url=url, headers=headers, proxies=self._proxy, timeout=_timeout)
            else:
                raise Exception('sdk does no support this request type.')
        except (TimeoutError, requests.exceptions.ConnectionError, MaxRetryError, NewConnectionError):
            return 500, {'code': 500, 'msg': 'Timeout Error'}
        if self._logger and show_request and show_url:  # 真实 url
            self._logger.debug('--- Request [real] url: %s' % response.url)
        if self._logger and show_rsp:
            self._logger.debug('Response status code: %s' % response.status_code)
            self._logger.debug('Response headers: %s' % response.headers)
            if show_response:
                self._logger.debug('Response content: %s' % response.text)
        if response.status_code == 404:
            return response.status_code, {'code': response.status_code, 'msg': response.text}
        elif response.status_code in [405]:
            return response.status_code, {'code': response.status_code, 'msg': 'Method Not Allowed'}
        content_type = response.headers.get('Content-Type')
        if content_type in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'audio/mp3', 'video/mpeg']:
            message = response.content
        else:
            message = response.text if content_type and 'application/json' in content_type else response.content
            try:
                if isinstance(message, str):
                    message = json.loads(message)
                elif isinstance(message, bytes):
                    message = json.loads(message.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                message = {}
            except UnicodeDecodeError:
                pass
        return response.status_code, message

    def decrypt_callback(self, headers, body):
        """
        通知的数据会加密 post 到对接方接口中，由于涉及到回调加密和解密，接入方必须先通过微校商务侧申请
        通知秘钥 key，申请好通知秘钥 key 后才能解密回调通知
        :param headers:
        :param body:
        :return:
        """
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
        if self._logger:
            self._logger.debug('Callback Header: %s' % headers)
            self._logger.debug('Callback Body: %s' % body)
        data = json.loads(body)
        resource_type = data.get('resource_type')
        if resource_type != 'encrypt-resource':
            return None
        resource = data.get('resource')
        if not resource:
            return None
        algorithm = resource.get('algorithm')
        if algorithm != 'AEAD_AES_256_GCM':
            raise Exception('sdk does not support this algorithm')
        nonce = resource.get('nonce')
        ciphertext = resource.get('ciphertext')
        associated_data = resource.get('associated_data')
        if not (nonce and ciphertext):
            return None
        if not associated_data:
            associated_data = ''
        result = aes_decrypt(
            nonce=nonce,
            ciphertext=ciphertext,
            associated_data=associated_data,
            notify_key=self._api_key)
        if self._logger:
            self._logger.debug('Callback resource: %s' % result)
        return result


def jd_concat(url: str, path: str):
    """
    url 合并， 去掉重复的 / 字符
    :param url:     url 网关，例如： 'https://domain.com
    :param path:    请求路径，例如： '/some_path/books_get'
    :return:    合并后的路径  url + path，去掉 多余 字符('/')
    """
    if url and path:
        n = 1 if url[-1] == '/' else 0
        if path[0] == '/':
            n += 1

        if 2 == n:
            return url + path[1:]
        elif 0 == n:
            return f"{url}/{path}"

    return (url or '') + (path or '')


def aes_decrypt(nonce, ciphertext, associated_data, notify_key):
    """
    微卡 订单流水实时推送第三方平台， 数据解密

    下面详细描述对通知数据进行解密的流程：
    1. 通知秘钥 key，记为 notify_key；
    2. 针对 resource.algorithm 中描述的算法（目前为 AEAD_AES_256_GCM），取得对应的参数 nonce 和 associated_data；
    3. 使用 notify_key、nonce 和 associated_data，对数据密文 resource.ciphertext 进行解密，得到 JSON 形式的资源
    对象（资源对象就是具体的数据内容）；
    注： AEAD_AES_256_GCM 算法的接口细节，请参考 rfc5116。微校支付使用的通知密钥 key 长度为 32 个字节，随机串 nonce
    长度 32 个字节，associated_data 长度小于 16 个字节并可能为空。
    :param nonce:               加密使用的随机串
    :param ciphertext:          Base64编码后的数据密文
    :param associated_data:     附加数据
    :param notify_key:          秘钥
    :return:
    """
    key_bytes = notify_key.encode('UTF-8')
    nonce_bytes = nonce.encode('UTF-8')
    associated_data_bytes = associated_data.encode('UTF-8') if associated_data else None
    data = base64.b64decode(ciphertext)
    aes_gcm = AESGCM(key=key_bytes)
    try:
        result = aes_gcm.decrypt(nonce=nonce_bytes, data=data, associated_data=associated_data_bytes).decode('UTF-8')
    except InvalidTag:
        result = None
    return result
