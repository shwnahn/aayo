from bana import crawl_bana
from bean import crawl_bean
from compose import crawl_compose
from curban import crawl_curban
from ediya import crawl_ediya
from gongcha import crawl_gongcha
from hasamdong import crawl_hasamdong
from hollys import crawl_hollys
from mammoth_ex import crawl_mammoth_ex
from mega import crawl_mega
from paik import crawl_paik
from starbucks import crawl_starbucks
from theventi import crawl_theventi
from toms import crawl_toms
from twosome import crawl_twosome
from yoger import crawl_yoger



def main():
    cafe_list = [
        'bana',
        'bean',
        'compose',
        'curban',
        'ediya',
        'gongcha',
        'hasamdong',
        'hollys',
        'mammoth_ex',
        'mega',
        'paik',
        'starbucks',
        'theventi',
        'toms',
        'twosome',
        'yoger',
    ]

    for cafe_name in cafe_list:
        func_name = f'crawl_{cafe_name}'
        func = globals().get(func_name)
        if callable(func):
            print(f"## {cafe_name} 크롤링")
            try:
                func()
            except Exception as e:
                print(f"크롤링 실패: {cafe_name}, 오류: {e}")
            print(f"## {cafe_name} 크롤링 COMPLETE")

if __name__ == "__main__":
    main()