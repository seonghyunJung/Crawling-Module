from preprocess import *
import os

def main():
    file_list = os.listdir('네이버 플레이스 리뷰 원본')
    for file in file_list:
        file_name = file.split('.')[0]
        do_preprocess(file_name)


if __name__ == '__main__':
    main()
