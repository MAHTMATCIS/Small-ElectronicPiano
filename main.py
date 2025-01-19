import time
import pygame
import mido
pygame.init()

keypos={
    "b": 69,
    "v": 67,
    "c": 65,
    "x": 64,
    "z": 62,
    "g": 60,
    "f": 59,
    "d": 57,
    "s": 55,
    "a": 53,
    "t": 52,
    "r": 50,
    "e": 48,
    "w": 47,
    "q": 45,
    "\t": 43,
    "`": 41,
    "1": 40,
    "2": 38,
    "3": 36,
    "4": 35,
    "5": 33,
    "n": 71,
    "m": 72,
    ",": 74,
    ".": 76,
    "/": 77,
    "h": 79,
    "j": 81,
    "k": 83,
    "l": 84,
    ";": 86,
    "\'": 88,
    "\r": 89,
    "y": 91,
    "u": 93,
    "i": 95,
    "o": 96,
    "p": 98,
    "[":100,
    "]": 101,
    "\\": 103,
    "=": 105,
    "-": 107,
    "0": 108,
    "9": 26,
    "8": 28,
    "7": 29,
    "6": 31,
}
hold=0
info=0


cnt=1
def messageon(note,no):
    global hold,info,cnt
    if note.unicode == ' ' and no=='on':
        hold=~hold
        output_port.send(mido.Message('control_change', control=64, value=127 if hold else 0))
    if note.key == 1073742049 and no == 'on':
        info+=1
    if note.key == 1073742049 and no == 'off':
        info-=1
    if note.key==1073741906 and no == 'on':
        info+=1
    if note.key == 1073741905 and no == 'on':
        info -= 1
    unicode=note.unicode
    unicode:str
    if note.unicode.isupper():
        unicode = unicode.lower()
    print(unicode if unicode != "\r" else "\n")
    if unicode in keypos:
        try:
            for i in range(cnt):
                output_port.send(mido.Message('note_'+no, note=keypos[unicode]+info, velocity=127))
        except:
            print('error')


# 获取可用的 MIDI 输出设备名称
output_names = mido.get_output_names()

if output_names:
    # 选择第一个可用的输出设备，你可以根据需要修改
    pass
else:
    print("Midi devices not found! 未找到 MIDI 输出设备！")
    raise SystemError("Midi devices not found! 未找到 MIDI 输出设备！")

port=None
print(output_names)
print(len(output_names),"Midi devices found:",'找到',len(output_names),"个设备，分别为：")
for i in enumerate(output_names):
    print('\tId:',i[0],' Name/名称:',i[1])
try:
    with open('port_id.txt','r') as f:
        port=int(f.read())
    print('You select: 你的选择：',output_names[port])
    print('You selection is in the file \"port_id.txt\". 你的选择在文件 \"port_id.txt\" 中。')
    print('You can change it in the file \"port_id.txt\". 你可以在文件 \"port_id.txt\" 中改变它。')
except FileNotFoundError:
    port=int(input("Please input the Midi Devices id (0,1,2...): 请输入 MIDI 输出设备 id （0、1、2...）："))
    print('You select: 你的选择：',output_names[port])
    if input("Are you sure? 你确定吗？(y/n):") != 'y':
        exit()
    print('You selection is in the file \"port_id.txt\". 你的选择在文件 \"port_id.txt\" 中。')
    print('You can change it in the file \"port_id.txt\". 你可以在文件 \"port_id.txt\" 中改变它。')
    with open('port_id.txt','w') as f:
        f.write(str(port))

if output_names:
    output_port = mido.open_output(output_names[port])

win=pygame.display.set_mode((500,500))
clock=pygame.time.Clock()
f=pygame.font.Font('nunito-bold.ttf',50)

while True:
    a=f.render("Listening!",1,(255,255,255))
    win.blit(a,(250-a.get_width()//2,250-a.get_height()//2))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            output_port.close()
            exit()
        if event.type==pygame.KEYDOWN:
            messageon(event,'on')
        if event.type == pygame.KEYUP:
            messageon(event,'off')

    clock.tick(240)
