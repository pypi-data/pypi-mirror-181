import ptrade
from rule import MyRule


class MySimulate(ptrade.Simulate):
    def __init__(
            self,
            candle,
            rule,
            instId: str = None,
            warn: bool = True,
    ):
        super(MySimulate, self).__init__(candle, rule, instId, warn)

    def setup(self):
        # do something
        pass

    def buy(self):
        # do something
        pass

    def sell(self):
        # do something
        pass


if __name__ == '__main__':
    # ------------------------------------------------------
    instId = '【产品ID】'
    load_candle_param = dict(
        company='【交易所】',
        instType='【产品类别】',
        instId=instId,
        start='【起始日期】',
        end='【终止日期】',
        bar='【时间粒度】',
    )
    filepath = './simulate.csv'  # 交易数据存储路径
    # ------------------------------------------------------
    candle = ptrade.load.load_candle(**load_candle_param)
    ms = MySimulate(
        candle=candle,
        rule=MyRule,
        instId=instId,
        warn=True
    )
    ms.run()
    df = ms.analysis.get_df()
    df.to_csv(filepath)
    print(df.head())
