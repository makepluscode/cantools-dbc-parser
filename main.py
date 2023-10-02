# main.py

from cantools_parser import CANToolsParser
from signal_analyzer import SignalAnalyzer
import configparser


def load_config():
    # config.ini 파일을 읽어옴
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def parse_dbc_file(dbc_file_path):
    parser = CANToolsParser(dbc_file_path)
    return parser.parse_dbc()


def extract_message_data(db, desired_receiver=None):
    parser = CANToolsParser('')
    return parser.extract_messages(db, desired_receiver)


def extract_signal_data(db, desired_receiver=None):
    parser = CANToolsParser('')
    return parser.extract_signals(db, desired_receiver)


def extract_signal_data_simple(db):
    parser = CANToolsParser('')
    return parser.extract_signals_simple(db)


def print_parsing_errors(message_parsing_error, signal_simple_parsing_error, signal_parsing_error):
    print(f"메시지 데이터 파싱 오류: {message_parsing_error} 개")
    print(f"시그널 데이터 (단순 버전) 파싱 오류: {signal_simple_parsing_error} 개")
    print(f"시그널 데이터 파싱 오류: {signal_parsing_error} 개")


def save_dataframes_to_csv(message_df, signal_df_simple, signal_df, ecu_matrix_df):
    message_df.to_csv("message.csv", index=False, sep=',')
    signal_df_simple.to_csv("signal_simple.csv", index=False, sep=',')
    signal_df.to_csv("signal.csv", index=False, sep=',')
    ecu_matrix_df.to_csv("ecu_matrix.csv", index=False, sep=',')


def main():
    config = load_config()
    dbc_file_path = config['Paths']['dbc_file_path']

    db = parse_dbc_file(dbc_file_path)
    desired_receiver = None

    message_df, message_parsing_error = extract_message_data(
        db, desired_receiver)
    signal_df_simple, signal_simple_parsing_error = extract_signal_data_simple(
        db)
    signal_df, signal_parsing_error = extract_signal_data(db, desired_receiver)

    print_parsing_errors(message_parsing_error,
                         signal_simple_parsing_error, signal_parsing_error)

    # SignalAnalyzer를 사용하여 주고 받는 시그널의 개수 출력
    signal_analyzer = SignalAnalyzer(signal_df)
    ecu_matrix_df, ecu_matrix_total = signal_analyzer.get_ecu_matrix()

    print("\n주고 받는 시그널의 개수:", ecu_matrix_total)
    print()
    print(ecu_matrix_df)

    save_dataframes_to_csv(message_df, signal_df_simple,
                           signal_df, ecu_matrix_df)


if __name__ == "__main__":
    main()
