import os
import os.path as op

# 使用说明：从script_cn 转入 script_cn_with_jp

translated_script = 'script_cn'
merged_script = 'script_cn_with_jp'


# 遍历文件夹，返回文件列表
def walk(adr: str) -> list[str]:
    mylist = []
    for root, _, files in os.walk(adr):
        for name in files:
            adrlist = os.path.join(root, name)
            mylist.append(adrlist)
    return mylist


def convert2cmp(jp_cn: list[str]) -> list[str]:
    jp = jp_cn[0].rstrip()
    cn_with_jp = jp_cn[1][:-1] + '||' + jp[10:] + '\n'
    return [jp_cn[0], cn_with_jp]


if __name__ == '__main__':
    files = walk(translated_script)

    if len(files) > 0:
        os.makedirs(merged_script, exist_ok=True)

    for file in files:
        write_lines = []
        lines = open(file, encoding='utf8').readlines()
        for index, line in enumerate(lines):
            if (line[0] == '○') and ('^' not in line):
                pair = convert2cmp(lines[index : index + 2])
                write_lines.extend(pair)
            elif (line[0] == '●') and ('^' not in line):
                pass
            else:
                write_lines.append(line)
        open(
            op.join(merged_script, op.basename(file)), 'w', encoding='utf8'
        ).writelines(write_lines)
        print(file, 'done')
