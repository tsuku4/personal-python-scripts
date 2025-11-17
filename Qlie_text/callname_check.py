import os, sys
import os.path as op

# 检查さん
# 使用说明：检查script_cn

root = sys.argv[1]

translated_script = op.join(root, 'script_cn')


callname_dict = {
    '日高さん': '日高同学',
    '日高舞夜さん': '日高舞夜同学',
    '静内さん': '静内同学',
    '静内蛍火さん': '静内萤火同学',
    '豊郷さん': '丰乡同学',
    '豊郷沙流さん': '丰乡沙流同学',
    '富川さん': '富川同学',
    '富川紫雲さん': '富川紫云同学',
    '田浦さん': '田浦同学',
    '田浦汐見さん': '田浦汐见同学',
}


# 遍历文件夹，返回文件列表
def walk(adr: str) -> list[str]:
    mylist = []
    for root, _, files in os.walk(adr):
        for name in files:
            adrlist = os.path.join(root, name)
            mylist.append(adrlist)
    return mylist


def check(jp_cn_line: list[str]) -> str:
    jp_line = jp_cn_line[0]
    cn_line = jp_cn_line[1]
    second_maru = jp_line[1:].index('○') + 1
    index = int(jp_line[1:second_maru])

    for jp_name, cn_name in callname_dict.items():
        jp_name_count = jp_line.count(jp_name)
        cn_name_count = cn_line.count(cn_name)
        if jp_name_count != cn_name_count:
            return f'{index}: {jp_name}'

    return ''


if __name__ == '__main__':
    files = walk(translated_script)

    sum = 0

    for file in files:
        lines = open(file, encoding='utf8').readlines()
        for index, line in enumerate(lines):
            if line[0] == '○':
                ret = check(lines[index : index + 2])
                if len(ret) > 0:
                    print(file, ret)
                    sum += 1

        print(file, 'done')

    print('total:', sum)

