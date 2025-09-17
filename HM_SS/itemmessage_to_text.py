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


class ItemMessageToText:
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
        # Actually, ItemMessage is just simple shift-jis text file (without header!)
        out_filename = os.path.join(self.outdir, os.path.basename(path) + ".txt")

        data = b""
        with open(path, "rb") as f:
            data = f.read()

        text = data.decode("shift-jis")

        with open(out_filename, "w", encoding="utf-8") as f:
            f.write(text)

    def import_text(self):
        if len(self.tbl) == 0:
            raise Exception("No text table found")
        for file in os.listdir(self.dir):
            if file.endswith(".txt"):
                self._import_text(os.path.join(self.dir, file))
        print("Import Done!")

    def _import_text(self, path):

        out_filename = os.path.join(
            self.outdir, os.path.basename(path).replace(".txt", "")
        )

        # Make sure out file is just one line, if not find the longest line
        texts = []
        longest_text = ""

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            lines = [line for line in lines if line.strip() != ""]
            if len(lines) == 0:
                raise Exception("No text found in " + path)
            count = 0
            for line in lines:
                if line.strip() == "":
                    continue
                texts.append(line.strip())
                if len(line) > len(longest_text):
                    longest_text = line
                count += 1
        text_binary = b""
        for text in longest_text:

            for char in text:
                if char in self.tbl:
                    text_binary += self.tbl[char]
                else:
                    # TODO: raise error?
                    text_binary += char.encode("shift-jis")

        with open(out_filename, "wb") as f:
            f.write(text_binary)


def usage():
    print("ItemMessage to Text Converter")
    print("If you want to extract text, use -e or --extract")
    print("If you want to import text, use -i or --import")
    print(
        "Usage: python itemmessage_to_text.py -e <Extracted ItemMessage.bin directory> <Output directory (Optional)>"
    )
    print(
        "Usage: python itemmessage_to_text.py -i <tbl file> <Imported ItemMessage.bin directory> <Output directory (Optional)>"
    )
    sys.exit(1)


def test():
    tbl_path = "SS_jpn_utf8.tbl"
    message_data_to_text = ItemMessageToText(
        "tmp/ItemMessage", "tmp/ItemMessage_out_test"
    )
    message_data_to_text.extract_text()
    print("Extracted text files are in tmp/ItemMessage_out_test")

    message_data_to_text = ItemMessageToText(
        "tmp/ItemMessage_out_test", "tmp/ItemMessage_out_bin_test"
    )
    message_data_to_text.load_tbl(tbl_path)
    message_data_to_text.import_text()

    # Check ItemMessage and ItemMessage_out_bin_test are same
    # They are folders
    for file in os.listdir("tmp/ItemMessage"):
        with open(os.path.join("tmp/ItemMessage", file), "rb") as f1, open(
            os.path.join("tmp/ItemMessage_out_bin_test", file), "rb"
        ) as f2:
            if f1.read() != f2.read():
                print(f"File {file} is different")
            else:
                print(f"File {file} is same")
    # remove file
    shutil.rmtree("tmp/ItemMessage_out_bin_test")
    shutil.rmtree("tmp/ItemMessage_out_test")


if __name__ == "__main__":
    # test()
    # exit()
    if len(sys.argv) == 1:
        usage()
    mode = sys.argv[1]

    if mode.strip() == "-e" or mode.strip() == "--extract":
        input_dir = sys.argv[2]
        try:
            output_dir = sys.argv[3]
        except IndexError:
            output_dir = input_dir
        message_data_to_text = ItemMessageToText(input_dir, output_dir)
        message_data_to_text.extract_text()
    elif mode.strip() == "-i" or mode.strip() == "--import":
        tbl_path = sys.argv[2]
        input_dir = sys.argv[3]
        try:
            output_dir = sys.argv[4]
        except IndexError:
            output_dir = input_dir
        message_data_to_text = ItemMessageToText(input_dir, output_dir)
        message_data_to_text.load_tbl(tbl_path)
        message_data_to_text.import_text()
    else:
        usage()
