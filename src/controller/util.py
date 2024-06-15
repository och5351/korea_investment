from ..model.auth import AuthModel
from ..model.communicator import *
from ..config import *
import asyncio


class Controller(AuthModel):

    def stock_explanation(self, tr_id: str):
        """
        주식 설명 메소드

        :param tr_id: 종목 코드
        :return:
        """

        print(PrimaryStockComm().get_info(
            url=COMMUNICATION_CONF.PRIMARY_SEARCH_URL,
            token=super().get_token(),
            app_key=super().get_app_key(),
            secret_key=super().get_secret_key(),
            tr_id=tr_id))

    def realtime_listing(self, tr_key: str):

        super().update_approval_key()

        asyncio.get_event_loop().run_until_complete(
            realtime_trading_price_comm(
                url=COMMUNICATION_CONF.REALTIME_PRICE_URL,
                approval_key=super().get_approval_key(),
                tr_key=tr_key
            )
        )
        asyncio.get_event_loop().close()

    def my_account(self):

        print(AccountComm().get_account(
            url=COMMUNICATION_CONF.PRIMARY_SEARCH_URL,
            token=super().get_token(),
            app_key=super().get_app_key(),
            secret_key=super().get_secret_key(),
            accuont_num=super().get_user_account()
        ))
