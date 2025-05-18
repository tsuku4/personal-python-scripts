import os
import os.path as op

# 汉化名字统一
# 使用说明：从script_cn 转入 script_cn_format

translated_script = 'script_cn'
format_script = 'script_cn_format'


jp_cn_name_dict = {
    '柳': '柳',
    '舞夜': '舞夜',
    '流衣': '流衣',
    '蛍火': '萤火',
    '紫雲': '紫云',
    '汐見': '汐见',
    '沙流': '沙流',
    '沙流・汐見': '沙流・汐见',
    '女子＠舞夜': '女生＠舞夜',
    '女子＠蛍火': '女生＠萤火',
    '女子１＠沙流': '女生＠沙流',
    '女子２＠紫雲': '女生＠紫云',
    '女子３＠汐見': '女生＠汐见',
    '女子＠真実': '女生＠真实',
    '図書委員＠若葉': '图书委员＠若叶',
    '姉＠梓': '姐姐＠梓',
    '姉＠檜': '姐姐＠桧',
    '姉＠カヤ': '姐姐＠佳耶',
    '姉＠クヌギ': '姐姐＠栎',
    'アズサ': '梓',
    'ヒノキ': '桧',
    'カヤ': '佳耶',
    'クヌギ': '栎',
    '男子１': '男生1',
    '男子２': '男生2',
    '男子３': '男生3',
    '男子４': '男生4',
    '男子５': '男生5',
    '明石': '明石',
    '男性教師': '男性老师',
    '数学教師': '数学老师',
    '清田': '清田',
    '西岡': '西冈',
    '平岸': '平岸',
    '三人': '三人',
    '３人': '3人',
    '４人': '4人',
    '５人': '5人',
    'みんな': '大家',
    '全員': '全员',
    'バニーたち': '兔女郎们',
    '男子たち': '男生们',
    '姉たち': '姐姐们',
}


# 遍历文件夹，返回文件列表
def walk(adr: str) -> list[str]:
    mylist = []
    for root, _, files in os.walk(adr):
        for name in files:
            adrlist = os.path.join(root, name)
            mylist.append(adrlist)
    return mylist


def format_name(jp_cn_name: list[str]) -> list[str]:
    rindex = jp_cn_name[0].index('】')
    jp_name = jp_cn_name[0][11:rindex]
    cn_name = jp_cn_name_dict.get(jp_name, '')
    if cn_name == '':
        print('\n' + jp_name + '\n')
        cn_name = jp_name
    new_cn_name_line = jp_cn_name[1][:11] + cn_name + '】\n'
    return [jp_cn_name[0], new_cn_name_line]


if __name__ == '__main__':
    files = walk(translated_script)

    if len(files) > 0:
        os.makedirs(format_script, exist_ok=True)

    for file in files:
        write_lines = []
        lines = open(file, encoding='utf8').readlines()
        for index, line in enumerate(lines):
            if (line[0] == '○') and (line[10] == '【'):
                pair = format_name(lines[index : index + 2])
                write_lines.extend(pair)
            elif (line[0] == '●') and (line[10] == '【'):
                pass
            else:
                write_lines.append(line)
        open(
            op.join(format_script, op.basename(file)), 'w', encoding='utf8'
        ).writelines(write_lines)
        print(file, 'done')
