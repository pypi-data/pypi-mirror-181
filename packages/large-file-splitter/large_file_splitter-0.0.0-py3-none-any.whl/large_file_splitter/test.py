
# 巨大ファイルの分割 [large_file_splitter]
# 【動作確認 / 使用例】

import os
import sys
from sout import sout
from ezpip import load_develop
# 巨大ファイルの分割 [large_file_splitter]
large_file_splitter = load_develop("large_file_splitter", "../", develop_flag = True)

# 巨大ファイルの分割 [large_file_splitter]
large_file_splitter.split(
	"dummy_large_file.txt",	# 分割対象ファイル
	split_str = "SPLIT_MARK\r\n",	# 分割文字列 (分割の都合上内部ではbinaryとして処理するので、ここを一文字等にするのは、マルチバイト文字等の誤分割に繋がる可能性があるため非推奨)
	div_mode = "start",	# 分割文字列の扱いのモード (delete: 分割文字列は出力に含まない; start: 分割文字列は次の塊の先頭に結合される; end: 分割文字列は前の塊の末尾に結合される)
	output_filename_frame = "./output/div_%d.txt",	# 出力先ファイル名のテンプレート (%dのところは自動で整数値が挿入される)
	cache_size = 1024	# メモリで作業するデータ塊の大きさの指定 (バイト単位; メモリ容量は少なくともこの数倍は必要)
)
