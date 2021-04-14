import copy
import pickle
import random
import tkinter as tk

import class_MJ_Pai as PaiIMG
import class_MJ_SheyPai as Pai

class Test_Haipai(Pai.class_MJ_SheyPai):
    def __init__(self):
        super().__init__()

        self.select_choice = None
        self.select_haipai = None
        self.haipai = [None for _ in range(14)]
        self.haipai_list = list()
        self.naki_list = list()

        self.mk_tag = 'MARK'
        self.tag_head = 'PAI_'
        self.tag_frame_head = 'FRAME_'
        self.sel_tag = 'SEL_'
        self.naki_tag = 'NAKI_'

        self.memnumber = 0

    def create_dialog(self):
        W, H = 0, 1
        self.offset = 10
        self.blank = 2

        # ボタンエリアの大きさ
        b_width = 0
        b_height = 24

        # 牌選択エリアの大きさ
        c_width = PaiIMG.PAI_SIZE[W]*(PaiIMG.NUM_PAI+1)+self.blank*(PaiIMG.NUM_PAI)+self.offset*2
        c_height = PaiIMG.PAI_SIZE[H]*(PaiIMG.NUM_PATTERN)+self.blank*(PaiIMG.NUM_PATTERN-1)+self.offset*2
        # 手牌エリアの大きさ
        h_width = PaiIMG.PAI_SIZE[W]*(13+1)+self.blank*2*(13-1+4)+self.offset*2
        h_height = PaiIMG.PAI_SIZE[H]*(1)+self.offset*2
        # 鳴き牌エリアの大きさ
        n_width = PaiIMG.PAI_SIZE[H]*(4*4)+self.blank*2*(4*4-1)+self.offset*2
        n_height = PaiIMG.PAI_SIZE[H]*(1)+self.offset*2

        # ダイアログ
        self.view_dialog = tk.Tk()
        self.view_dialog.geometry(f'{max(b_width,c_width,h_width,n_width)}x{b_height*2+c_height+h_height+n_height+5*4}+300+300')
        self.view_dialog.title('麻雀配牌エディタ')
        self.view_dialog.resizable(0,0)

        # メニュー実装
        self.menubar = tk.Menu(
            self.view_dialog,
        )
        self.file_menu = tk.Menu(
            self.menubar,
            tearoff=0
        )

        self.menubar.add_cascade(label='ファイル', menu=self.file_menu)
        self.file_menu.add_command(label='開く',command=self.file_open)
        self.file_menu.add_command(label='保存',command=self.file_save)

        self.view_dialog.config(menu=self.menubar)

        InFrame = tk.Frame(self.view_dialog)
        InFrame0 = tk.Frame(self.view_dialog)
        InFrame1 = tk.Frame(self.view_dialog)
        InFrame2 = tk.Frame(self.view_dialog)
        InFrame3 = tk.Frame(self.view_dialog)

        self.txtMemNum = tk.StringVar()
        self.strMemnumber()

        self.labelM = tk.Label(InFrame, width=6, text="メモリ：")
        self.labelNum = tk.Label(InFrame, width=4, textvariable=self.txtMemNum)
        self.btn_back = tk.Button(
            InFrame, width=4, text='<<',command=self.list_back)
        self.btn_forword = tk.Button(
            InFrame, width=4, text='>>',command=self.list_forword)
        self.btn_mem = tk.Button(
            InFrame, width=4, text='登録',command=self.list_save)
        self.btn_delete = tk.Button(
            InFrame, width=4, text='削除',command=self.list_delete)

        self.labelM.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.labelNum.pack(side=tk.LEFT,anchor=tk.W,padx=2)

        self.btn_back.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_forword.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_mem.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_delete.pack(side=tk.LEFT,anchor=tk.W,padx=2)

        self.spinboxBa = tk.Spinbox(
            InFrame0, width=5, values=('東', '南', '西', '北'))
        self.labelBa = tk.Label(InFrame0, width=4, text="場")

        self.spinboxKyoku = tk.Spinbox(
            InFrame0, width=5, values=(1, 2, 3, 4))
        self.labelKyoku = tk.Label(InFrame0, width=4, text="局")

        self.spinboxTya = tk.Spinbox(
            InFrame0, width=5, values=('東', '南', '西', '北'))
        self.labelTya = tk.Label(InFrame0, width=4, text="家")

        self.btn_pon = tk.Button(
            InFrame0, width=4, text='吃',command=self.cmd_pon)
        self.btn_chey = tk.Button(
            InFrame0, width=4, text='碰',command=self.cmd_chey)
        self.btn_mkan = tk.Button(
            InFrame0, width=4, text='明槓',command=self.cmd_mkan)
        self.btn_akan = tk.Button(
            InFrame0, width=4, text='暗槓',command=self.cmd_akan)
        self.btn_tsumo = tk.Button(
            InFrame0, width=4, text='自模',command=self.cmd_tsumo)
        self.btn_ron = tk.Button(
            InFrame0, width=4, text='栄和',command=self.cmd_ron)

        self.spinboxBa.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.labelBa.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.spinboxKyoku.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.labelKyoku.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.spinboxTya.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.labelTya.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_pon.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_chey.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_mkan.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_akan.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_tsumo.pack(side=tk.LEFT,anchor=tk.W,padx=2)
        self.btn_ron.pack(side=tk.LEFT,anchor=tk.W,padx=2)

        self.choice_canvas = tk.Canvas(
                InFrame1, bg='green', width=max(b_width,c_width,h_width,n_width), height=c_height)
        self.choice_canvas.pack()

        self.choice_canvas.bind('<Button-1>',self._choice_click_)

        self.haipai_canvas = tk.Canvas(
                InFrame2, bg='darkgreen', width=max(b_width,c_width,h_width,n_width), height=h_height)
        self.haipai_canvas.pack()

        self.haipai_canvas.bind('<Button-1>',self._haipai_click_)
        self.haipai_canvas.bind('<Button-3>',self._haipai_right_click_)

        self.naki_canvas = tk.Canvas(
                InFrame3, bg='darkgreen', width=max(b_width,c_width,h_width,n_width), height=n_height)
        self.naki_canvas.pack()

        self.naki_canvas.bind('<Button-3>',self._naki_right_click_)

        InFrame.pack(padx=2,anchor=tk.W)
        InFrame0.pack(padx=2,anchor=tk.W)
        InFrame1.pack()
        InFrame2.pack()
        InFrame3.pack()

        self._image_pai_()

        self._lineup_choice_()
        self._haipai_farame_()

        self.view_dialog.mainloop()

    def strMemnumber(self):
        max_number = len(self.haipai_list)

        if self.memnumber < max_number:
            txt = f'{self.memnumber}'
        else:
            txt = f'({self.memnumber})'

        self.txtMemNum.set(txt)

        return

    def _lineup_choice_(self):
        W, H = 0, 1

        for i, l in enumerate(self.PAI_DEF):
            for j, img_index in enumerate(l):
                img = self.PAI_IMG[img_index]
                self.choice_canvas.create_image(
                    self.offset+(PaiIMG.PAI_SIZE[W]+self.blank)*j,
                    self.offset+((PaiIMG.PAI_SIZE[H]+self.blank)*(i)),
                    image=img, anchor=tk.NW, tags=f'{self.tag_head}{img_index}')
            else:
                if i < 3:
                    aka = [115,125,135]
                    img_index = aka[i]
                    img = self.PAI_IMG[img_index]
                    self.choice_canvas.create_image(
                        self.offset+(PaiIMG.PAI_SIZE[W]+self.blank)*(j+1),
                        self.offset+((PaiIMG.PAI_SIZE[H]+self.blank)*(i)),
                        image=img, anchor=tk.NW, tags=f'{self.tag_head}{img_index}')

        return

    def _haipai_farame_(self):
        W, H = 0, 1

        for i in range(14):
            x0 = self.offset+PaiIMG.PAI_SIZE[W]*i+(self.blank*2)*(i+int(i/(14-1))*2)
            y0 = self.offset
            self.haipai_canvas.create_rectangle(
                    x0,y0,x0+PaiIMG.PAI_SIZE[W],y0+PaiIMG.PAI_SIZE[H],
                    fill='gray', stipple='gray50', tag=f'{self.tag_frame_head}{i}'
            )

    def _choice_click_(self,event):
        W, H = 0, 1
        canvas = self.choice_canvas
        canvas.delete(self.mk_tag)
        x, y = event.x, event.y
        id_list =canvas.find_overlapping(x,y,x,y)
        pai_index = None
        for oid in id_list:
            tag_list = canvas.gettags(oid)
            for tags in tag_list:
                if self.tag_head in tags:
                    pai_index = tags
                    break
            if pai_index is not None:
                break
        if pai_index is not None:

            mk_list = canvas.find_withtag(pai_index)

            for oid in mk_list:
                coods = canvas.coords(oid)
                x0,y0 = coods
                canvas.create_rectangle(x0,y0,x0+PaiIMG.PAI_SIZE[W],y0+PaiIMG.PAI_SIZE[H],
                    fill='yellow', stipple='gray50', tag=self.mk_tag)
        self.select_choice = pai_index

        if self.select_choice is not None and self.select_haipai is not None:
            self.set_haipai()

    def _haipai_click_(self,event):
        W, H = 0, 1
        canvas = self.haipai_canvas
        canvas.delete(self.mk_tag)
        x, y = event.x, event.y
        id_list =canvas.find_overlapping(x,y,x,y)
        pai_index = None
        for oid in id_list:
            tag_list = canvas.gettags(oid)
            for tags in tag_list:
                if self.tag_frame_head in tags:
                    pai_index = tags
                    break
            if pai_index is not None:
                break
        if pai_index is not None:

            mk_list = canvas.find_withtag(pai_index)

            for oid in mk_list:
                coods = canvas.coords(oid)
                x0,y0,x1,y1 = coods
                canvas.create_rectangle(x0,y0,x1,y1,
                    fill='yellow', stipple='gray50', tag=self.mk_tag)
        self.select_haipai = pai_index

        if self.select_choice is not None and self.select_haipai is not None:
            self.set_haipai()

    def _merge_pai_(self):
        naki_pai_list= list()

        for naki in self.naki_list:
            for val in naki.values():
                pai_list = val['pai']
                naki_pai_list.extend(pai_list)

        pai_list = self.haipai + naki_pai_list

        return pai_list

    def set_haipai(self):
        W, H = 0, 1
        canvas = self.haipai_canvas
        coods = canvas.coords(self.select_haipai)
        x0,y0,x1,y1 = coods

        if self.tag_frame_head in self.select_haipai:
            hindex = self.select_haipai.strip(self.tag_frame_head)
            hindex = int(hindex)

        if self.tag_head in self.select_choice:
            index = self.select_choice.strip(self.tag_head)
            index = int(index)

            pai_list = self._merge_pai_()

            if pai_list.count(index) < 4:
                if index > 100 and pai_list.count(index) > 0:
                    return

                if index%10 == 5 and pai_list.count(index) > 3:
                    return

                if self.haipai.count(None) -len(self.naki_list)*3 <= 0:
                    return

                self._draw_haipai_(pai_index=index,pos_index=hindex)

                self.haipai[hindex] = index

        return

    def _draw_haipai_(self,pai_index,pos_index):
        W, H = 0, 1

        canvas = self.haipai_canvas

        img = self.PAI_IMG[pai_index]

        x = self.offset+PaiIMG.PAI_SIZE[W]*pos_index+(self.blank*2)*(pos_index+int(pos_index/(14-1))*2)
        y = self.offset

        canvas.delete(f'{self.sel_tag}{pos_index}')
        canvas.create_image(
            x,y,image=img, anchor=tk.NW, tags=f'{self.sel_tag}{pos_index}')

        canvas.tag_raise(self.mk_tag)

        return

    def _haipai_right_click_(self,event):
        W, H = 0, 1
        canvas = self.haipai_canvas
        x, y = event.x, event.y
        id_list =canvas.find_overlapping(x,y,x,y)
        pai_index = None
        for oid in id_list:
            tag_list = canvas.gettags(oid)
            for tags in tag_list:
                if self.tag_frame_head in tags:
                    pai_index = tags
                    break
            if pai_index is not None:
                break
        if pai_index is not None:
            hindex = pai_index.strip(self.tag_frame_head)
            hindex = int(hindex)
            mk_list = canvas.find_withtag(f'{self.sel_tag}{hindex}')

            for oid in mk_list:
                canvas.delete(oid)

            self.haipai[hindex] = None

    def _naki_right_click_(self,event):
        W, H = 0, 1
        canvas = self.naki_canvas
        x, y = event.x, event.y
        id_list =canvas.find_overlapping(x,y,x,y)
        pai_index = None
        for oid in id_list:
            tag_list = canvas.gettags(oid)
            for tags in tag_list:
                if self.naki_tag in tags:
                    pai_index = tags
                    break
            if pai_index is not None:
                break
        if pai_index is not None:
            canvas.delete(f'{pai_index}')
            naki_index = int(pai_index.strip(self.naki_tag))

            for index in range(naki_index+1,len(self.naki_list)):
                deltag = f'{self.naki_tag}{index}'
                addtag = f'{self.naki_tag}{index-1}'
                oid_list = canvas.find_withtag(deltag)
                for oid in oid_list:
                    canvas.dtag(oid,deltag)
                    canvas.addtag_withtag(addtag,oid)
            self.naki_list.pop(naki_index)

    def run(self):
        self.create_dialog()

    def file_save(self):
        with open('save_haipai.txt','wb') as f:
            str_data = pickle.dump(self.haipai_list,f)

    def file_open(self):
        with open('save_haipai.txt','rb') as f:
            self.haipai_list = pickle.load(f)

        self.haipai = [None for _ in range(14)]
        self.naki_list.clear()

        self.memnumber = 0
        self.list_back()

    def list_save(self):
        set_dict ={
            'haipai':copy.deepcopy(self.haipai),
            'naki':copy.deepcopy(self.naki_list),
        }

        if self.memnumber < len(self.haipai_list):
            self.haipai_list[self.memnumber] = set_dict
        else:
            self.haipai_list.append(set_dict)

        self.strMemnumber()

    def list_delete(self):
        if self.memnumber < len(self.haipai_list):
            self.haipai_list.pop(self.memnumber)
            self.memnumber = 0

            self.haipai = [None for _ in range(14)]
            self.naki_list.clear()
            self.list_back()

        self.strMemnumber()

    def list_back(self):
        if self.memnumber > 0:
            self.memnumber -= 1

        self.pick_up_list()

        return

    def list_forword(self):
        if self.memnumber < len(self.haipai_list):
            self.memnumber += 1

        self.haipai = [None for _ in range(14)]
        self.naki_list.clear()

        self.pick_up_list()

        return

    def pick_up_list(self):
        W, H = 0, 1

        self.clear_canvas()

        if self.memnumber < len(self.haipai_list):
            haipai = self.haipai_list[self.memnumber]
            self.haipai = copy.deepcopy(haipai['haipai'])
            self.naki = copy.deepcopy(haipai['naki'])

            canvas = self.haipai_canvas

            for i, hai in enumerate(self.haipai):
                if hai is not None:
                    self._draw_haipai_(pai_index=hai,pos_index=i)
                    img = self.PAI_IMG[hai]

        self.strMemnumber()

    def clear_canvas(self):
        self.select_choice = None
        self.select_haipai = None

        canvas = self.choice_canvas
        canvas.delete(self.mk_tag)

        canvas = self.haipai_canvas
        canvas.delete(self.mk_tag)
        oid_list = canvas.find_all()
        for oid in oid_list:
            tag_list = canvas.gettags(oid)
            for tag in  tag_list:
                if self.sel_tag in tag:
                    canvas.delete(tag)

        canvas = self.naki_canvas
        canvas.delete(self.mk_tag)
        oid_list = canvas.find_all()
        for oid in oid_list:
            tag_list = canvas.gettags(oid)
            for tag in  tag_list:
                if self.naki_tag in tag:
                    canvas.delete(tag)

        return

    def _draw_naki_(self,naki_index=None):
        W, H = 0, 1

        dx = 0

        for index, set_dict in enumerate(self.naki_list):
            key = list(set_dict.keys())[0]

            isDraw = True

            if naki_index is not None:
                if naki_index != index:
                    isDraw = False

            if isDraw:
                offset_x = self.offset + dx

                if 'index' in set_dict[key]:
                    d_index = set_dict[key]['index']
                if 'pai' in set_dict[key]:
                    pai_list = set_dict[key]['pai']

                for i in range(len(pai_list)):
                    _index_ = pai_list[i]
                    if i == d_index:
                        img = self.PAI_ROTATE_IMG[_index_]
                        x = offset_x
                        offset_x += PaiIMG.PAI_SIZE[H]+self.blank*2
                        y = self.offset+PaiIMG.PAI_SIZE[H]-PaiIMG.PAI_SIZE[W]
                    else:
                        if key == 'akan' and i%3 == 0:
                            img = self.PAI_IMG_URA
                        else:
                            img = self.PAI_IMG[_index_]
                        x = offset_x
                        offset_x += PaiIMG.PAI_SIZE[W]+self.blank*2
                        y = self.offset

                    self.naki_canvas.create_image(
                        x,y,
                        image=img, anchor=tk.NW, tags=f'{self.naki_tag}{index}')

            if key in ['pon','chey']:
                dx += (PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*2+self.blank*8)
            if key in ['mkan',]:
                dx += (PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*3+self.blank*10)
            if key in ['akan',]:
                dx += (PaiIMG.PAI_SIZE[W]*4+self.blank*10)

        return

    def cmd_pon(self):
        if self.select_choice is not None:
            if self.tag_head in self.select_choice:
                pai_list = self._merge_pai_()

                index = self.select_choice.strip(self.tag_head)
                index = int(index)

                if index>100:
                    return

                if len(self.naki_list) < 4 and pai_list.count(index) <= 1:
                    set_dict ={
                        'pon':{
                            'index':0,
                            'pai':[index,index,index],
                        }
                    }

                    self.naki_list.append(copy.deepcopy(set_dict))
                    naki_index = len(self.naki_list)-1

                    self._draw_naki_(naki_index=naki_index)

        return

    def cmd_chey(self):
        if self.select_choice is not None:
            if self.tag_head in self.select_choice:
                index = self.select_choice.strip(self.tag_head)
                index = int(index)

                if index > 100:
                    return

                if int(index/10)%10 > 3: #字牌はチーできない。indexが40,50代
                    return

                chey_list = list()

                num = index%10 #下一桁で判断
                for i in range(num-2,num+1):
                    if i > 0 and i+2 < 10:
                        digit = int((index/10)%10)*10
                        set_list = [digit+i,digit+i+1,digit+i+2]
                        if index in set_list:
                            j = set_list.index(index)
                            if j != 0:
                                set_list[0],set_list[j] = set_list[j],set_list[0]
                        chey_list.append(
                            copy.deepcopy(set_list)
                        )

                if len(chey_list) > 1:
                    image_set = list()
                    for pt in chey_list:
                        pt_set = list()
                        for i, iid in enumerate(pt):
                            if i == 0:
                                pt_set.append(self.PAI_ROTATE_IMG[iid])
                            else:
                                pt_set.append(self.PAI_IMG[iid])
                        image_set.append(pt_set)

                    inst = PopCheySelect(
                        parent=self.view_dialog,
                        image_set = image_set,
                        )
                    select = inst.select()

                if len(chey_list) == 1:
                    select = 0

                isChey = False

                if select is not None:
                    chey = chey_list[select]
                    pai_list = self._merge_pai_()
                    for pai in chey:
                        if len(self.naki_list) < 4:
                            if pai%10 == 5 and pai_list.count(pai) < 3:
                                isChey = True
                            elif pai_list.count(pai) < 4:
                                isChey = True
                if isChey:
                    set_dict ={
                        'chey':{
                            'index':0,
                            'pai':chey,
                        }
                    }

                    self.naki_list.append(copy.deepcopy(set_dict))
                    naki_index = len(self.naki_list)-1

                    self._draw_naki_(naki_index=naki_index)

        return

    def cmd_mkan(self):
        if self.select_choice is not None:
            if self.tag_head in self.select_choice:
                index = self.select_choice.strip(self.tag_head)
                index = int(index)

                pai_list = self._merge_pai_()

                if len(self.naki_list) < 4 and pai_list.count(index) == 0:
                    index_list = [index,index,index,index]
                    if index%10 == 5:
                        index_list = [index,index,index+100,index]

                    set_dict ={
                        'mkan':{
                            'index':0,
                            'pai':index_list,
                        }
                    }

                    self.naki_list.append(copy.deepcopy(set_dict))
                    naki_index = len(self.naki_list)-1

                    self._draw_naki_(naki_index=naki_index)

        return

    def cmd_akan(self):
        if self.select_choice is not None:
            if self.tag_head in self.select_choice:
                index = self.select_choice.strip(self.tag_head)
                index = int(index)

                pai_list = self._merge_pai_()

                if len(self.naki_list) < 4 and pai_list.count(index) == 0:
                    index_list = [index,index,index,index]
                    if index%10 == 5:
                        index_list = [index,index,index+100,index]

                    set_dict ={
                        'akan':{
                            'index':None,
                            'pai':index_list,
                        }
                    }


                    self.naki_list.append(copy.deepcopy(set_dict))
                    naki_index = len(self.naki_list)-1

                    self._draw_naki_(naki_index=naki_index)

        return

    def cmd_tsumo(self):
        print(self.haipai_list)
        pass

    def cmd_ron(self):
        print(self.haipai,self.naki_list)
        pass

class PopCheySelect():
    def __init__(self,parent,image_set):
        W, H = 0, 1
        self.offset = 20
        self.blank = 2

        self.select_set = None

        number = len(image_set)

        # 牌選択エリアの大きさ
        c_width = PaiIMG.PAI_SIZE[W]*3+self.blank*(5)+self.offset*2
        c_height = PaiIMG.PAI_SIZE[H]*(number)+self.blank*(number)+self.offset*2

        self.dialog = tk.Toplevel(parent)
        self.dialog.title('牌選択')
        self.dialog.geometry(f"{c_width}x{c_height+30}+600+450")
        self.dialog.grab_set()
        self.dialog.resizable(0,0)
        self.dialog.overrideredirect(True)

        InFrame1 = tk.Frame(self.dialog)
        InFrame2 = tk.Frame(self.dialog)

        btn_OK = tk.Button(InFrame2, width=8,text='OK',command=self.OK)
        btn_Cancel = tk.Button(InFrame2, width=8,text='Cancel',command=self.Cancel)

        btn_OK.pack(side=tk.LEFT,anchor=tk.W,padx=4)
        btn_Cancel.pack(side=tk.LEFT,anchor=tk.W,padx=4)

        self.canvas = tk.Canvas(
            InFrame1,bg='green', width=c_width, height=c_height
        )

        self.canvas.pack()

        InFrame1.pack(anchor=tk.W)
        InFrame2.pack()


        for j, pt in enumerate(image_set):
            dx = 0
            for i, img in enumerate(pt):
                offset_x = self.offset + dx
                x = offset_x

                if i == 0:
                    dx += PaiIMG.PAI_SIZE[H]+self.blank
                    y = self.offset+PaiIMG.PAI_SIZE[H]*j +self.blank*2*j+ (PaiIMG.PAI_SIZE[H]-PaiIMG.PAI_SIZE[W])
                else:
                    dx += PaiIMG.PAI_SIZE[W]+self.blank
                    y = self.offset+PaiIMG.PAI_SIZE[H]*j +self.blank*2*j
                self.canvas.create_image(
                    x,y,
                    image=img, anchor=tk.NW, tags=f'Chey_{j}')

        self.mk_tag = 'MARK'
        self.canvas.bind('<Button-1>',self._click_)

        self.dialog.wait_window()

    def OK(self):
        self.dialog.destroy()
        return

    def Cancel(self):
        self.dialog.destroy()
        return

    def select(self):
        return self.select_set

    def _click_(self,event):
        W, H = 0, 1
        canvas = self.canvas
        canvas.delete(self.mk_tag)
        x, y = event.x, event.y
        id_list =canvas.find_overlapping(x,y,x,y)
        pai_index = None
        for oid in id_list:
            tag_list = canvas.gettags(oid)
            for tags in tag_list:
                if 'Chey_' in tags:
                    pai_index = tags
                    break
            if pai_index is not None:
                break

        if pai_index is not None:
            x0, y0, x1, y1 = None,None,None,None
            mk_list = canvas.find_withtag(pai_index)
            for oid in mk_list:
                coods = canvas.coords(oid)
                x,y = coods
                if x0 is None:
                    x0 = x
                else:
                    x0 = min(x0,x)
                if y0 is None:
                    y0 = y
                else:
                    y0 = min(y0,y)
                if x1 is None:
                    x1 = x
                else:
                    x1 = max(x1,x)
                if y1 is None:
                    y1 = y
                else:
                    y1 = max(y1,y)
            canvas.create_rectangle(x0,y0,x1+PaiIMG.PAI_SIZE[W],y0+PaiIMG.PAI_SIZE[H],
                fill='orange', stipple='gray50', tag=self.mk_tag)

            self.select_set = int(pai_index.strip('Chey_'))
        else:
            self.select_set = None


if __name__ == '__main__':
    Test_Haipai().run()

