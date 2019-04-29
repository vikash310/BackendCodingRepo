from flask import request, url_for, Flask, jsonify, render_template
import psycopg2
from config import config


app = Flask(__name__)
@app.route("/getBranchDetails", methods=['GET', 'POST'])
def query1():
	if request.method == 'POST':
		content = request.form['ifsc_code']
		conn = None
		ifsc_code = content
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		sql_query = '''select banks.id,banks.name,br.ifsc,br.branch, br.address, br.city,br.district,br.state from branches AS br join banks on banks.id = br.bank_id where ifsc = %s'''
		cur.execute(sql_query, (ifsc_code, ))
		data = cur.fetchall()

		cur.close()
		return jsonify(data)
	return render_template('query1.html')
	
	
@app.route("/getAllBranchOfCity", methods=['GET', 'POST'])
def query2():
	if request.method == 'POST':
		content = request.form
		bank_name = content["bank_name"]
		bank_city = content["bank_city"]
		conn = None
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		
		sql_query = '''select * from branches where bank_id in (select id from banks where banks.name = %s) and city = %s'''
		cur.execute(sql_query, (bank_name, bank_city, ))
		data = cur.fetchall()
		
		cur.close()
		return jsonify(data)
	return render_template('query2.html')
	
	
if __name__ == "__main__":
	app.run(debug=True,host="localhost",port=8080)
