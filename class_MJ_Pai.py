import os

from PIL import Image, ImageTk, ImageDraw

import tkinter as tk

# 牌山の列数
NUM_YAMA = 17
# 牌山の段数
NUM_YAMA_STEPS = 2
# 牌種別数
NUM_PATTERN = 4
# 数字牌の種類
NUM_PAI = 9
# 風牌の種類
NUM_TSUU_PAI = 4
# 三元牌の種類
NUM_3GEN_PAI = 3
# １種類の牌数
NUM_TYPES = 4
# 牌の合計数　136
TOTAL_PAI = ((NUM_PATTERN-1)*NUM_PAI+NUM_TSUU_PAI+NUM_3GEN_PAI)*NUM_TYPES

# 表示牌サイズ
PAI_SIZE = (30, 40)


class class_MJ_Pai (object):
    # ---[0:初期値
    def __init__(self):
        self._init_PAT_()

        return

    def _init_PAT_(self):

        self.PAI_CHAR_DEF = [
            # デバッグ用表示（環境依存）
            # 萬子
            ['一', 'ニ', '三', '四', '五', '六', '七', '八', '九'],
            # 筒子
            ['➀', '➁', '➂', '➃', '➄', '➅', '➆', '➇', '➈'],
            # 索子
            ['１', '２', '３', '４', '５', '６', '７', '８', '９'],
            # 字牌
            ['東', '南', '西', '北', '⬜︎', '発', '中'],
        ]

        self.PAI_DEF = [
            # 萬子
            [i for i in range(11, 11+NUM_PAI)],
            # 筒子
            [i for i in range(21, 21+NUM_PAI)],
            # 索子
            [i for i in range(31, 31+NUM_PAI)],
            # 字牌(東南西北白発中)
            [i for i in range(41, 41+NUM_TSUU_PAI)] + \
            [i for i in range(51, 51+NUM_3GEN_PAI)],
        ]

        return

    def _image_pai_(self):
        # imageフォルダ内のファイル名称特定
        self.HEAD_N_DEF = [
            'man', 'pin', 'sou', 'ji',
        ]
        TSUU_N_DEF = [
            '-ton', '-nan', '-sha', '-pei', '-haku', '-hatsu', '-chun',
        ]
        _ura_ = 'ura'
        _aka_ = '-aka5'
        _e_ = '.gif'

        _image_path_ = os.path.abspath("image")

        # イメージオブジェクトを格納する辞書　ROTATEは90度回転
        self.PAI_IMG = dict()
        self.PAI_ROTATE_IMG = dict()

        f_path = os.path.join(_image_path_, _ura_ + _e_)
        _img_obj_ = Image.open(f_path).resize(PAI_SIZE)
        _img_ = ImageTk.PhotoImage(_img_obj_)
        self.PAI_IMG_URA = _img_

        for i, types in enumerate(self.PAI_DEF):
            _header_ = self.HEAD_N_DEF[i]
            for j, hai in enumerate(types):
                if i == 3:
                    _num_ = str(j+1) + TSUU_N_DEF[j]
                else:
                    _num_ = str(j+1)
                f_path = os.path.join(_image_path_, _header_ + _num_ + _e_)
                _img_obj_ = Image.open(f_path).resize(PAI_SIZE)
                _img_ = ImageTk.PhotoImage(_img_obj_)
                self.PAI_IMG.setdefault(hai, _img_)
                _img_obj_r = _img_obj_.rotate(90, expand=True)
                _img_ = ImageTk.PhotoImage(_img_obj_r)
                self.PAI_ROTATE_IMG.setdefault(hai, _img_)
        else:
            # 赤牌は100を足す
            aka5 = [115, 125, 135]
            for i, key in enumerate(aka5):
                f_path = os.path.join(
                    _image_path_, self.HEAD_N_DEF[i] + _aka_ + _e_)
                _img_obj_ = Image.open(f_path).resize(PAI_SIZE)
                _img_ = ImageTk.PhotoImage(_img_obj_)
                self.PAI_IMG.setdefault(key, _img_)
                _img_obj_r = _img_obj_.rotate(90, expand=True)
                _img_ = ImageTk.PhotoImage(_img_obj_r)
                self.PAI_ROTATE_IMG.setdefault(key, _img_)

        return


if __name__ == '__main__':
    Pai = class_MJ_Pai()

    W, H = 0, 1
    offset = 10
    blank = 2

    width = PAI_SIZE[W]*NUM_PAI+blank*(NUM_PAI-1)+offset*2
    height = PAI_SIZE[H]*(NUM_TYPES*4)+blank*(NUM_TYPES*4-1)+offset*2

    _view_ = tk.Tk()
    _view_.geometry(f'{width}x{height}+300+300')
    _view_.title('麻雀牌画像表示')

    Pai._image_pai_()

    canvas = tk.Canvas(
        _view_, bg='green', width=width, height=height)
    canvas.pack()

    # 全種類表示テスト
    for y, types in enumerate(Pai.PAI_DEF):
        for x, hai in enumerate(types):
            for i in range(4):
                if i == 3 and hai % 10 == 5 and hai < 40:
                    hai += 100
                img = Pai.PAI_IMG[hai]
                canvas.create_image(
                    offset+(PAI_SIZE[W]+blank)*x,
                    offset+((PAI_SIZE[H]+blank)*i)+((PAI_SIZE[H]+blank)*4)*y,
                    image=img, anchor=tk.NW)

    _view_.mainloop()
