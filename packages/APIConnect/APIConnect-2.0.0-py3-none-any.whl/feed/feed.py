from cgitb import Hook
import json
import logging
import socket
from threading import Thread
from time import sleep
from typing import Any, Callable

from constants.streaming_constants import StreamingConstants

LOGGER = logging.getLogger(__name__)

class Feed:

    def __init__(self, confObj):
        self.__conf = confObj

        AppIdKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImZmIjoiVyIsImJkIjoid2ViLXBjIiwibmJmIjoxNjcxMTcwMjc2LCJzcmMiOiJlbXRtdyIsImF2IjoiMi4wLjAiLCJhcHBpZCI6IjQxZGE0MDEyNDg2YjFhY2IzNTc4YzYwZjdmNGUyNDhhIiwiaXNzIjoiZW10IiwiZXhwIjoxNjcxMjE1NDAwLCJpYXQiOjE2NzExNzA1NzZ9.7mqgyIfCxuILFGKI_WR0QsrS64mUIKptW5D7utHyDHA"
        Host="ncst.nuvamawealth.com"
        Port=9443

        self._appID = AppIdKey
        self.__host = Host
        self.__port = Port

        if self.__conf:
            if self.__conf['GLOBAL'].get('AppIdKey'):
                self._appID = self.__conf['GLOBAL'].get('AppIdKey')
            if self.__conf['STREAM'].get('HOST'):
                self.__host = self.__conf['STREAM'].get('HOST')
            if self.__conf['STREAM'].get('PORT'):
                self.__port = int(self.__conf['STREAM'].get('PORT'))
        self._sock = None
        self._socket_fs = None
        self.__requestsList = {}

        t = Thread(target=self.__do_connection)
        t.start()

    def _subscribe(self, request : str, callback : Callable[[str], Any], requestCode : StreamingConstants):
        self.__requestsList[requestCode] = {'request' : request, 'callback' : callback}
        self.__sub(requestCode)

    def _unsubscribe(self, request : str, requestCode : StreamingConstants):
        if self.__is_connection_alive():
            self.__send_stream_request(request)
        else :
            self.__do_connection()
            self.__send_stream_request(request)
        self.__requestsList.pop(requestCode, "Key not found")


    def __sub(self, action):
        if self.__is_connection_alive():
            if action == 'all':
                for req_code in self.__requestsList.keys():
                    self.__start_streaming(self.__requestsList[req_code]['request'])
                    sleep(0.1)
            elif type(action) is StreamingConstants:
                self.__start_streaming(self.__requestsList[action]['request'])
        else:
            self.__do_connection()
            self.__sub(action)

    def __start_streaming(self, sendRequest : str):
        self.__send_stream_request(sendRequest)
        t_read = Thread(target = self.__read_stream_data)
        t_read.start()

    def __send_stream_request(self, request : str):
        self._socket_fs.writelines(request)
        self._socket_fs.flush()

    def __read_stream_data(self):
        while True:
            resp = self._socket_fs.readline()

            if resp:
                LOGGER.debug(f"Response recevied : {resp}")
                try:
                    resp_dict = json.loads(resp)

                    if resp_dict['response']["streaming_type"] == "quote3":
                        callback = self.__requestsList[StreamingConstants.QUOTE_SREAM_REQ_CODE]['callback']
                    elif resp_dict['response']["streaming_type"] == "orderFiler":
                        callback = self.__requestsList[StreamingConstants.ORDER_STREAM_REQ_CODE]['callback']
                    elif resp_dict['response']["streaming_type"] == "news":
                        callback = self.__requestsList[StreamingConstants.LIVENEWS_STREAM_REQ_CODE]['callback']

                    callback(resp)

                except json.JSONDecodeError:
                    pass

            else:
                LOGGER.error("Response Blank. Socket Connection seems to be closed. Trying to reconnect...")
                break

        self.__sub(action = "all")

    def __is_connection_alive(self) -> bool:
        alive = False
        status = f"Socket is null : {self._sock is None}, socket file stream is null : {self._socket_fs is None}, "
        if (self._sock is not None) and (self._socket_fs is not None) :
            LOGGER.debug(status + f"Socket is closed : {self._sock._closed}, socket file stream is closed : {self._socket_fs.closed}")
            if (not self._sock._closed) and (not self._socket_fs.closed):
                alive = True
        return alive

    def __do_connection(self):
        ''' Create connection; if it fails inititate retry logic '''

        try :
            self.__create_connection()
        except OSError:
            self.__retry_connection()

    def __create_connection(self):
        # New code TCP
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(100)

        self._sock.connect((self.__host, self.__port)) # raises OSError
        self._sock.setblocking(True)

        self._socket_fs = self._sock.makefile('rw')
        LOGGER.info("Connection established with subscriber.")

    def __retry_connection(self):
        times = 17000  # ~17000 for ~24 hours with delay of 5 seconds
        initalDelay = 1 # seconds
        maxDelay = 5 # seconds
        delayFactor = 2.0

        currentDelay = initalDelay
        for currentTry in range(times, 0, -1):
            try :
                self.__create_connection()
            except OSError as e:
                LOGGER.error(f"Error : {e}. Failed to establish connection with the streaming socket. Retrying socket connection... Max tries left {currentTry}")
                sleep(currentDelay)
                currentDelay = currentDelay*delayFactor if currentDelay*delayFactor < maxDelay else maxDelay
            else:
                break
        else:
            #last attempt
            try :
                self.__create_connection()
            except OSError as e:
                LOGGER.error(f"Failed to connect with streaming socket after {times} unsuccessful retry attempts. Error : {e}")
                self._sock.close()
                raise e
