import random
import tkinter as tk

import class_MJ_Pai as PaiIMG

class class_MJ_SheyPai(PaiIMG.class_MJ_Pai):
    def __init__(self):
        super().__init__()

        # 牌のリスト
        self.pais_list = list()
        # 牌山のリスト
        self.pai_yama_list = list()

        return

    # ---[1:洗牌
    def shey_pai(self):
        # 牌の合計数分の数字リストを生成
        self.pais_list = list(range(PaiIMG.TOTAL_PAI))
        # シャッフル（洗牌）
        random.shuffle(self.pais_list)

        return self.pais_list

    # ---[2:牌山作成
    def create_haiyama(self, num_player):
        # 洗牌
        pai_yama_list = self.shey_pai()

        # 牌山を17牌、2段に分ける。
        # 0:牌山上段1枚目、1:牌山下段1枚目、2:牌山上段2枚目...
        self.pai_yama_list = [
            pai_yama_list[
                PaiIMG.NUM_YAMA_STEPS*PaiIMG.NUM_YAMA*i:
                PaiIMG.NUM_YAMA_STEPS*PaiIMG.NUM_YAMA*(i+1)
            ]
            for i in range(num_player)
        ]

        return self.pai_yama_list

    # ---[3:牌種を計算
    def get_pai_kind_num(self, pai_number):
        __pai_type__ = int(pai_number/PaiIMG.NUM_PATTERN/PaiIMG.NUM_PAI)
        __pai_indv__ = int(pai_number/PaiIMG.NUM_PATTERN % PaiIMG.NUM_PAI)

        return (__pai_type__, __pai_indv__)

    # ---[4:牌のIDおよび表示文字
    def set_pai_char(self, pai_number, isAka=False):
        (__pai_type__, __pai_indv__) = self.get_pai_kind_num(pai_number)

        if __pai_type__ < PaiIMG.NUM_PATTERN and __pai_indv__ < PaiIMG.NUM_PAI:
            pai_char = self.PAI_CHAR_DEF[__pai_type__][__pai_indv__]
            pai_id = self.PAI_DEF[__pai_type__][__pai_indv__]
            if isAka:
                if __pai_type__ >= 0 and __pai_type__ <= 2 and __pai_indv__ == 5-1:
                    if (pai_number % (PaiIMG.NUM_PATTERN*PaiIMG.NUM_PAI)) % (PaiIMG.NUM_TYPES*(5-1)) == 0:
                        pai_id += 100

        return pai_char, pai_id

    # ---[5:配牌リストをIDおよび表示文字に変換
    def set_haipai_char(self, haipai, isAka=False):
        haipai_list = list()
        haipai_char_list = list()
        if isinstance(haipai, list):
            for pai in haipai:
                pai_char, pai_id = self.set_pai_char(pai, isAka)
                haipai_list.append(pai_id)
                haipai_char_list.append(pai_char)
        return haipai_list, haipai_char_list

if __name__ == '__main__':
    SPai = class_MJ_SheyPai()
    pai_yama_list = SPai.create_haiyama(num_player=4)

    W, H = 0, 1
    offset = 10
    blank = 2

    width = PaiIMG.PAI_SIZE[W]*PaiIMG.NUM_YAMA+blank*(PaiIMG.NUM_YAMA-1)+offset*2
    height = PaiIMG.PAI_SIZE[H]*(PaiIMG.NUM_YAMA_STEPS*4)+blank*(PaiIMG.NUM_YAMA_STEPS*4-1)+offset*2

    tag_head = 'PAI_'
    mk_tag = 'MARK'

    _view_ = tk.Tk()
    _view_.geometry(f'{width}x{height}+300+300')
    _view_.title('麻雀洗牌表示')

    canvas = tk.Canvas(
            _view_, bg='green', width=width, height=height)
    canvas.pack()

    def choice(pai_index):
        canvas.delete(mk_tag)
        mk_list = canvas.find_withtag(pai_index)

        print(f'{pai_index}:{len(mk_list)}')

        for oid in mk_list:
            coods = canvas.coords(oid)
            x0,y0 = coods
            canvas.create_rectangle(x0,y0,x0+PaiIMG.PAI_SIZE[W],y0+PaiIMG.PAI_SIZE[H],
                fill='yellow', stipple='gray50', tag=mk_tag)


    def click(event):
        canvas.delete(mk_tag)
        x, y = event.x, event.y
        id_list =canvas.find_overlapping(x,y,x,y)
        pai_index = None
        for oid in id_list:
            tag_list = canvas.gettags(oid)
            for tags in tag_list:
                if tag_head in tags:
                    pai_index = tags
                    break
            if pai_index is not None:
                break
        if pai_index is not None:
            choice(pai_index)

    canvas.bind('<Button-1>', click)

    iter_index_list = list()
    for l in SPai.PAI_DEF:
        iter_index_list.extend(l)

    iter_index =iter(iter_index_list)

    def after():
        try:
            tag_index = next(iter_index)
            tags = f'{tag_head}{tag_index}'
            choice(tags)

            _view_.after(1000,after)
        except:
            pass
        return

    SPai._image_pai_()

    for i, yama in enumerate(pai_yama_list):
        u_yama = yama[0::2] #インデックス0から始まる偶数は上段
        d_yama = yama[1::2] #インデックス1から始まる奇数は下段
        _u_yama_list_, _ = SPai.set_haipai_char(
            u_yama, isAka=True)
        _d_yama_list_, _ = SPai.set_haipai_char(
            d_yama, isAka=True)
        for j, img_index in enumerate(_u_yama_list_):
            img = SPai.PAI_IMG[img_index]
            tag_index = img_index%100
            canvas.create_image(
                offset+(PaiIMG.PAI_SIZE[W]+blank)*j,
                offset+((PaiIMG.PAI_SIZE[H]+blank)*(i*2)),
                image=img, anchor=tk.NW, tags=f'{tag_head}{tag_index}')
        for j, img_index in enumerate(_d_yama_list_):
            img = SPai.PAI_IMG[img_index]
            tag_index = img_index%100
            canvas.create_image(
                offset+(PaiIMG.PAI_SIZE[W]+blank)*j,
                offset+((PaiIMG.PAI_SIZE[H]+blank)*(i*2+1)),
                image=img, anchor=tk.NW, tags=f'{tag_head}{tag_index}')

    _view_.after(2000,after)
    _view_.mainloop()

