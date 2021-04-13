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
        self.list_index = 0
        self.naki_list = list()

        self.mk_tag = 'MARK'
        self.tag_head = 'PAI_'
        self.tag_frame_head = 'FRAME_'
        self.sel_tag = 'SEL_'
        self.naki_tag = 'NAKI_'

    def create_dialog(self):
        W, H = 0, 1
        self.offset = 10
        self.blank = 2
        c_width = PaiIMG.PAI_SIZE[W]*(PaiIMG.NUM_PAI+1)+self.blank*(PaiIMG.NUM_PAI)+self.offset*2
        c_height = PaiIMG.PAI_SIZE[H]*(PaiIMG.NUM_PATTERN)+self.blank*(PaiIMG.NUM_PATTERN-1)+self.offset*2
        h_width = PaiIMG.PAI_SIZE[W]*(13+1)+self.blank*2*(13-1+4)+self.offset*2
        h_height = PaiIMG.PAI_SIZE[H]*(1)+self.offset*2
        n_width = PaiIMG.PAI_SIZE[H]*(4*4)+self.blank*2*(4*4-1)+self.offset*2
        n_height = PaiIMG.PAI_SIZE[H]*(1)+self.offset*2

        self.view_dialog = tk.Tk()
        self.view_dialog.geometry(f'{max(c_width,h_width,n_width)}x{c_height+h_height+n_height+5*3}+300+300')
        self.view_dialog.title('麻雀配牌エディタ')

        self.menubar = tk.Menu(
            self.view_dialog,
        )
        self.file_menu = tk.Menu(
            self.menubar,
            tearoff=0
        )
        self.naki_menu = tk.Menu(
            self.view_dialog,
        )
        self.naki_menu_list = tk.Menu(
            self.naki_menu,
            tearoff=0
        )
        self.menubar.add_cascade(label='ファイル', menu=self.file_menu)
        self.file_menu.add_command(label='開く',command=self.file_open)
        self.file_menu.add_command(label='保存',command=self.file_save)
        self.menubar.add_command(label='削除',command=self.list_delete)
        self.menubar.add_command(label='<<',command=self.list_back)
        self.menubar.add_command(label='>>',command=self.list_forword)
        self.menubar.add_cascade(label='鳴き', menu=self.naki_menu_list)
        self.naki_menu_list.add_command(label='ポン',command=self.cmd_pon)
        self.naki_menu_list.add_command(label='チー',command=self.cmd_chey)
        self.naki_menu_list.add_command(label='明槓',command=self.cmd_mkan)
        self.naki_menu_list.add_command(label='暗槓',command=self.cmd_akan)
        #self.menubar.add_command(label='判定',command=self.list_forword)

        self.view_dialog.config(menu=self.menubar)

        InFrame1 = tk.Frame(self.view_dialog)
        InFrame2 = tk.Frame(self.view_dialog)
        InFrame3 = tk.Frame(self.view_dialog)

        self.choice_canvas = tk.Canvas(
                InFrame1, bg='green', width=max(c_width,h_width,n_width), height=c_height)
        self.choice_canvas.pack()

        self.choice_canvas.bind('<Button-1>',self._choice_click_)

        self.haipai_canvas = tk.Canvas(
                InFrame2, bg='darkgreen', width=max(c_width,h_width,n_width), height=h_height)
        self.haipai_canvas.pack()

        self.haipai_canvas.bind('<Button-1>',self._haipai_click_)
        self.haipai_canvas.bind('<Button-3>',self._haipai_right_click_)

        self.naki_canvas = tk.Canvas(
                InFrame3, bg='darkgreen', width=max(c_width,h_width,n_width), height=n_height)
        self.naki_canvas.pack()

        self.naki_canvas.bind('<Button-3>',self._naki_right_click_)

        InFrame1.pack()
        InFrame2.pack()
        InFrame3.pack()

        self._image_pai_()

        self._lineup_choice_()
        self._haipai_farame_()

        self.view_dialog.mainloop()

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
            img = self.PAI_IMG[index]

            x = self.offset+PaiIMG.PAI_SIZE[W]*hindex+(self.blank*2)*(hindex+int(hindex/(14-1))*2)
            y = self.offset

            canvas.delete(f'{self.sel_tag}{hindex}')
            canvas.create_image(
                x,y,image=img, anchor=tk.NW, tags=f'{self.sel_tag}{hindex}')

            canvas.tag_raise(self.mk_tag)

            self.haipai[hindex] = index

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
            print(pai_index)

    def run(self):
        self.create_dialog()

    def file_save(self):
        self.haipai_list.append(
            {
                'haipai':copy.deepcopy(self.haipai),
                'naki':copy.deepcopy(self.naki_list),
            }
        )

        with open('save_haipai.txt','wb') as f:
            str_data = pickle.dump(self.haipai_list,f)

    def file_open(self):
        with open('save_haipai.txt','rb') as f:
            self.haipai_list = pickle.load(f)

    def list_delete(self):
        del_index = None
        for index, hl in enumerate(self.haipai_list):
            haipai = hl['haipai']
            naki = hl['naki']
            if self.haipai == haipai and self.naki_list== naki:
                del_index = index
                break
        if del_index is not None:
            self.haipai_list.pop(del_index)

            self.list_index = 0
            self.list_back()

    def list_back(self):
        if self.list_index > 0:
            self.list_index -= 1

        self.pick_up_list()

        return

    def list_forword(self):
        if self.list_index < len(self.haipai_list)-1:
            self.list_index += 1

        self.pick_up_list()

        return

    def pick_up_list(self):
        if self.list_index < len(self.haipai_list):
            haipai = self.haipai_list[self.list_index]
            self.haipai = copy.deepcopy(haipai['haipai'])
            self.naki = copy.deepcopy(haipai['naki'])

        print(self.haipai_list)
        print(self.haipai)
        print(self.naki)

    def cmd_pon(self):
        W, H = 0, 1

        if self.select_choice is not None:
            if self.tag_head in self.select_choice:
                index = self.select_choice.strip(self.tag_head)
                index = int(index)

                if len(self.naki_list) < 4:
                    set_dict ={
                        'pon':{
                            'index':0,
                            'pai':[index,index,index],
                        }
                    }

                    dx = 0
                    for naki in self.naki_list:
                        key = list(naki.keys())[0]
                        if key in ['pon','chey']:
                            dx += PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*2+self.blank*8
                        if key in ['mkan',]:
                            dx += PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*3+self.blank*10
                        if key in ['akan',]:
                            dx += PaiIMG.PAI_SIZE[W]*4+self.blank*10

                    self.naki_list.append(copy.deepcopy(set_dict))

                    naki_index = len(self.naki_list)

                    offset_x = self.offset + dx

                    for i in range(3):
                        if i == set_dict['pon']['index']:
                            img = self.PAI_ROTATE_IMG[index]
                            x = offset_x
                            offset_x += PaiIMG.PAI_SIZE[H]+self.blank*2
                            y = self.offset+PaiIMG.PAI_SIZE[H]-PaiIMG.PAI_SIZE[W]
                        else:
                            img = self.PAI_IMG[index]
                            x = offset_x
                            offset_x += PaiIMG.PAI_SIZE[W]+self.blank*2
                            y = self.offset

                        self.naki_canvas.create_image(
                            x,y,
                            image=img, anchor=tk.NW, tags=f'{self.naki_tag}{naki_index}')

        pass

    def cmd_chey(self):
        pass

    def cmd_mkan(self):
        W, H = 0, 1

        if self.select_choice is not None:
            if self.tag_head in self.select_choice:
                index = self.select_choice.strip(self.tag_head)
                index = int(index)

                if len(self.naki_list) < 4:
                    set_dict ={
                        'mkan':{
                            'index':0,
                            'pai':[index,index,index,index],
                        }
                    }

                    dx = 0
                    for naki in self.naki_list:
                        key = list(naki.keys())[0]
                        if key in ['pon','chey']:
                            dx += PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*2+self.blank*8
                        if key in ['mkan',]:
                            dx += PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*3+self.blank*10
                        if key in ['akan',]:
                            dx += PaiIMG.PAI_SIZE[W]*4+self.blank*10

                    self.naki_list.append(copy.deepcopy(set_dict))

                    naki_index = len(self.naki_list)

                    offset_x = self.offset + dx

                    for i in range(4):
                        if i == set_dict['mkan']['index']:
                            img = self.PAI_ROTATE_IMG[index]
                            x = offset_x
                            offset_x += PaiIMG.PAI_SIZE[H]+self.blank*2
                            y = self.offset+PaiIMG.PAI_SIZE[H]-PaiIMG.PAI_SIZE[W]
                        else:
                            img = self.PAI_IMG[index]
                            x = offset_x
                            offset_x += PaiIMG.PAI_SIZE[W]+self.blank*2
                            y = self.offset

                        self.naki_canvas.create_image(
                            x,y,
                            image=img, anchor=tk.NW, tags=f'{self.naki_tag}{naki_index}')

    def cmd_akan(self):
        W, H = 0, 1

        if self.select_choice is not None:
            if self.tag_head in self.select_choice:
                index = self.select_choice.strip(self.tag_head)
                index = int(index)

                if len(self.naki_list) < 4:
                    set_dict ={
                        'akan':{
                            'index':None,
                            'pai':[index,index,index,index],
                        }
                    }

                    dx = 0
                    for naki in self.naki_list:
                        key = list(naki.keys())[0]
                        if key in ['pon','chey']:
                            dx += PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*2+self.blank*8
                        if key in ['mkan',]:
                            dx += PaiIMG.PAI_SIZE[H]+PaiIMG.PAI_SIZE[W]*3+self.blank*10
                        if key in ['akan',]:
                            dx += PaiIMG.PAI_SIZE[W]*4+self.blank*10

                    self.naki_list.append(copy.deepcopy(set_dict))

                    naki_index = len(self.naki_list)

                    offset_x = self.offset + dx

                    for i in range(4):
                        if i%3 == 0:
                            img = self.PAI_IMG_URA
                        else:
                            img = self.PAI_IMG[index]

                        x = offset_x
                        offset_x += PaiIMG.PAI_SIZE[W]+self.blank*2
                        y = self.offset

                        self.naki_canvas.create_image(
                            x,y,
                            image=img, anchor=tk.NW, tags=f'{self.naki_tag}{naki_index}')

if __name__ == '__main__':
    Test_Haipai().run()

