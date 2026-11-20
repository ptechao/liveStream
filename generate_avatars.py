import os
import math
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('assets/avatars', exist_ok=True)

def create_photorealistic_avatar(filename, theme="female_pro"):
    # 建立 600x800 高解析度擬真主播畫像
    w, h = 600, 800
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # 1. 溫暖景深虛化直播間背景
    bg = Image.new("RGBA", (w, h), (15, 18, 30, 255))
    bg_draw = ImageDraw.Draw(bg)
    if theme == "female_pro":
        # 暖金與柔紫奢華演播室背景
        for i in range(h):
            r = int(25 + (i / h) * 15)
            g = int(20 + (i / h) * 10)
            b = int(45 + (i / h) * 20)
            bg_draw.line([(0, i), (w, i)], fill=(r, g, b, 255))
        # 散景光斑
        bg_draw.ellipse([80, 100, 220, 240], fill=(255, 180, 80, 45))
        bg_draw.ellipse([400, 80, 560, 240], fill=(138, 43, 226, 40))
        bg_draw.ellipse([300, 280, 480, 460], fill=(255, 46, 99, 35))
    elif theme == "male_hype":
        # 賽博藍紫與潮流霓虹燈背景
        for i in range(h):
            r = int(12 + (i / h) * 10)
            g = int(18 + (i / h) * 25)
            b = int(35 + (i / h) * 45)
            bg_draw.line([(0, i), (w, i)], fill=(r, g, b, 255))
        bg_draw.ellipse([50, 120, 250, 320], fill=(8, 217, 214, 50))
        bg_draw.ellipse([380, 150, 550, 320], fill=(255, 46, 99, 45))
    else:
        # 甜美清新粉橘調背景
        for i in range(h):
            r = int(35 + (i / h) * 20)
            g = int(20 + (i / h) * 15)
            b = int(35 + (i / h) * 20)
            bg_draw.line([(0, i), (w, i)], fill=(r, g, b, 255))
        bg_draw.ellipse([100, 100, 260, 260], fill=(255, 140, 170, 50))
        bg_draw.ellipse([360, 180, 500, 320], fill=(255, 200, 120, 45))

    bg = bg.filter(ImageFilter.GaussianBlur(12))
    im.paste(bg, (0, 0))
    draw = ImageDraw.Draw(im)

    cx = w // 2
    cy = 380

    # 2. 身體與服裝 (立體打光)
    body_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(body_im)

    if theme == "female_pro":
        # 高級絲絨深藍修身西裝
        bdraw.polygon([
            (cx - 180, h), (cx - 150, 540), (cx - 75, 490),
            (cx + 75, 490), (cx + 150, 540), (cx + 180, h)
        ], fill=(26, 36, 68, 255))
        # 內搭白襯衫與V領線條
        bdraw.polygon([
            (cx - 45, 490), (cx, 590), (cx + 45, 490)
        ], fill=(245, 245, 250, 255))
    elif theme == "male_hype":
        # 潮流黑色連帽衫與金項鍊
        bdraw.polygon([
            (cx - 200, h), (cx - 165, 520), (cx - 80, 480),
            (cx + 80, 480), (cx + 165, 520), (cx + 200, h)
        ], fill=(22, 24, 32, 255))
        # 金項鍊
        bdraw.arc([cx - 40, 520, cx + 40, 590], 0, 180, fill=(255, 200, 50, 255), width=5)
    else:
        # 柔粉甜美針織衫
        bdraw.polygon([
            (cx - 180, h), (cx - 145, 530), (cx - 70, 490),
            (cx + 70, 490), (cx + 145, 530), (cx + 180, h)
        ], fill=(235, 120, 150, 255))

    im.alpha_composite(body_im)
    draw = ImageDraw.Draw(im)

    # 3. 頸部
    neck_color = (248, 218, 200, 255) if theme != "male_hype" else (235, 205, 185, 255)
    draw.polygon([
        (cx - 36, 420), (cx - 42, 510), (cx + 42, 510), (cx + 36, 420)
    ], fill=neck_color)

    # 4. 臉部底色 (精緻鵝蛋臉輪廓)
    face_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(face_im)

    # 臉型多邊形平滑控制點
    fdraw.polygon([
        (cx - 88, 300), (cx - 86, 360), (cx - 75, 410),
        (cx - 48, 460), (cx, 480), (cx + 48, 460),
        (cx + 75, 410), (cx + 86, 360), (cx + 88, 300),
        (cx + 80, 240), (cx, 220), (cx - 80, 240)
    ], fill=neck_color)

    im.alpha_composite(face_im)
    draw = ImageDraw.Draw(im)

    # 5. 精緻腮紅與高光
    blush_color = (255, 130, 150, 45) if theme != "male_hype" else (220, 140, 130, 30)
    draw.ellipse([cx - 72, 360, cx - 32, 400], fill=blush_color)
    draw.ellipse([cx + 32, 360, cx + 72, 400], fill=blush_color)

    # 6. 眉毛
    brow_color = (45, 30, 25, 230)
    if theme == "male_hype":
        draw.line([(cx - 65, 308), (cx - 20, 304)], fill=brow_color, width=4)
        draw.line([(cx + 20, 304), (cx + 65, 308)], fill=brow_color, width=4)
    else:
        draw.line([(cx - 62, 312), (cx - 40, 305), (cx - 18, 312)], fill=brow_color, width=3)
        draw.line([(cx + 18, 312), (cx + 40, 305), (cx + 62, 312)], fill=brow_color, width=3)

    # 7. 擬真眼睛 (鞏膜、虹膜、瞳孔、環形燈環高光)
    for side in [-1, 1]:
        ex = cx + side * 42
        ey = 332
        # 眼眶底
        draw.ellipse([ex - 22, ey - 10, ex + 22, ey + 10], fill=(255, 255, 255, 240))
        # 虹膜
        iris_color = (40, 28, 22, 255) if theme != "male_hype" else (30, 45, 65, 255)
        draw.ellipse([ex - 10, ey - 9, ex + 10, ey + 9], fill=iris_color)
        # 瞳孔
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(10, 10, 12, 255))
        # 擬真環形補光燈高光 (攝影級 Catchlight)
        draw.arc([ex - 7, ey - 7, ex + 7, ey + 7], 45, 220, fill=(255, 255, 255, 230), width=2)
        draw.ellipse([ex + 2, ey - 5, ex + 5, ey - 2], fill=(255, 255, 255, 255))
        # 上眼線與睫毛
        draw.arc([ex - 23, ey - 12, ex + 23, ey + 8], 190, 350, fill=(30, 20, 18, 255), width=3)

    # 8. 鼻樑與鼻尖
    draw.line([(cx, 335), (cx, 380)], fill=(225, 185, 165, 140), width=2)
    draw.ellipse([cx - 9, 382, cx + 9, 393], fill=(235, 190, 170, 210))
    draw.ellipse([cx - 8, 388, cx - 3, 393], fill=(180, 130, 115, 160))
    draw.ellipse([cx + 3, 388, cx + 8, 393], fill=(180, 130, 115, 160))

    # 9. 擬真嘴唇底色 (開播時由前端 Canvas 疊加即時語音口型)
    lip_base = (205, 55, 80, 240) if theme != "male_hype" else (195, 95, 90, 220)
    draw.polygon([
        (cx - 28, 428), (cx - 10, 422), (cx, 425),
        (cx + 10, 422), (cx + 28, 428), (cx + 18, 436),
        (cx, 438), (cx - 18, 436)
    ], fill=lip_base)
    # 唇部中央陰影縫
    draw.line([(cx - 22, 429), (cx + 22, 429)], fill=(120, 20, 35, 255), width=2)

    # 10. 頭髮 (飄逸立體層次)
    hair_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(hair_im)
    hair_col = (30, 20, 18, 255) if theme == "female_pro" else ((20, 20, 25, 255) if theme == "male_hype" else (70, 40, 35, 255))
    highlight_col = (85, 55, 45, 150)

    if theme == "female_pro":
        # 大波浪優雅黑長髮
        hdraw.polygon([
            (cx - 95, 300), (cx - 110, 420), (cx - 105, 580),
            (cx - 75, 590), (cx - 65, 430), (cx - 80, 280)
        ], fill=hair_col)
        hdraw.polygon([
            (cx + 95, 300), (cx + 110, 420), (cx + 105, 580),
            (cx + 75, 590), (cx + 65, 430), (cx + 80, 280)
        ], fill=hair_col)
        # 頭頂與偏分瀏海
        hdraw.ellipse([cx - 105, 180, cx + 105, 320], fill=hair_col)
        # 偏分髮絲
        hdraw.polygon([
            (cx - 95, 240), (cx - 20, 290), (cx + 85, 260), (cx, 200)
        ], fill=hair_col)
    elif theme == "male_hype":
        # 潮流層次碎蓋髮型
        hdraw.ellipse([cx - 98, 175, cx + 98, 290], fill=hair_col)
        for i in range(-5, 6):
            hdraw.polygon([
                (cx + i * 16 - 8, 235), (cx + i * 16, 280), (cx + i * 16 + 8, 235)
            ], fill=hair_col)
    else:
        # 甜美韓系鎖骨微捲
        hdraw.ellipse([cx - 102, 185, cx + 102, 310], fill=hair_col)
        hdraw.polygon([
            (cx - 100, 280), (cx - 105, 520), (cx - 70, 460), (cx - 80, 280)
        ], fill=hair_col)
        hdraw.polygon([
            (cx + 100, 280), (cx + 105, 520), (cx + 70, 460), (cx + 80, 280)
        ], fill=hair_col)
        # 空氣瀏海
        hdraw.ellipse([cx - 45, 260, cx + 45, 295], fill=hair_col)

    im.alpha_composite(hair_im)

    # 存檔
    out_path = os.path.join('assets/avatars', filename)
    im.save(out_path, 'PNG')
    print(f"Generated {out_path} ({w}x{h})")

create_photorealistic_avatar("elena_pro.png", "female_pro")
create_photorealistic_avatar("lucas_hype.png", "male_hype")
create_photorealistic_avatar("mia_sweet.png", "female_sweet")
