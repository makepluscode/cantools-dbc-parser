import os
from cantools_parser import CANToolsParser
from signal_analyzer import SignalAnalyzer
import configparser
import matplotlib.pyplot as plt
import plotly.express as px


class DBCParser:
    def __init__(self, config_path="config.ini"):
        # 설정 파일 로드
        self.config = self.load_config(config_path)
        # DBC 파일 경로 설정
        self.dbc_file_path = self.config.get(
            "Global", "dbc_file_path", fallback="disable"
        )
        # visualization 설정 로드
        self.visualization = self.config.get(
            "Global", "visualization", fallback="disable"
        )

        # DBC 파일 파싱
        self.db = self.parse_dbc_file(self.dbc_file_path)

    def load_config(self, config_path):
        """설정 파일을 로드하는 함수"""
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def parse_dbc_file(self, dbc_file_path):
        """DBC 파일을 파싱하는 함수"""
        parser = CANToolsParser(dbc_file_path)
        return parser.parse_dbc()

    def extract_message_data(self, desired_receiver=None):
        """메시지 데이터 추출 함수"""
        parser = CANToolsParser("")
        return parser.extract_messages(self.db, desired_receiver)

    def extract_signal_data(self, desired_receiver=None):
        """시그널 데이터 추출 함수"""
        parser = CANToolsParser("")
        return parser.extract_signals(self.db, desired_receiver)

    def extract_signal_data_simple(self):
        """단순한 형태의 시그널 데이터 추출 함수"""
        parser = CANToolsParser("")
        return parser.extract_signals_simple(self.db)

    def print_parsing_errors(
        self, message_parsing_error, signal_simple_parsing_error, signal_parsing_error
    ):
        """파싱 오류 출력 함수"""
        print(f"메시지 데이터 파싱 오류: {message_parsing_error} 개")
        print(f"시그널 데이터 (단순 버전) 파싱 오류: {signal_simple_parsing_error} 개")
        print(f"시그널 데이터 파싱 오류: {signal_parsing_error} 개")

    def save_dataframes_to_csv(
        self, message_df, signal_df_simple, signal_df, ecu_matrix_df
    ):
        """데이터프레임을 CSV 파일로 저장하는 함수"""
        base_filename = self.dbc_file_path.split("/")[-1].replace(".dbc", "")
        csv_dir = "csv"
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        message_df.to_csv(
            os.path.join(csv_dir, f"{base_filename}_message.csv"), index=False, sep=","
        )
        signal_df_simple.to_csv(
            os.path.join(csv_dir, f"{base_filename}_signal_simple.csv"),
            index=False,
            sep=",",
        )
        signal_df.to_csv(
            os.path.join(csv_dir, f"{base_filename}_signal.csv"), index=False, sep=","
        )
        ecu_matrix_df.to_csv(
            os.path.join(csv_dir, f"{base_filename}_ecu_matrix.csv"),
            index=True,
            sep=",",
        )

    def analyze_signals(self, signal_df):
        """시그널 분석 함수"""
        signal_analyzer = SignalAnalyzer(signal_df)
        return signal_analyzer.get_ecu_matrix()

    def visualize_ecu_matrix(self, ecu_matrix_df):
        """ECU 매트릭스 시각화 함수"""
        fig = px.imshow(ecu_matrix_df, color_continuous_scale="purples")
        fig.show()

    def run(self):
        """주요 실행 함수"""
        desired_receiver = None
        message_df, message_parsing_error = self.extract_message_data(desired_receiver)
        (
            signal_df_simple,
            signal_simple_parsing_error,
        ) = self.extract_signal_data_simple()
        signal_df, signal_parsing_error = self.extract_signal_data(desired_receiver)
        self.print_parsing_errors(
            message_parsing_error, signal_simple_parsing_error, signal_parsing_error
        )
        ecu_matrix_df, ecu_matrix_total = self.analyze_signals(signal_df)
        print("\n주고 받는 시그널의 개수:", ecu_matrix_total)
        print()
        print(ecu_matrix_df)
        self.save_dataframes_to_csv(
            message_df, signal_df_simple, signal_df, ecu_matrix_df
        )
        if self.visualization == "enable":
            self.visualize_ecu_matrix(ecu_matrix_df)


if __name__ == "__main__":
    parser = DBCParser()
    parser.run()
