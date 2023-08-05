from pathlib import Path


def write_dump_mailbox(uid: int, codec: str, msg: bytes):
    folder = Path(__file__).parent / "mailbox"
    folder.mkdir(parents=True, exist_ok=True)
    file = folder / f"{uid}_{codec}.eml"
    file.write_bytes(msg)
