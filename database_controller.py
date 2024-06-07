'''
en : All comments were translated using DeepL.
ja : すべてのコメントはDeepLを使用して翻訳されました。

'''

import os, asyncio
from tinydb import TinyDB, Query

db_name = 'database.json'				# en:Filename of database		ja:データベースのファイル名
table_name = 'translations'
cwd = os.getcwd()						# en:Current Working Directory 	ja:現在の作業フォルダ
db_file = os.path.join(cwd,db_name)		# en:Database File				ja:データベース・ファイル

db = TinyDB(db_name, encoding='utf-8')
print("Connected to database.")

tb = db.table(table_name)

async def save(message,translation,dlang):	# en:Save the translations   ja:翻訳を保存する
	tb.insert({"message": message, "dlang": dlang, "translation": translation})

async def get(message,dlang):  # en:Get the translations    ja:翻訳を入手する
	query = Query()
	result = tb.get((query.message == message) & (query.dlang == dlang))
	if (not result):
		return None
	return result["translation"]

def delete():
	pass

def close():
	pass
