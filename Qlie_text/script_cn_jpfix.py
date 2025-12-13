import os, sys, re
import os.path as op
from typing import Optional

# 使用说明：从script_jp, script_cn 转入script_cn_jpfixed

root = sys.argv[1]

original_script = op.join(root, 'script_jp')
translated_script = op.join(root, 'script_cn')
fix_script = op.join(root, 'script_cn_jpfixed')


# 遍历文件夹，返回文件列表
def walk(adr: str) -> list[str]:
    mylist = []
    for root, _, files in os.walk(adr):
        for name in files:
            adrlist = os.path.join(root, name)
            mylist.append(adrlist)
    return mylist


def makestr(lines: list[str]) -> list[str]:
    sentence_i = -1
    string_list = []
    for index, line in enumerate(lines):
        s = re.match('○[0-9A-Fa-f]+○', line)
        if s:
            now = int(line[1:9])
            assert now == sentence_i + 1, now
            sentence_i = now

            string_list.append(line)
    return string_list


def convert2cmp(jp_cn: list[str], debug_file: Optional[str] = None) -> list[str]:
    jp = jp_cn[0].rstrip()
    cn_with_jp = jp_cn[1][:-1] + '||' + jp[10:] + '\n'

    if debug_file is not None:
        No = int(jp[1 : jp.index('○', 1)])
        cn_with_jp = cn_with_jp[:-1] + '||' + debug_file + '.' + str(No) + '\n'

    return [jp_cn[0], cn_with_jp]


if __name__ == '__main__':
    jp_files = walk(original_script)

    if len(jp_files) > 0:
        os.makedirs(fix_script, exist_ok=True)

    for jp_file in jp_files:
        filename = op.splitext(op.basename(jp_file))[0]
        print(filename, 'processing')

        cn_file = op.join(translated_script, filename + '.txt')

        jp_lines = open(jp_file, encoding='utf8').readlines()
        cn_lines = open(cn_file, encoding='utf8').readlines()

        ori_jps = makestr(jp_lines)
        cn_jps = makestr(cn_lines)

        assert len(ori_jps) == len(cn_jps)

        for ori, cn in zip(ori_jps, cn_jps):
            if ori.strip() != cn.strip():
                print(filename, repr(ori.strip()), repr(cn.strip()))

        write_lines = []
        i = 0
        for line in cn_lines:
            if line[0] == '○':
                write_lines.append(ori_jps[i])
                i += 1
            else:
                write_lines.append(line)
        open(op.join(fix_script, filename + '.txt'), 'w', encoding='utf8').writelines(
            write_lines
        )
        print(filename, 'done')
