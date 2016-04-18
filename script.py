import tornado.httpserver
import tornado.ioloop
import tornado.web
import sqlite3
import sys

_db = sqlite3.connect('database.db')
_cursor = _db.cursor()
class dbReset(tornado.web.RequestHandler):
	def delete(self):
		_cursor.execute("DROP TABLE IF EXISTS item")
		_cursor.execute("CREATE TABLE item (item VARCHAR, price FLOAT, quantity INT)")
		_db.commit()
		self.write('OK')
class grapeRequestHandler(tornado.web.RequestHandler):
	def put(self):
		record = ("grape", float(self.get_argument("price", default = "0")), int(self.get_argument("quantity", default = "0")))
		_cursor.execute("INSERT INTO item VALUES (?,?,?)", record)
		_db.commit()
		self.write('OK')
	def get(self, ID):
		range = self.get_argument("range", default ="0, "+str(sys.maxint)).split(',')
		params = [ID]+range
		_cursor.execute("SELECT * FROM item WHERE ID=? AND time>=? AND time<=?", params)
		records = []
		for row in _cursor:
			records = records + [{'ID':row[0],'value':row[1],'time':row[2]}]
		self.write(tornado.escape.json_encode(records))

class cheeseRequestHandler(tornado.web.RequestHandler):
	def put(self):
		record = ("cheese", float(self.get_argument("price", default = "0")), int(self.get_argument("quantity", default = "0")))
		_cursor.execute("INSERT INTO item VALUES (?,?,?)", record)
		_db.commit()
		self.write('OK')
	def get(self, ID):
		range = self.get_argument("range", default ="0, "+str(sys.maxint)).split(',')
		params = [ID]+range
		_cursor.execute("SELECT * FROM item WHERE ID=? AND time>=? AND time<=?", params)
		records = []
		for row in _cursor:
			records = records + [{'ID':row[0],'value':row[1],'time':row[2]}]
		self.write(tornado.escape.json_encode(records))



application = tornado.web.Application([(r"/database", dbReset),(r"/item/grape", grapeRequestHandler),(r"/item/cheese", cheeseRequestHandler)])

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(43594)
	tornado.ioloop.IOLoop.instance().start()
