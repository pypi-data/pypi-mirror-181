from typing import Union
import datetime
import paux.process
import ptrade.component


def _process_simualte_multiply_worker(
        simulate, start, end, clear
):
    simulate.run(start=start, end=end, clear=clear)
    return [simulate.historyOrderDatas, simulate.currentOrderDatas]


# 执行多个产品的模拟交易
class SimulateMultiply():
    def __init__(
            self,
            Simulate,
            candle_map: dict,
            rule: object,
            warn: bool = True,
    ):
        self.simulate_map = {}
        for instId, candle in candle_map.items():
            self.simulate_map[instId] = Simulate(
                candle=candle,
                rule=rule,
                instId=instId,
                warn=warn
            )

    def run(
            self,
            start: Union[datetime.date, int, float, str, None] = None,
            end: Union[datetime.date, int, float, str, None] = None,
            clear: bool = True,
            p_num=1,
            skip_exception=False,
    ):
        if p_num <= 1:
            self.historyOrderDatas = []
            for instId, simulate in self.simulate_map.items():
                simulate.run(start=start, end=end, clear=clear)
                self.historyOrderDatas += simulate.historyOrderDatas
            self.analysis = ptrade.component.Analysis(historyOrderDatas=self.historyOrderDatas)
        else:
            # warnings.warn('p_num应该为1，异步执行存在安全性问题，下个版本会更新')
            params = []
            index_to_instId = {}
            for index, (instId, simulate) in enumerate(self.simulate_map.items()):
                index_to_instId[index] = instId
                params.append(
                    {
                        'simulate': simulate,
                        'start': start,
                        'end': end,
                        'clear': clear,
                    }
                )
            results = paux.process.pool_worker(
                params=params,
                p_num=p_num,
                func=_process_simualte_multiply_worker,
                skip_exception=skip_exception
            )
            self.historyOrderDatas = []
            self.currentOrderDatas = []
            for index, (historyOrderDatas, currentOrderDatas) in enumerate(results):
                instId = index_to_instId[index]
                self.simulate_map[instId].historyOrderDatas = historyOrderDatas
                self.simulate_map[instId].currentOrderDatas = currentOrderDatas
                self.historyOrderDatas += historyOrderDatas
                self.historyOrderDatas += currentOrderDatas
            self.analysis = ptrade.component.Analysis(historyOrderDatas=self.historyOrderDatas)
