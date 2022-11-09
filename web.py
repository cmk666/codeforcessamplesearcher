from flask import Flask, request, jsonify
import os, difflib
from os.path import join as pjoin
app = Flask('CodeforcesSampleSearcher')
f = open('index.html')
html = f.read()
f.close()
def simi(x, y):
	return int(100 * difflib.SequenceMatcher(None, x, y).ratio())
@app.get('/')
def index():
	return html
@app.get('/search')
def search():
	ret = []
	ct = request.args.get('content').strip()
	if len(ct) > 300:
		return jsonify([])
	suf = 'out' if request.args.get('type') == '1' else 'in'
	for fn in os.listdir('problem'):
		if fn.split('.')[-1] == suf:
			with open(pjoin('problem', fn), encoding='utf-8') as f:
				v = simi(ct, f.read())
				if v >= 80:
					qwq = fn.split('_')
					ret.append({
						"CID": qwq[0],
						"PID": qwq[1],
						"SID": qwq[2].split('.')[0],
						"SIM": v
					})
	ret.sort(key=lambda x : -x['SIM'])
	return jsonify(ret)
app.run('127.0.0.1', 23333)