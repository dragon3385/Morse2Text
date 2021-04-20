import wave
import numpy
from collections import Counter

CODE: dict[str, str] = {
    # 26个字母
    'A': '.-', 'B': '-...', 'C': '-.-.',
    'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',

    # 10个数字
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.',

    # 16个标点符号
    ',': '--..--', '.': '.-.-.-', ':': '---...', ';': '-.-.-.',
    '?': '..--..', '=': '-...-', "'": '.----.', '/': '-..-.',
    '!': '-.-.--', '-': '-....-', '_': '..--.-', '(': '-.--.',
    ')': '-.--.-', '$': '...-..-', '&': '. . . .', '@': '.--.-.'

    # 下面还可自行添加密码字典

}
# 反转字典(作为解密摩斯密码的字典)
UNCODE: dict[str, str] = dict(map(lambda t: (t[1], t[0]), CODE.items()))


def morseAlphabetToString(morseCode: str) -> str:
    """
        将摩斯密码还原成字符串
        params:需要还原的摩斯码
    :rtype: 摩斯明文
    """
    # message用于保存解密结果
    message = ''
    for s in morseCode.split(' '):
        if s == '':
            message += ' '
        else:
            message += UNCODE[s]
    return message


def wav2Morse(fileName: str = r'C1.wav'):
    # 打开wav文件 ，open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据。
    with wave.open(fileName, 'rb') as f:
        # 读取格式信息
        # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
        # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        # 读取波形数据
        # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
        str_data = f.readframes(nframes)

    # 将波形数据转换成数组
    # 需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
    waveData = numpy.frombuffer(str_data, dtype=numpy.short)
    # 通过取样点数和取样频率计算出每个取样的时间。
    poolLenth = int(framerate * 0.01)
    waveData = numpy.array(waveData, numpy.int32)
    poolsList = []

    for i in range(0, len(waveData), poolLenth):
        poolsList.append(max(waveData[i:i + poolLenth]))
    # print(poolsList)
    # print(len(poolsList), Counter(poolsList))
    avgPoolsList = numpy.mean(poolsList)
    # print('avgPoolList:', avgPoolsList)
    binarizationList = []
    count_0 = 0
    count_1 = 0
    for i in poolsList:
        if i >= avgPoolsList:
            if count_1 == 0 and count_0 != 0:
                binarizationList.append((0, count_0))
                count_0 = 0
            count_1 += 1
        else:
            if count_0 == 0 and count_1 != 0:
                binarizationList.append((1, count_1))
                count_1 = 0
            count_0 += 1
    if count_0 == 0 and count_1 != 0:
        binarizationList.append((1, count_1))
    if count_1 == 0 and count_0 != 0:
        binarizationList.append((0, count_0))
    # print(binarizationList)
    # print(len(binarizationList), Counter(binarizationList))
    length_0 = 0
    length_1 = 0
    count_0 = 0
    count_1 = 0
    # print(dict(Counter(binarizationList)))
    for (binarization, length), count in dict(Counter(binarizationList)).items():
        if count > (len(binarizationList) / 100):
            if binarization == 0:
                length_0 += length * count
                count_0 += count
            else:
                length_1 += length * count
                count_1 += count
    morseText = ''
    for (binarization, length) in binarizationList:
        if binarization == 0:
            if length > (length_0 / count_0):
                morseText += ' '
        else:
            if length > (length_1 / count_1):
                morseText += '-'
            else:
                morseText += '.'
    print(morseText)
    print(morseAlphabetToString(morseText))
    return


if __name__ == '__main__':
    # wav2Morse(r'C1.wav')
    # wav2Morse(r'tppds.wav')
    # wav2Morse(r'az.wav')
    wav2Morse(r'wikipedia.wav')
