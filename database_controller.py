'''
en : All comments were translated using DeepL.
ja : すべてのコメントはDeepLを使用して翻訳されました。

'''

import datetime, os, asyncio
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

db_name = 'database.json'				# en:Filename of database		ja:データベースのファイル名
table_name = 'translations'
cwd = os.getcwd()						# en:Current Working Directory 	ja:現在の作業フォルダ
db_file = os.path.join(cwd,db_name)		# en:Database File				ja:データベース・ファイル

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'ISO8601')
db = TinyDB(db_name, encoding='utf-8', storage=serialization)
print("Connected to database.")

tb = db.table(table_name)

def get_datetime_now():
	return datetime.datetime.now()

async def save(message,translation,dlang):	# en:Save the translations   ja:翻訳を保存する
	query = Query()
	result = tb.get((query.message == message) & (query.translation == translation) & (query.dlang == dlang))
	if result:
		# en:Update Don't   ja:更新不要
		return
	else:
		now = get_datetime_now()
		record = {
			"message": message,
			"dlang": dlang,
			"translation": translation,
			"created_at": now,
			"reference_at": now,
		}
		tb.insert(record)

async def get(message,dlang):  # en:Get the translations    ja:翻訳を入手する
	query = Query()
	result = tb.get((query.message == message) & (query.dlang == dlang))
	if not result:
		return None
	now = get_datetime_now()
	tb.update({"reference_at": now}, doc_ids=[result.doc_id])
	return result["translation"]

def delete():
	# en:Rumors last for 75 days    ja:人の噂も七十五日
	seventy_five_days_ago = get_datetime_now() - datetime.timedelta(days=75)
	query = Query()
	old_records = tb.search(query.reference_at < seventy_five_days_ago)
	if not old_records:
		return
	old_record_ids = [record.doc_id for record in old_records]
	tb.remove(doc_ids=old_record_ids)

def close():
	pass
