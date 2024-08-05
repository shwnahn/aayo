from starbucks import crawl_starbucks
from hasamdong import crawl_hasamdong
from ediya import crawl_ediya
from mega import crawl_mega
from compose import crawl_compose
from paik import crawl_paik
from mammoth_ex import crawl_mammoth_ex
from twosome import crawl_twosome
from gongcha import crawl_gongcha
# from theventi import crawl_theventi
from hollys import crawl_hollys
from toms import crawl_toms

def main():
    cafe_list = [
        "starbucks",
        "hasamdong",
        "ediya",
        "mega",
        "compose",
        "paik",
        "mammoth_ex",
        "twosome",
        "gongcha",
        "theventi",
        "hollys",
        "toms"
    ]

    for cafe_name in cafe_list:
        func_name = f'crawl_{cafe_name}'
        func = globals().get(func_name)
        if callable(func):
            func()

if __name__ == "__main__":
    main()