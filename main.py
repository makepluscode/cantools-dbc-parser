# main.py

import pandas as pd
from cantools_parser import CANToolsParser

if __name__ == "__main__":
    dbc_file_path = "sample.dbc"
    parser = CANToolsParser(dbc_file_path)

    # DBC 파일 파싱
    db = parser.parse_dbc()

    # desired_receiver의 기본값을 None으로 설정
    desired_receiver = None

    # 메시지 데이터 추출
    message_df, message_parsing_error = parser.extract_messages(db, desired_receiver)

    # 시그널 데이터 추출 (단순 버전)
    signal_df_simple, signal_simple_parsing_error = parser.extract_signals_simple(db)

    # 시그널 데이터 추출 (일반 버전)
    signal_df, signal_parsing_error = parser.extract_signals(db, desired_receiver)

    # 각 데이터프레임 출력
    print("메시지 데이터:")
    print(message_df)

    print("\n시그널 데이터 (단순 버전):")
    print(signal_df_simple)

    print("\n시그널 데이터:")
    print(signal_df)

    # 출력 오류 갯수 출력
    print(f"메시지 데이터 파싱 오류: {message_parsing_error} 개")
    print(f"시그널 데이터 (단순 버전) 파싱 오류: {signal_simple_parsing_error} 개")
    print(f"시그널 데이터 파싱 오류: {signal_parsing_error} 개")

    # 각각의 데이터프레임을 각각의 CSV 파일로 저장 (탭으로 구분)
    message_df.to_csv("message.csv", index=False, sep=',')
    signal_df_simple.to_csv("signal_simple.csv", index=False, sep=',')
    signal_df.to_csv("signal.csv", index=False, sep=',')
