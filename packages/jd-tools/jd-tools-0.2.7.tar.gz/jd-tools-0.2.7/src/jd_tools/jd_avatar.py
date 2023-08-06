# -*- coding: utf-8 -*-
import os
from .tools import Singleton, JdPath, JdTools
from .oper_file import copy_file, move_file


__version__ = '1.0.6'
__all__ = ('Avatar', 'AvatarDirMgr')

"""
文件上传， 将临时上传的文件移动 / 目录重命名为 正式目录
只支持单文件操作

用法示例：
1. 先注册模块
    ad = AvatarDirMgr()
    ad.basedir = os.path.join(basedir, 'app/static')
    ad.tmpdir = os.path.join(basedir, 'app/static/tmp')
    logger.debug(f"basedir: [{ad.basedir}], tmpdir: [{ad.tmpdir}]")

    ad.register_module('user', 'head')  # 产生的url为： /head/user/{id}/filename
    ad.register_module('student')       # 产生的url为： /student/{id}/filename
"""

# location 取值定义
LOCAL_SERVER = 1    # 本地服务器
PIC_SERVER = 2      # 图片服务器


class AvatarDirMgr(metaclass=Singleton):
    _module = {}    # 模块
    _basedir = ''   # 文件基准目录。 静态页面所在地址
    _tmp_dir = ''   # 公共临时文件相对目录， 从 _basedir 目录开始写

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, basedir):
        if not os.path.isdir(basedir):
            raise Exception(f'basedir path not exist! [{basedir}]')
        self._basedir = basedir

    @property
    def tmpdir(self):
        return self._tmp_dir

    @tmpdir.setter
    def tmpdir(self, tmp_dir):
        self._tmp_dir = tmp_dir

    def register_module(self, module: str, m_dir: str = '', absolute=False, prefix=''):
        """
        注册模块 及存放路径
        :param module:  模块名称
        :param m_dir:   存放路径，基准路径后面的路径，比如 '/img/head/', 通过 域名 + 该路径 可以访问到文件
        :param absolute:  绝对目录， False-否， 在 m_dir 后添加【模块名】做目录， True-是，不添加 模块名目录
        :param prefix:  id 目录前缀， 比如 company， id为5， 生成的目录为 company_5
        :return:
        """
        if not module:
            raise Exception('[module] is not assigned!')
        # m_dir 以 '/' 开头时， 去掉 '/'
        self._module[module] = {'dir': m_dir[1:] if m_dir and m_dir[0] == '/' else (m_dir or ''),
                                'absolute': absolute, 'prefix': prefix or ''}

    def allowed(self, module: str) -> bool:
        """
        判断模块是否注册过
        :param module:  模块名称
        :return:    bool， True-模块注册过， False-模块未注册
        """
        return module in self._module

    def get_dir(self, module: str) -> tuple:
        """
        获取模块的存放路径
        :param module:  模块名称
        :return:    (模块存放路径, absolute, prefix)，若模块未注册，返回 空 字符串
        """
        m = self._module.get(module)
        if m:
            return m['dir'], m['absolute'], m['prefix']
        return '', False, ''


class Avatar(object):
    """
    图片文件处理
    负责 某模块 图片 位置存储， 临时文件存储， 临时文件转到正式目录
    """

    def __init__(self, module, module_id=0, relative_dir=False):
        self.__module = module
        self.__module_id = module_id

        self.__url = ''     # 图片文件 url
        self._mgr = AvatarDirMgr()
        if not self._mgr.allowed(module):
            raise Exception(f'module [{module}] not registered!')
        self._basedir = self._mgr.basedir
        self._dir, self._abs, self._prefix = self._mgr.get_dir(module)
        self._tmpdir = self._mgr.tmpdir
        self._relative_dir = relative_dir   # 临时目录使用相对目录， True-是， False-否，使用公共临时目录
        
    def file_path(self, url):
        """
        获取 url 对应的服务器文件路径
        """
        if not url:
            return ''
        fp = os.path.join(self._basedir, url[1:] if url[0] == '/' else url)
        return JdPath.slash(fp)

    def _inner_path(self, some_id=None):
        f"""
        内部路径， 模块注册路径+之后的目录， 比如注册目录为 img/head,  模块为 'user', 则返回的内部路径为
        img/head/user/{some_id}
        若 模块ID为0，新增时，返回的路径为
        tmp_dir/del_user_年月日_时分秒_6位随机字符
        :param some_id:     模块ID
        :return:        内部路径
        """
        module = self.__module
        module_id = some_id or self.__module_id
        if module_id == 0:
            path = f'del_{module}_' + JdTools.get_date()
            upper_dir = self._dir if self._relative_dir else self._tmpdir
        else:
            if self._abs:   # True-是，不添加 模块名目录
                path = f"{self._prefix}{module_id}"
            else:
                path = f'{module}/{self._prefix}%s' % module_id  # 内部路径是 模块名/数据id
            upper_dir = self._dir
        return os.path.join(upper_dir, path)

    def get_module_path(self, some_id=None):
        # 获取模块所在路径， 文件真实路径
        module_id = some_id or self.__module_id
        directory = self._inner_path(module_id)
        dd = os.path.join(self._basedir, directory)
        d2 = JdPath.slash(dd)
        return d2

    def _mk_dir(self, some_id=None, create_dir=True):
        # 创建目录
        module_id = some_id or self.__module_id
        directory = self._inner_path(module_id)
        dd = os.path.join(self._basedir, directory)
        if create_dir and not os.path.exists(dd):  # 当路径不存在时
            os.makedirs(dd)  # 创建路径
        return dd

    def new_file(self, new_file, create_dir=True, some_id=None):
        """返回新文件路径全称
        new_file:       文件名，不含路径
        create_dir:     是否创建新文件所在目录
        some_id:        记录ID，不填时使用模块ID
        """
        module_id = some_id or self.__module_id
        dd = self._mk_dir(module_id, create_dir)
        fp = os.path.join(dd, new_file)

        url = fp.split(self._basedir)[-1]
        self.__url = JdPath.slash(url)  # 修改斜杠，避免url打不开
        return fp

    @property
    def url(self):
        return self.__url

    @staticmethod
    def rm(fn):
        """删除图片文件  fn: 头像 url """

        if not fn or fn in ['/img/avatar.jpg', '/img/item_default.png', '/img/logo.png']:
            return

        head = fn[1:] if fn[0] == '/' else fn
        old_img = os.path.join(AvatarDirMgr().basedir, head)
        if os.path.isfile(old_img):
            try:
                os.remove(old_img)
            except FileNotFoundError:
                pass

    @classmethod
    def basename(cls, filepath):
        """获取文件名， filepath 为路径+文件名"""
        return os.path.basename(filepath)

    @classmethod
    def copy_file_to(cls, module, module_id, old_url):
        """拷贝文件到模块所在目录
        old_url:    原文件所在目录
        """
        av = Avatar(module, module_id)
        filename = av.basename(old_url)

        old_fp = av.file_path(old_url)
        new_fp = av.new_file(filename)
        copy_file(old_fp, new_fp)
        return av.url
    
    @classmethod
    def move_to_normal(cls, module, url, some_id):
        """
        将临时图片 移动到 正式目录， 不保存数据库。 返回 正式 url 地址
        重命名临时目录 --> 正式目录(正式目录不能提前创建) 或者 将 临时目录文件拷贝到正式目录后，再删除 临时目录
        :param module:      模块名称
        :param url:         临时文件url
        :param some_id:     模块ID
        :return:
        """
        image = url
        some_id = some_id
        ret_url = url
        if image:
            av = Avatar(module, some_id)
            old_file = av.file_path(image)
        
            old_path = os.path.dirname(old_file)  # 获取文件所在路径
            new_path = av.get_module_path()
            if old_path == new_path:
                return ret_url
            fn = os.path.basename(old_file)
            new_file = av.new_file(fn, create_dir=False)
            ret_url = av.url
        
            try:
                os.renames(old_path, new_path)  # new_path 存在时，报错跳转到 FileExistsError
            except FileNotFoundError:
                pass
            except FileExistsError:
                move_file(old_file, new_file)
                if not os.listdir(old_path):  # 目录没有文件
                    os.rmdir(old_path)  # 删除目录
    
        return ret_url

    @classmethod
    def move_to_normal_db(cls, module, tb, avatar_key):
        """
        将临时图片 移动到 正式目录。 同时修改表 的字段，改为新的 图片文件url
        重命名临时目录 --> 正式目录(正式目录不能提前创建) 或者 将 临时目录文件拷贝到正式目录后，再删除 临时目录
        :param module:      模块名称
        :param tb:          表对象
        :param avatar_key:  表中的字段名
        :return:
        """
        image = getattr(tb, avatar_key)
        some_id = getattr(tb, 'id')
        ret_url = cls.move_to_normal(module, image, some_id)
        setattr(tb, avatar_key, ret_url)
        return ret_url
        