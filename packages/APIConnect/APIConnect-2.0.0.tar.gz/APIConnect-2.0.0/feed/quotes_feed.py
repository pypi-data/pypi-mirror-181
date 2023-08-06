import json
import logging
from typing import Any, Callable, List
from APIConnect.validator import Validator
from constants.streaming_constants import StreamingConstants
from feed.feed import Feed

LOGGER = logging.getLogger(__name__)


class QuotesFeed():

    @Validator.ValidateInputDataTypes
    def __init__(self, feedObj : Feed) -> None:
        self.__feed_obj = feedObj

    @Validator.isRequired(["symbols", "callBack"])
    def subscribeQuotesFeed(self, symbols: List[str], callBack: Callable[[str], Any]) -> None:
        quote = self.__create_quote_request(symbols)
        LOGGER.debug("Subscribing quote feed with request: %s", quote)

        self.__feed_obj._subscribe(quote, callBack, StreamingConstants.QUOTE_SREAM_REQ_CODE)

    @Validator.isRequired(["symbols"])
    def unsubscribeQuotesFeed(self) -> None:
        '''

         This method will unsubscribe from the streamer. After successful invokation, this will stop the streamer packets of the symbols subscribed.

        '''
        unsub_quote = self.__create_quote_request(subscribe = False)
        LOGGER.debug("Unsubscribing quote feed with request: %s", unsub_quote)
        self.__feed_obj._unsubscribe(unsub_quote, StreamingConstants.QUOTE_SREAM_REQ_CODE)

    def __create_quote_request(self, symbols = [], subscribe: bool = True) -> str:

        symset = []
        for syms in symbols:
            symset.append({"symbol": syms})
        if subscribe:
            request_type = "subscribe"
        else:
            request_type = "unsubscribe"
        req = {
            "request":
                {
                    "streaming_type": "quote3",
                    "data":
                        {
                            "accType": "EQ",
                            "symbols": symset
                        },
                    "formFactor": "P",
                    "appID": self.__feed_obj._appID,
                    "response_format": "json",
                    "request_type": request_type
                },
            "echo": {}
        }
        return json.dumps(req) + "\n"
