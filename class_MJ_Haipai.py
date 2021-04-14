import copy
import pickle
import collections

FILE_NAME = 'save_haipai.pckl'

def toitsu_anko_ankan(haipai_Set):
    toustu = set()
    anko = set()
    ankan = set()
    if 'haipai' in haipai_Set:
        haipai = haipai_Set['haipai']
        c = collections.Counter(haipai)
        for k, v in c.items():
            if v == 2:
                toustu.add(k)
            if v == 3:
                anko.add(k)
            if v == 4:
                ankan.add(k)

    return toustu,anko,ankan

def syuntsu(haipai_Set):
    if 'haipai' in haipai_Set:
        haipai = haipai_Set['haipai']
        man = list()
        pin = list()
        sou = list()
        for pai in haipai:
            syubetu = int((pai%100)/10)
            if syubetu == 1:
                man.append(pai)
            if syubetu == 2:
                pin.append(pai)
            if syubetu == 3:
                sou.append(pai)

        def pai_cut(l):
            return [ p%10 for p in l]
        k, s = list(), list()

        for tp in [man,pin,sou]:
            num_list = pai_cut(tp)

            if num_list:
                for i, p in enumerate(num_list):
                    p1, p2 = p+1, p+2
                    pai1, pai2 = None, None
                    if p1 in num_list:
                        pai1 = tp[num_list.index(p1)]
                    if p2 in num_list:
                        pai2 = tp[num_list.index(p2)]

                    if pai1 and pai2:
                        pai = tp[i]
                        s.append([pai,pai1,pai2])
                    if pai1 and not pai2:
                        pai = tp[i]
                        k.append([pai,pai1])
                    if not pai1 and pai2:
                        pai = tp[i]
                        k.append([pai,pai2])
    return k, s

if __name__ == '__main__':
    with open(f'{FILE_NAME}','rb') as f:
        haipai_list = pickle.load(f)

    for haipai in haipai_list:
        print(haipai)
        toustu,anko,ankan = toitsu_anko_ankan(haipai)
        print(f'対子：{toustu},暗刻：{anko},暗槓：{ankan}')
        kouho,syun = syuntsu(haipai)
        print(f'順子：{syun},候補：{kouho}')


