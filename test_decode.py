import json

def parse_cat062_message(raw_data):
    """
    解析 CAT062 消息并转化为字典。
    :param raw_data: 二进制数据（bytes 或 bytearray）
    :return: 解析后的数据字典
    """
    parsed_data = {}

    # 1. 解析 CAT 和长度字段
    parsed_data['Category'] = raw_data[0]  # CAT 字段
    parsed_data['Length'] = int.from_bytes(raw_data[1:3], byteorder='big')  # 总长度

    # 2. 解析 FSPEC 字段
    fspec = []
    fspec_index = 3  # FSPEC 从第 4 字节开始
    while True:
        fspec_byte = raw_data[fspec_index]
        fspec_index += 1
        fspec.extend([bool(fspec_byte & (1 << bit)) for bit in range(7, -1, -1)])
        if fspec_byte & 0x01 == 0:  # FSPEC 扩展标志
            break
    parsed_data['FSPEC'] = fspec

    # 3. 按照 FSPEC 解析数据项
    data_items = {}
    data_start_index = fspec_index

    if fspec[0]:  # I062/010 数据源标识
        data_items['I062/010'] = {
            'SAC': raw_data[data_start_index],
            'SIC': raw_data[data_start_index + 1]
        }
        data_start_index += 2

    if fspec[1]:  # I062/015 服务识别号
        data_items['I062/015'] = raw_data[data_start_index]
        data_start_index += 1

    if fspec[2]:  # I062/040 目标报告描述
        data_items['I062/040'] = raw_data[data_start_index]
        data_start_index += 1

    if fspec[3]:  # I062/080 目标位置（WGS-84）
        latitude = int.from_bytes(raw_data[data_start_index:data_start_index + 4], 'big', signed=True) * (180 / 2**31)
        longitude = int.from_bytes(raw_data[data_start_index + 4:data_start_index + 8], 'big', signed=True) * (180 / 2**31)
        data_items['I062/080'] = {'Latitude': latitude, 'Longitude': longitude}
        data_start_index += 8

    if fspec[4]:  # I062/100 目标识别码
        data_items['I062/100'] = raw_data[data_start_index:data_start_index + 2].hex()
        data_start_index += 2

    if fspec[5]:  # I062/105 目标速度向量
        ground_speed = int.from_bytes(raw_data[data_start_index:data_start_index + 2], 'big') / 256.0
        track_angle = int.from_bytes(raw_data[data_start_index + 2:data_start_index + 4], 'big') / 256.0
        data_items['I062/105'] = {'Ground Speed': ground_speed, 'Track Angle': track_angle}
        data_start_index += 4

    if fspec[6]:  # I062/200 时间标记
        timestamp = int.from_bytes(raw_data[data_start_index:data_start_index + 3], 'big') / 128.0
        data_items['I062/200'] = {'Timestamp': timestamp}
        data_start_index += 3

    parsed_data['Data Items'] = data_items

    return parsed_data

def save_to_json(parsed_data, output_file):
    """
    保存解析后的数据为 JSON 文件。
    :param parsed_data: 解析后的数据字典
    :param output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)

# 示例输入（十六进制转换为 bytes）
raw_data = bytes.fromhex("3E0034BB7D25040203000E584F003806E501460641FD2601B70D4A000D33B3C37E2080780CCB000601000550000028002A003E04")

# 解析并保存为 JSON
parsed_message = parse_cat062_message(raw_data)
save_to_json(parsed_message, 'outputs/cat062_output.json')

print("解析完成，结果保存在 cat062_output.json 文件中。")
