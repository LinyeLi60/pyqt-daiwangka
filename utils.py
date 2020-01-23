
import requests
import re



def ascending(num):
    if num[-1] == num[-3] == num[-5] == num[-7]:
        if int(num[-2]) - int(num[-4]) == int(num[-4]) - int(num[-6]) == int(num[-6]) - int(num[-8]):
            return True
        else:
            return False

    elif num[-2] == num[-4] == num[-6] == num[-8]:
        if int(num[-1]) - int(num[-3]) == int(num[-3]) - int(num[-5]) == int(num[-5]) - int(num[-7]):
            return True
        else:
            return False
    else:
        return False

def get_area_info():
    try:
        headers = {
            'Referer': 'https://msgo.10010.com/newMsg/onLineGo/html/fill.html?sceneFlag=03&goodsId=981610241535&productName=%E5%A4%A7%E7%8E%8B%E5%8D%A1&channel=9999&p=51&c=558&u=rSqV6hmVlPRu8PHYYIjcUQ==&s=02,03&sceneFlag=03',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        }

        response = requests.get('https://res.mall.10010.cn/mall/front/js/areaInfo.js', headers=headers)
        area_info_dict = eval(re.search("[{].*[}]", response.text).group())
        print("省份和城市列表:", area_info_dict)    #ESS_PROVINCE_CODE
        return area_info_dict
    except Exception as e:
        print(e, "获取省份和城市列表失败")


def classify_num(num, custom_rules=None):
    type_of_card = ['所有号码']
    match_index_dict = {'所有号码': (0, 11), '尾abababab': (3, 11), '顺子': (7, 11),
                        '中ABCDE': (3, 8), '炸弹': (7, 11), '真山': (7, 11), '豹子': (8, 11), '尾aabbcc': (5, 11),
                        '4拖1': (6, 11), '尾ababab': (5, 11), '尾号ABC': (8, 11), '尾号CBA': (8, 11), '*a*a*a*a': (3, 11)}

    if custom_rules is not None:
        for rule in custom_rules:
            if re.search(rule.replace('*', '.'), num):
                type_of_card.append('自定义规则')

    if re.search(
            "(?:0(?=1)|1(?=2)|2(?=3)|3(?=4)|4(?=5)|5(?=6)|6(?=7)|7(?=8)|8(?=9)){3,}\\d",
            num[-4:]):
        type_of_card.append('顺子')

    if re.search(
            "(?:0(?=1)|1(?=2)|2(?=3)|3(?=4)|4(?=5)|5(?=6)|6(?=7)|7(?=8)|8(?=9)){2,}\\d",
            num[-3:]):
        if int(num[-1]) > int(num[-2]):
            type_of_card.append('尾号ABC')
        else:
            type_of_card.append('尾号CBA')

        if re.search('([\\d])\\1{2}', num[-6:-3]):
            type_of_card.append('AAABCD')
            match_index_dict['AAABCD'] = (5, 11)

    if re.search(
            "(?:0(?=1)|1(?=2)|2(?=3)|3(?=4)|4(?=5)|5(?=6)|6(?=7)|7(?=8)|8(?=9)){4,}\\d",
            num[3:8]):
        type_of_card.append('中ABCDE')

    if re.search('([\\d])\\1{3}', num[-4:]):
        type_of_card.append('炸弹')
    if num[-8: -4] == num[-4:]:
        type_of_card.append('真山')

    if re.search('([\\d])\\1{2}', num[-3:]):
        type_of_card.append('豹子')

    elif re.search('([\\d])\\1{2}', num[3:]):
        type_of_card.append('全段3A(AAA)')
        match_index_dict['全段3A(AAA)'] = re.search('([\\d])\\1{2}', num).span()

    if re.search('([\\d])\\1{2}', num[-4:-1]):
        type_of_card.append('尾号3拖1')
        match_index_dict['尾号3拖1'] = (7, 10)

    # ret = re.search(
    #         '(?:9(?=8)|8(?=7)|7(?=6)|6(?=5)|5(?=4)|4(?=3)|3(?=2)|2(?=1)|1(?=0)){5,}\\d', num[1:])
    # if ret:
    #     type_of_card.append'倒顺')
    #     s, e = ret.span()a
    #     match_index_dict['倒顺'] = (s+1, e+1)

    if re.search(
            '(?:9(?=8)|8(?=7)|7(?=6)|6(?=5)|5(?=4)|4(?=3)|3(?=2)|2(?=1)|1(?=0)){4,}\\d', num[-5:]):
        type_of_card.append('倒顺')
        match_index_dict['倒顺'] = (6, 11)

    ret = re.search('(\\d)\\1\\1(\\d)\\2\\2', num[3:])  # aaabbb
    if ret:
        type_of_card.append('aaabbb')
        match_index_dict['aaabbb'] = re.search('(\\d)\\1\\1(\\d)\\2\\2', num).span()

    if re.search('(\\d)\\1(\\d)\\2(\\d)\\3', num[-6:]):  # aabbcc
        type_of_card.append('尾aabbcc')
    # if re.search('(\\d)\\1(\\d)\\2(\\d)(\\d)\\3\\4', num[-8:]):  # aabbcdcd
    #     type_of_card.append('aabbcdcd')
    # if re.search('(\\d)\\1(\\d)\\2(\\d)\\3\\3(\\d)', num[-8:]):  # aabbcccd
    #     type_of_card.append('aabbcccd')
    # if re.search('(\\d)(\\d)\\1\\2(\\d)\\3\\3(\\d)', num[-8:]):  # ababcccd
    #     type_of_card.append('ababcccd')
    # if re.search('(\\d)(\\d)\\1\\2(\\d)\\3(\\d)\\4', num[-8:]):  # ababccdd
    #     type_of_card.append('ababccdd')

    ret = re.search('([\\d])\\1{4}', num)
    if ret:
        type_of_card.append('5A')
        match_index_dict['5A'] = ret.span()

    if re.search('([\\d])\\1{3}', num[-5:-1]):
        type_of_card.append('4拖1')
    if re.search('([\\d])\\1{3}', num[3:-2]):
        type_of_card.append('中间4A')
        s, e = re.search('([\\d])\\1{3}', num[3:-2]).span()
        match_index_dict['中间4A'] = (s+3, e+3)

    if num[-6: -4] == num[-4:-2] == num[-2:]:
        type_of_card.append('尾ababab')
    if re.search('000[1|8]', num[-4:]):  # 0001 或0008
        type_of_card.append('0001或0008')
    if re.search('(\\d)\\1\\1(8)', num[-4:]):  # XXX8
        type_of_card.append('XXX8')
    # if re.search('(\\d)(\\d)(\\d)\\1\\2\\3', num[-6:]):  # abcabc
    #     if int(num[-1]) - int(num[-2]) == int(num[-2]) - int(num[-3]):
    #         type_of_card.append('abcabc')

    # if re.search('(\\d)\\1(\\d)\\2', num[-8:-4]):  # AABBxABC
    #     if int(num[-1]) - int(num[-2]) == int(num[-2]) - int(num[-3]) == 1:
    #         type_of_card.append('AABBxABC')

    # if re.search('(\\d)(\\d)\\1\\2', num[-8:-4]):  # ABABxABC
    #     if int(num[-1]) - int(num[-2]) == int(num[-2]) - int(num[-3]) == 1:
    #         type_of_card.append('ABABxABC')

    # if re.search('(\\d)\\1\\1', num[-8:-5]):  # AAABxABC
    #     if int(num[-1]) - int(num[-2]) == int(num[-2]) - int(num[-3]) == 1:
    #         type_of_card.append('AAABxABC')

    if re.search('(\\d)(\\d)\\1\\2\\1\\2', num):  # ababab
        type_of_card.append('ababab')
        match_index_dict['ababab'] = re.search('(\\d)(\\d)\\1\\2\\1\\2', num).span()

    if re.search('(\\d)(\\d)\\1\\2\\1\\2\\1\\2', num[-8:]):  # abababab
        type_of_card.append('尾abababab')
    if re.search('(\\d)(\\d)\\1\\2(\\d)(\\d)\\3\\4', num[-8:]):  # ababcdcd
        type_of_card.append('ababcdcd')
    if re.search('^\\d*(\\d)\\1\\1.(\\d)\\2\\2\\d*$', num[-8:]):  # aaabcccd
        type_of_card.append('aaabcccd')
    if re.search('1688', num[-4:]):  # '1688'
        type_of_card.append('1688')
    if re.search('10086', num[-5:]):  # '10086'
        type_of_card.append('10086')
    # elif re.search('1314', num[-4:]):  # '1314'
    #     type_of_card.append('1314')
    if re.search('^\\d*(\\d)\\1\\1.(\\d)\\2(\\d)\\3.*$', num[-8:]):  # aaabccdd
        type_of_card.append('aaabccdd')
    if len(set(num)) == 3:
        type_of_card.append('3数字组合')
    if re.search('(\\d)\\1(88)', num[-4:]):
        type_of_card.append('AA88')
    if set(num) == {'1', '3', '4', '9'}:
        type_of_card.append('1349风水号')
    if ascending(num):
        type_of_card.append('*a*a*a*a')
    if re.search('(\\d)\\1(\\d)\\2(\\d)\\3(\\d)\\4', num[-8:]):
        type_of_card.append('四对')
    if num[-6:] == '678910':
        type_of_card.append('678910')
    if num[-5:] == '67890':
        type_of_card.append('67890')

    if re.search('888\\d8', num[-5:]):  # 888X8
        type_of_card.append('888X8')

    if re.search('8\\d88', num[-4:]):  # 8X88
        type_of_card.append('8X88')

    if num[-6:] == '131419':
        type_of_card.append('131419')

    if num[-6:] == '141319':
        type_of_card.append('141319')

    if num[-7:] == '1314520':
        type_of_card.append('1314520')

    if num[-7:] == '1314521':
        type_of_card.append('1314521')

    if num[-6:] == '201314':
        type_of_card.append('201314')

    if re.search('(\\d)(\\1)(\\1)520', num[-6:]):
        type_of_card.append('AAA520')

    if re.search('(\\d)(\\1)(\\1)521', num[-6:]):
        type_of_card.append('AAA521')

    # # 有问题
    # if re.search('(\\d)88(\\d)(\\d)88(\\d)', num):
    #     s, e = re.search('(\\d)88(\\d)(\\d)88(\\d)', num)
    #     num_of_interest = num[s: e]
    #     if num_of_interest[0] == num_of_interest[3] and num_of_interest[4] == num_of_interest[7]:
    #         type_of_card.append('A88AB88B')
    #
    # if re.search('8(\\d)(\\d)88(\\d)(\\d)8', num):
    #     s, e = re.search('8(\\d)(\\d)88(\\d)(\\d)8', num)
    #     num_of_interest = num[s: e]
    #     if num_of_interest[1] == num_of_interest[2] and num_of_interest[5] == num_of_interest[6]:
    #         type_of_card.append('8AA88BB8')

    return type_of_card, match_index_dict


if __name__ == '__main__':
    get_area_info()