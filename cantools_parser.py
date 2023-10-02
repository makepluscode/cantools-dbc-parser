# cantools_parser.py

import cantools
import pandas as pd


class CANToolsParser:
    def __init__(self, dbc_file_path):
        self.dbc_file_path = dbc_file_path

    def parse_dbc(self):
        try:
            db = cantools.database.load_file(self.dbc_file_path)
            return db
        except FileNotFoundError:
            print(f"Error: DBC file '{self.dbc_file_path}' not found.")
            return None

    def extract_messages(self, db, desired_receiver=None):
        message_data = []
        error_count = 0  # 오류 카운트 초기화
        for message in db.messages:
            if desired_receiver is None or desired_receiver in message.receivers:
                message_data.append({
                    'Message Name': message.name,
                    'TX': message.senders,
                    'RX': message.receivers,
                    'ID': message.frame_id,
                    'Byte Length': message.length,
                    'Desired Receiver': desired_receiver,
                })
        return pd.DataFrame(message_data), error_count

    def extract_signals(self, db, desired_receiver=None):
        signal_data = []
        error_count = 0  # 오류 카운트 초기화
        for message in db.messages:
            for signal in message.signals:
                for receiver in signal.receivers:
                    if len(message.senders) != 1:
                        print(
                            f"Error: Signal '{message.name}' has {len(message.senders)} senders.")
                        error_count += 1

                    signal_data.append({
                        'Message Name': message.name,
                        'Signal Name': signal.name,
                        'TX': message.senders[0] if message.senders else '',
                        'RX': receiver,
                        'Bit Start Position': signal.start,
                        'Bit Length': signal.length,
                        'Unit': signal.unit,
                        'Minimum Value': signal.minimum,
                        'Maximum Value': signal.maximum,
                        'Scale Factor': signal.scale,
                        'Offset': signal.offset,
                        'Desired Receiver': desired_receiver,
                    })
        return pd.DataFrame(signal_data), error_count

    def extract_signals_simple(self, db):
        signal_data = []
        error_count = 0  # 오류 카운트 초기화
        for message in db.messages:
            for signal in message.signals:
                signal_data.append({
                    'Message Name': message.name,
                    'Signal Name': signal.name,
                    'TX': message.senders[0] if message.senders else '',
                    'RX': message.receivers,
                    'Bit Start Position': signal.start,
                    'Bit Length': signal.length,
                    'Unit': signal.unit,
                    'Minimum Value': signal.minimum,
                    'Maximum Value': signal.maximum,
                    'Scale Factor': signal.scale,
                    'Offset': signal.offset,
                })
        return pd.DataFrame(signal_data), error_count
