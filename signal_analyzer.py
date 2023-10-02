# signal_analyzer.py

import pandas as pd

class SignalAnalyzer:
    def __init__(self, signal_df):
        self.signal_df = signal_df
        self.tx_ecu_list, self.tx_ecu_count, self.rx_ecu_list, self.rx_ecu_count = self.analyze_signal()

    def analyze_signal(self):
        tx_ecu_list = []
        rx_ecu_list = []

        for index, row in self.signal_df.iterrows():
            tx = row['TX']
            rx = row['RX']

            # TX 리스트에 추가 (중복 허용하지 않음)
            if tx not in tx_ecu_list:
                tx_ecu_list.append(tx)

            # RX 리스트에 추가 (중복 허용하지 않음)
            if rx not in rx_ecu_list:
                rx_ecu_list.append(rx)

        # TX와 RX 리스트를 알파벳 순으로 정렬
        tx_ecu_list.sort()
        rx_ecu_list.sort()

        return tx_ecu_list, len(tx_ecu_list), rx_ecu_list, len(rx_ecu_list)

    def get_ecu_matrix(self):
        ecu_matrix = pd.DataFrame(0, index=self.tx_ecu_list, columns=self.rx_ecu_list)

        for index, row in self.signal_df.iterrows():
            tx = row['TX']
            rx = row['RX']
            ecu_matrix.at[tx, rx] += 1

        return ecu_matrix, ecu_matrix.values.sum()