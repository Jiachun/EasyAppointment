# -*- coding: utf-8 -*-
"""
# 文件名称: utils/file_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-28
# 版本: 1.0
# 描述: 实现了数据的导入导出功能。
"""


import os
import pandas as pd


def import_excel(file_path, sheet_name=0):
	"""
	从 Excel 文件导入数据。
	
	:param file_path: Excel 文件路径
	:param sheet_name: 要导入的工作表名称或索引，默认为第一个
	:return: DataFrame
	"""
	return pd.read_excel(file_path, sheet_name=sheet_name)


def export_excel(dataframe, file_path, sheet_name='Sheet1'):
	"""
	将 DataFrame 导出到 Excel 文件。
	
	:param dataframe: 要导出的 DataFrame
	:param file_path: 导出文件路径
	:param sheet_name: 要保存的工作表名称，默认为 'Sheet1'
	:return row_count_len: 记录行数
	"""
	with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
		dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

		# 获取 xlsxwriter 对象
		workbook = writer.book
		worksheet = writer.sheets[sheet_name]

		# 定义表头格式
		format_header = workbook.add_format({
			'bold': True,  # 加粗
			'align': 'center',  # 水平局中
			'valign': 'vcenter',  # 垂直居中
			'font_name': 'Microsoft YaHei',  # 微软雅黑
			'font_size': 12,  #  12磅字体
			'font_color': '#ffffff',  # 白色字体
			'bg_color': '#548ff5',  # 浅蓝色背景
			'border': 1,  # 1磅边框
			'border_color': '#d8d8d8'  # 灰色边框
		})

		# 定义内容格式
		format_content = workbook.add_format({
			'align': 'center',  # 水平局中
			'valign': 'vcenter',  # 垂直居中
			'font_name': '_GB2312 FangSong_GB2312',  # 微软雅黑
			'font_size': 12,  #  12磅字体
			'font_color': '#000000',  # 黑色字体
			'bg_color': '#ffffff',  # 白色背景
			'border': 1,  # 1磅边框
			'border_color': '#d8d8d8'  # 灰色边框
		})

		# 应用表头格式
		for col_num, value in enumerate(df.columns.values):
			worksheet.write(0, col_num, value, format_header)  # 手动写入表头并应用格式

		# 应用内容格式
		for row in range(1, len(df) + 1):  # 跳过表头行，从数据行开始
			worksheet.set_row(row, 22, format_content)  # 设置行高为 20，并应用内容格式

		worksheet.set_row(0, 26)  # 设置表头行高为 26

		# 计算每列的最大字符长度并设置列宽
		for idx, col in enumerate(df.columns):
			# 获取当前列的所有值以及表头的字符长度
			column_len = max(
				df[col].astype(str).map(len).max(),  # 数据部分的最大字符长度
				len(col)  # 表头的字符长度
			) + 2  # 增加一些额外的空间以防止过紧

		# 设置列宽和字符格式
		worksheet.set_column(idx, idx, column_len)

	# 记录行数
	row_count_len = len(dataframe)

	return row_count_len

