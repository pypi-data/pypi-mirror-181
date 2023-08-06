import datetime

from snowflake import make_snowflake

last_timestamp_ms = 0
sequence_id = 0


def make_id(timestamp_ms: int) -> int:
    global last_timestamp_ms, sequence_id

    if timestamp_ms != last_timestamp_ms:
        last_timestamp_ms = timestamp_ms
        sequence_id = 0
    id = make_snowflake(timestamp_ms, 1, 1, sequence_id)
    sequence_id += 1
    return id


if __name__ == "__main__":
    ts = int(datetime.datetime.now().timestamp() * 1000)
    for i in range(1, 21):
        if i % 5 == 0:
            ts += 1
            print()
        print(make_id(ts))
