from Logic import *
from Komoran import *
from DAO import *

class InlineQuery:
    def __init__(self):
        self.ngrok = 'https://7e7e-118-36-193-8.ngrok.io'
        self.logic = Logic()
        self.dao = JjalDao()

    def CreateInline(self, urls):
        if len(urls) == 1:
            if 'gif' in urls[0]:
                inline1 = InlineQueryResultGif(
                id=str(uuid4()),
                type='gif',
                gif_width = 400,
                gif_url= urls[0],
                thumb_url= urls[0])
            elif 'mp4' in urls[0]:
                inline1 = InlineQueryResultMpeg4Gif(
                id=str(uuid4()),
                mpeg4_width = 400,
                type='mpeg4_gif',
                mpeg4_url= urls[0],
                thumb_url= urls[0])
            else:
                inline1 = InlineQueryResultPhoto(
                id=str(uuid4()),
                type='photo',
                photo_width = 400,
                photo_url= urls[0],
                thumb_url= urls[0])
            results = [inline1]

        elif len(urls) == 2:
            if 'gif' in urls[0]:
                inline1 = InlineQueryResultGif(
                id=str(uuid4()),
                type='gif',
                gif_width = 400,
                gif_url= urls[0],
                thumb_url= urls[0])
            elif 'mp4' in urls[0]:
                inline1 = InlineQueryResultMpeg4Gif(
                id=str(uuid4()),
                type='mpeg4_gif',
                mpeg4_width = 400,
                mpeg4_url= urls[0],
                thumb_url= urls[0])
            else:
                inline1 = InlineQueryResultPhoto(
                id=str(uuid4()),
                type='photo',
                photo_width = 400,
                photo_url= urls[0],
                thumb_url= urls[0])
                results = [inline1]
            if 'gif' in urls[1]:
                inline2 = InlineQueryResultGif(
                id=str(uuid4()),
                type='gif',
                gif_width = 400,
                gif_url= urls[1],
                thumb_url= urls[1])
            elif 'mp4' in urls[1]:
                inline2 = InlineQueryResultMpeg4Gif(
                id=str(uuid4()),
                type='mpeg4_gif',
                mpeg4_width = 400,
                mpeg4_url= urls[1],
                thumb_url= urls[1])
            else:
                inline2 = InlineQueryResultPhoto(
                id=str(uuid4()),
                type='photo',
                photo_width = 400,
                photo_url= urls[1],
                thumb_url= urls[1])
                results = [inline1]
            results = [inline1, inline2]

        else:
            if 'gif' in urls[0]:
                inline1 = InlineQueryResultGif(
                id=str(uuid4()),
                type='gif',
                gif_height = 400,
                gif_url= urls[0],
                thumb_url= urls[0])
            elif 'mp4' in urls[0]:
                inline1 = InlineQueryResultMpeg4Gif(
                id=str(uuid4()),
                type='mpeg4_gif',
                mpeg4_width = 400,
                mpeg4_url= urls[0],
                thumb_url= urls[0])
            else:
                inline1 = InlineQueryResultPhoto(
                id=str(uuid4()),
                type='photo',
                photo_width = 400,
                photo_url= urls[0],
                thumb_url= urls[0])
            if 'gif' in urls[1]:
                inline2 = InlineQueryResultGif(
                id=str(uuid4()),
                type='gif',
                gif_width = 400,
                gif_url= urls[1],
                thumb_url= urls[1])
            elif 'mp4' in urls[1]:
                inline2 = InlineQueryResultMpeg4Gif(
                id=str(uuid4()),
                type='mpeg4_gif',
                mpeg4_width = 400,
                mpeg4_url= urls[1],
                thumb_url= urls[1])
            else:
                inline2 = InlineQueryResultPhoto(
                id=str(uuid4()),
                type='photo',
                photo_width = 400,
                photo_url= urls[1],
                thumb_url= urls[1])
            if 'gif' in urls[2]:
                inline3 = InlineQueryResultGif(
                id=str(uuid4()),
                type='gif',
                gif_width = 400,
                gif_url= urls[2],
                thumb_url= urls[2])
            elif 'mp4' in urls[2]:
                inline3 = InlineQueryResultMpeg4Gif(
                id=str(uuid4()),
                type='mpeg4_gif',
                mpeg4_width = 400,
                mpeg4_url= urls[2],
                thumb_url= urls[2])
            else:
                inline3 = InlineQueryResultPhoto(
                id=str(uuid4()),
                type='photo',
                photo_width = 400,
                photo_url= urls[2],
                thumb_url= urls[2])
            results = [inline1, inline2, inline3]
        return results

    def sentence_to_url(self, query):
        self.logic.komoran(query)
        self.logic.dao_split()
        address = logic.result()
        urls = []
        for i in address:
            urls.append(f'{self.ngrok}/Img/img/{i}')
        return urls

    def mal_to_url(self, query):
        address = self.logic.mal_logic(query)
        urls = []
        # adress는 ['OOO.jpg, 25, 30, 14, 20', 'OOO.gif, 22, 35, 16, 25']처럼 구성됨
        # max_len은 이미 logic에서 걸러짐
        if len(address) == 1:
            img1 = Image.open(f'../mal/{address[0][0]}')
            tex = query.replace('.말', '')[3:]

            x, y, fs = int(address[0][1]), int(address[0][2]), int(address[0][4])
            fnt = ImageFont.truetype('MaruBuri-SemiBold.ttf', fs, encoding='utf-8')
            draw1 = ImageDraw.Draw(img1)
            W, H = draw1.textsize(tex, font=fnt)
            w, h = img1.size
            draw1.text((x - (W // 2), y - (H // 2)), text=tex, font=fnt, fill="black")
            name = ''
            for i in tex:
                name += str(ord(i))
            img1.save(f'../ramdisk/{name}{address[0][0]}')
            for i in address:
                urls.append(f'{ngrok}/Img/mal/{name}{i[0]}')
            CreateInline(urls)

        elif len(address) == 2:
            img1 = Image.open(f'../mal/{address[0][0]}')
            img2 = Image.open(f'../mal/{address[1][0]}')
            tex = query.replace('.말', '')[3:]
            x1, y1, fs1 = int(address[0][1]), int(address[0][2]), int(address[0][4])
            x2, y2, fs2 = int(address[1][1]), int(address[1][2]), int(address[1][4])
            fnt1 = ImageFont.truetype('MaruBuri-SemiBold.ttf', fs1, encoding='utf-8')
            fnt2 = ImageFont.truetype('MaruBuri-SemiBold.ttf', fs2, encoding='utf-8')
            draw1 = ImageDraw.Draw(img1)
            draw2 = ImageDraw.Draw(img2)
            W1, H1 = draw1.textsize(tex, font=fnt1)
            w1, h1 = img1.size
            W2, H2 = draw2.textsize(tex, font=fnt2)
            w2, h2 = img2.size
            draw1.text((x1 - (W1 // 2), y1 - (H1 // 2)), text=tex, font=fnt1, fill="black")
            draw2.text((x2 - (W2 // 2), y2 - (H2 // 2)), text=tex, font=fnt2, fill="black")
            name = ''
            for i in tex:
                name += str(ord(i))
            img1.save(f'../ramdisk/{name}{address[0][0]}')
            img2.save(f'../ramdisk/{name}{address[1][0]}')
            for i in address:
                urls.append(f'{ngrok}/Img/mal/{name}{i[0]}')
            CreateInline(urls)

        elif len(address) == 3:
            img1 = Image.open(f'../mal/{address[0][0]}')
            img2 = Image.open(f'../mal/{address[1][0]}')
            img3 = Image.open(f'../mal/{address[2][0]}')
            tex = query.replace('.말', '')[3:]
            x1, y1, fs1 = int(address[0][1]), int(address[0][2]), int(address[0][4])
            x2, y2, fs2 = int(address[1][1]), int(address[1][2]), int(address[1][4])
            x3, y3, fs3 = int(address[2][1]), int(address[2][2]), int(address[2][4])
            fnt1 = ImageFont.truetype('MaruBuri-SemiBold.ttf', fs1, encoding='utf-8')
            fnt2 = ImageFont.truetype('MaruBuri-SemiBold.ttf', fs2, encoding='utf-8')
            fnt3 = ImageFont.truetype('MaruBuri-SemiBold.ttf', fs3, encoding='utf-8')
            draw1 = ImageDraw.Draw(img1)
            draw2 = ImageDraw.Draw(img2)
            draw3 = ImageDraw.Draw(img3)
            W1, H1 = draw1.textsize(tex, font=fnt1)
            w1, h1 = img1.size
            W2, H2 = draw2.textsize(tex, font=fnt2)
            w2, h2 = img2.size
            W3, H3 = draw3.textsize(tex, font=fnt3)
            w3, h3 = img3.size
            draw1.text((x1 - (W1 // 2), y1 - (H1 // 2)), text=tex, font=fnt1, fill="black")
            draw2.text((x2 - (W2 // 2), y2 - (H2 // 2)), text=tex, font=fnt2, fill="black")
            draw3.text((x3 - (W3 // 2), y3 - (H3 // 2)), text=tex, font=fnt3, fill="black")
            name = ''
            for i in tex:
                name += str(ord(i))
            img1.save(f'../ramdisk/{name}{address[0][0]}')
            img2.save(f'../ramdisk/{name}{address[1][0]}')
            img3.save(f'../ramdisk/{name}{address[2][0]}')
            for i in address:
                urls.append(f'{self.ngrok}/Img/mal/{name}{i[0]}')
        return urls