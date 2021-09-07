from PIL import Image, ImageDraw, ImageFont
import threading, time


def worker_2(text):
    lines = []
    text = text
    while len(text) > 70:
        lines.append(text[:71])
        text = text[71::]
    lines.append(text)
    text = '\n'.join(lines)
    im = Image.new('RGB', (1920, 1080), color=('#FFFFFF'))
    font = ImageFont.truetype("arial.ttf", size=50)
    draw_text = ImageDraw.Draw(im)
    draw_text.text((100, 100), text, fill=('#000000'), font=font)
    im.show()


def worker(text):
    t = threading.Thread(target=worker_2, args=(text,))
    t.start()
    print('www')



words = ['kljdfghkdjhgdkjg', '12345', '                    5  1']

t = threading.Thread(target=worker, args=(words[0],))
t.start()

print('zzz')
