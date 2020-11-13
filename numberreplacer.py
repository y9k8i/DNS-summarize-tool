# CSVからホスト名を取得し数字を置換するクラス by @y9k8i 2020
import csv
import re
import sys
import pprint


class NumberReplacer:

    def replace_number(self, file_path, domain="", aggressive=False) -> list:
        """
        DNSレコードを記録したCSVからホスト名を読み込み数字を置換し返す

                aggressive:複数回出現した数字を全て置換するオプション
        """
        # 事前に正規表現をコンパイルしておく
        regex = re.compile(r'\d+') if aggressive else re.compile(r'\d+$')
        result = []

        # CSV読み込み
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            # ヘッダ行を無視
            next(reader)

            for row in reader:
                # ドメインが与えられていない場合自動検出
                if reader.line_num == 2 and domain == "":
                    domain = '.'.join(row[1].rsplit('.', 3)[-3:])
                hn_row = row[1].replace('.' + domain, '')
                if aggressive:
                    result.append(regex.sub('[数字]', hn_row))
                else:
                    hn_splited = hn_row.split('.', 1)
                    result.append(
                        regex.sub('[数字]', hn_splited[0]) +
                        ('.' + hn_splited[1] if len(hn_splited) != 1 else '')
                    )
        result.sort()
        return result


# 直接実行された場合
if __name__ == "__main__":
    NR = NumberReplacer()
    if len(sys.argv) == 4:
        pprint.pprint(NR.replace_number(
            sys.argv[1], sys.argv[2], sys.argv[3]), compact=False)
    elif len(sys.argv) == 3:
        pprint.pprint(NR.replace_number(
            sys.argv[1], sys.argv[2], None), compact=False)
    elif len(sys.argv) == 2:
        pprint.pprint(NR.replace_number(sys.argv[1]), compact=False)
    else:
        print("usage: " + sys.argv[0] + " filepath [domain] [aggressive]")
