# signal_analyzer.py

class SignalAnalyzer:
    def analyze_signal(self, signal_df):
        unique_tx_list = []
        unique_rx_list = []

        for index, row in signal_df.iterrows():
            tx = row['TX']
            rx = row['RX']

            # TX 리스트에 추가 (중복 허용하지 않음)
            if tx not in unique_tx_list:
                unique_tx_list.append(tx)

            # RX 리스트에 추가 (중복 허용하지 않음)
            if rx not in unique_rx_list:
                unique_rx_list.append(rx)

        # TX와 RX 리스트를 알파벳 순으로 정렬
        unique_tx_list.sort()
        unique_rx_list.sort()

        return unique_tx_list, len(unique_tx_list), unique_rx_list, len(unique_rx_list)
