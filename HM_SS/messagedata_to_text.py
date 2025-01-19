"""
This script is for extracting text from Each file in MessageData.bin
Use this after unpacking MessageData.bin
"""

import sys
import os
import struct
import shutil
import binascii


def read_int(data: bytes) -> int:
    return struct.unpack("<I", data[:4])[0]


def read_short(data: bytes) -> int:
    return struct.unpack("<H", data[:2])[0]


class MessageDataToText:
    def __init__(self, dir, outdir=None):
        self.dir = dir
        self.outdir = outdir
        self.tbl: dict[str, bytes] = {}
        if outdir is None:
            self.outdir = self.dir
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def load_tbl(self, tbl_path):
        with open(tbl_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() == "":
                    continue
                item = line.strip().split("=")
                hex_item = binascii.unhexlify(item[0])
                str_item = item[1]
                if len(item) == 3:
                    self.tbl["="] = hex_item
                elif len(item) == 2:
                    self.tbl[str_item] = hex_item
                else:
                    raise Exception("Invalid table format")
        print("Table loaded!")

    def extract_text(self):
        for file in os.listdir(self.dir):
            if file.endswith(".hav"):
                self._extract_text(os.path.join(self.dir, file))
        print("Extraction Done!")

    def _extract_text(self, path):
        out_filename = os.path.join(self.outdir, os.path.basename(path) + ".txt")
        f = open(path, "rb")
        count = read_int(f.read(4))
        pointers = []
        text_uids = []
        sizes = []
        texts = []

        pointers.append(0)

        for i in range(count):
            pointers.append(read_short(f.read(2)))

        for i in range(count):
            text_uids.append(read_short(f.read(2)))

        for i in range(count):
            sizes.append(pointers[i + 1] - pointers[i])
        for i in range(count):
            text = f.read(sizes[i])
            text = text.decode("shift-jis")
            texts.append(text)

        with open(out_filename, "w", encoding="utf-8") as f:
            f.write(str(text_uids))
            f.write("\n\n")
            for text in texts:
                f.write(text)
                f.write("\n")

    def import_text(self):
        if len(self.tbl) == 0:
            raise Exception("No text table found")
        for file in os.listdir(self.dir):
            if file.endswith(".txt"):
                self._import_text(os.path.join(self.dir, file))
        print("Import Done!")

    def _import_text(self, path):
        text_uids = []
        texts = []
        text_binaries: list[bytes] = []
        pointers = []
        count = 0
        pointers.append(0)
        out_filename = os.path.join(self.outdir, os.path.basename(path).replace(".txt", ""))

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            text_uids = eval(lines[0].strip())

            for line in lines[1:]:
                if line.strip() == "":
                    continue
                texts.append(line.strip())

        for i in range(len(text_uids)):
            item = text_uids[i]
            if isinstance(item, str):
                item = int.from_bytes(binascii.unhexlify(item))
            text_uids[i] = item

        if len(text_uids) == 0:
            with open(out_filename, "wb") as f:
                f.write(b"\x00\x00\x00\x00")
            return

        for text in texts:
            text_binary = b""
            for char in text:
                if char in self.tbl:
                    text_binary += self.tbl[char]
                else:
                    # TODO: raise error?
                    text_binary += char.encode("shift-jis")
            if text_binary[-1] != 0:
                text_binary += b"\x00"

            text_binaries.append(text_binary)

        for i in range(len(text_uids)):
            pointers.append(pointers[i] + len(text_binaries[i]))

        pointers = pointers[1:]
        count = len(pointers)

        with open(out_filename, "wb") as f:
            f.write(struct.pack("<I", count))
            for i in range(len(pointers)):
                f.write(struct.pack("<H", pointers[i]))
            for i in range(len(text_uids)):
                f.write(struct.pack("<H", text_uids[i]))
            for text_binary in text_binaries:
                f.write(text_binary)

            # Pad with NULL bytes to make total file length multiple of 4
            current_size = f.tell()
            padding_size = (4 - (current_size % 4)) % 4
            f.write(b"\x00" * padding_size)


def usage():
    print("MessageData to Text Converter")
    print("If you want to extract text, use -e or --extract")
    print("If you want to import text, use -i or --import")
    print(
        "Usage: python messagedata_to_text.py -e <Extracted MessageData.bin directory> <Output directory (Optional)>"
    )
    print(
        "Usage: python messagedata_to_text.py -i <tbl file> <Imported MessageData.bin directory> <Output directory (Optional)>"
    )
    sys.exit(1)


def test():
    tbl_path = "SS_jpn_utf8.tbl"
    message_data_to_text = MessageDataToText("MessageData", "MessageData_out_test")
    message_data_to_text.extract_text()

    message_data_to_text = MessageDataToText("MessageData_out_test", "MessageData_out_bin_test")
    message_data_to_text.load_tbl(tbl_path)
    message_data_to_text.import_text()

    # Check MessageData and MessageData_out_bin_test are same
    # They are folders
    for file in os.listdir("MessageData"):
        with open(os.path.join("MessageData", file), "rb") as f1, open(
            os.path.join("MessageData_out_bin_test", file), "rb"
        ) as f2:
            if f1.read() != f2.read():
                print(f"File {file} is different")
    # remove file
    shutil.rmtree("MessageData_out_bin_test")
    shutil.rmtree("MessageData_out_test")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    mode = sys.argv[1]

    if mode.strip() == "-e" or mode.strip() == "--extract":
        input_dir = sys.argv[2]
        try:
            output_dir = sys.argv[3]
        except IndexError:
            output_dir = input_dir
        message_data_to_text = MessageDataToText(input_dir, output_dir)
        message_data_to_text.extract_text()
    elif mode.strip() == "-i" or mode.strip() == "--import":
        tbl_path = sys.argv[2]
        input_dir = sys.argv[3]
        try:
            output_dir = sys.argv[4]
        except IndexError:
            output_dir = input_dir
        message_data_to_text = MessageDataToText(input_dir, output_dir)
        message_data_to_text.load_tbl(tbl_path)
        message_data_to_text.import_text()
    else:
        usage()
