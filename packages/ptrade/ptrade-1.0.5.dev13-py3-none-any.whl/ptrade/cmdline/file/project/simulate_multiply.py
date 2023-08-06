import ptrade
from rule import MyRule
from simulate import MySimulate



if __name__ == '__main__':
    # ------------------------------------------------------
    instIds = [] # 产品ID列表
    load_candle_map_param = dict(
        company='【交易所】',
        instType='【产品类别】',
        instIds=instIds,
        start='【起始日期】',
        end='【终止日期】',
        bar='【时间粒度】',
    )

    filepath = './simulate_multiply.csv'  # 交易数据存储路径
    # ------------------------------------------------------
    candle_map = ptrade.load.load_candle_map(**load_candle_map_param)
    sm = ptrade.SimulateMultiply(
        Simulate=MySimulate,
        candle_map=candle_map,
        rule = MyRule,
        warn= True
    )
    sm.run(p_num=4)
    df = sm.analysis.get_df()
    df.to_csv(filepath)
    print(df.head())
