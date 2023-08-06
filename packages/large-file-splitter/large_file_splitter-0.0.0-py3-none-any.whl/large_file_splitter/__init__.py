
# 巨大ファイルの分割 [large_file_splitter]

import os
import sys
from sout import sout

# split_strを前後につなげる処理
def gen_ex_small_block(small_block, bin_split_str, div_file_idx, div_mode):
	if div_mode == "start":
		if div_file_idx == 0: return small_block
		ex_small_block = bin_split_str + small_block
		return ex_small_block
	elif:
		raise Exception("[error] invalid mode.")

# 巨大ファイルの分割
def split(
	target_filename,	# 分割対象ファイル
	split_str,	# 分割文字列 (分割の都合上内部ではbinaryとして処理するので、ここを一文字等にするのは、マルチバイト文字等の誤分割に繋がる可能性があるため非推奨)
	div_mode = "start",	# 分割文字列の扱いのモード (delete: 分割文字列は出力に含まない; start: 分割文字列は次の塊の先頭に結合される; end: 分割文字列は前の塊の末尾に結合される)
	output_filename_frame = "./split_result_%d.txt",	# 出力先ファイル名のテンプレート (%dのところは自動で整数値が挿入される)
	cache_size = 10 * 1024 ** 2	# メモリで作業するデータ塊の大きさの指定 (バイト単位)
):
	# バイナリ版のsplit_str
	bin_split_str = split_str.encode("utf-8")
	# ファイルサイズの取得 (バイト単位)
	org_size = os.path.getsize(target_filename)
	# 分割ファイル保存関数
	def save_div_file(small_block, div_file_idx):
		with open(output_filename_frame%div_file_idx, "wb") as f:
			f.write(small_block)
	# 分割して繰り返し
	div_file_idx = 0
	idx = 0
	residual = b""
	while True:
		# 脱出条件
		if cache_size * idx >= org_size: break
		# ファイルの分割パート読み込み
		with open(target_filename, "rb") as f:
			f.seek(cache_size * idx)
			bin_block = f.read(cache_size)
		# 前ブロックの余りを先頭につける
		bin_block = residual + bin_block
		# 分割保存
		split_ls = bin_block.split(bin_split_str)	# 分割
		for small_block in split_ls[:-1]:
			ex_small_block = gen_ex_small_block(small_block, bin_split_str, div_file_idx, div_mode)	# split_strを前後につなげる処理
			save_div_file(ex_small_block, div_file_idx)	# 分割ファイル保存関数
			div_file_idx += 1
		# 余りの文字列の更新
		residual = split_ls[-1]
		# インクリメント
		idx += 1
	# 分割ファイル保存関数
	save_div_file(residual, div_file_idx)
