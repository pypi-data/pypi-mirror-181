# -*- coding:utf-8 -*-
# 文件:  thread_pool.py
# 日期:  2022/8/19 9:50
"""

"""
import threading
from concurrent import futures
from .logs import logger


__version__ = '1.2'
__all__ = ['JdThreadPool']


"""
Future 提供了如下方法：
cancel()：取消该 Future 代表的线程任务。如果该任务正在执行，不可取消，则该方法返回 False；否则，程序会取消该任务，并返回 True。
cancelled()：返回 Future 代表的线程任务是否被成功取消。
running()：如果该 Future 代表的线程任务正在执行、不可被取消，该方法返回 True。
done()：如果该 Future 代表的线程任务被成功取消或执行完成，则该方法返回 True。
result(timeout=None)：获取该 Future 代表的线程任务最后返回的结果。如果 Future 代表的线程任务还未完成，该方法将会阻塞当前线程，其中 timeout 参数指定最多阻塞多少秒。
exception(timeout=None)：获取该 Future 代表的线程任务所引发的异常。如果该任务成功完成，没有异常，则该方法返回 None。
add_done_callback(fn)：为该 Future 代表的线程任务注册一个“回调函数”，当该任务成功完成时，程序会自动触发该 fn 函数。
"""


class JdThreadPool(object):
    """
    线程池
    """

    def __init__(self, max_workers=5):
        """
        创建线程池
        """
        self.pool = futures.ThreadPoolExecutor(max_workers=max_workers)
        self._thread_lock = threading.Lock()
        self._future = set()

    def add_job(self, callback, para) -> futures.Future:
        """
        添加任务
        """
        thread_name = threading.current_thread().name
        logger.debug(f"[ {thread_name} ], {para}")
        future = self.pool.submit(callback, para)
        self._thread_lock.acquire()
        self._future.add(future)
        self._thread_lock.release()
        future.add_done_callback(self._callback_finished)
        return future

    def _callback_finished(self, future: futures.Future):
        """
        线程执行完毕后的 回调函数
        """
        thread_name = threading.current_thread().name
        logger.debug(f"[ {thread_name} ]执行完成： {future.result()}")
        self._thread_lock.acquire()
        self._future.remove(future)
        self._thread_lock.release()

    @classmethod
    def cancel(cls, future: futures.Future):
        """
        取消该 Future 代表的线程任务。如果该任务正在执行，不可取消，则该方法返回 False；
        否则，程序会取消该任务，并返回 True。
        """
        return future.cancel()

    @classmethod
    def cancelled(cls, future: futures.Future):
        """
        返回 Future 代表的线程任务是否被成功取消。
        """
        return future.cancelled()

    @classmethod
    def running(cls, future: futures.Future):
        """
        如果该 Future 代表的线程任务正在执行、不可被取消，该方法返回 True。
        """
        return future.running()

    @classmethod
    def done(cls, future: futures.Future):
        """
        如果该 Future 代表的线程任务被成功取消或执行完成，则该方法返回 True。
        """
        return future.done()
