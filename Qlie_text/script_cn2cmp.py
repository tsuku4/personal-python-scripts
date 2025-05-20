import os, sys
import os.path as op
from typing import Optional

# 使用说明：从script_cn 转入 script_cn_with_jp

root = sys.argv[1]

translated_script = op.join(root, 'script_cn')
cmp_script = op.join(root, 'script_cn_with_jp')


# 遍历文件夹，返回文件列表
def walk(adr: str) -> list[str]:
    mylist = []
    for root, _, files in os.walk(adr):
        for name in files:
            adrlist = os.path.join(root, name)
            mylist.append(adrlist)
    return mylist


def convert2cmp(jp_cn: list[str], debug_file: Optional[str] = None) -> list[str]:
    jp = jp_cn[0].rstrip()
    cn_with_jp = jp_cn[1][:-1] + '||' + jp[10:] + '\n'

    if debug_file is not None:
        No = int(jp[1 : jp.index('○', 1)])
        cn_with_jp = cn_with_jp[:-1] + '||' + debug_file + '.' + str(No) + '\n'

    return [jp_cn[0], cn_with_jp]


if __name__ == '__main__':
    files = walk(translated_script)

    if len(files) > 0:
        os.makedirs(cmp_script, exist_ok=True)

    for file in files:
        filename = op.splitext(op.basename(file))[0]
        write_lines = []
        lines = open(file, encoding='utf8').readlines()
        for index, line in enumerate(lines):
            if (
                ('^' not in line)
                and ('\\' not in line)
                and (len(line) > 10 and line[10] != '【')
            ):
                if line[0] == '○':
                    pair = convert2cmp(lines[index : index + 2], filename)
                    write_lines.extend(pair)
                    continue
                elif line[0] == '●':
                    continue
            write_lines.append(line)
        open(op.join(cmp_script, op.basename(file)), 'w', encoding='utf8').writelines(
            write_lines
        )
        print(file, 'done')
