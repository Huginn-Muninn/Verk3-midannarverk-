from flask import Flask, render_template
import urllib.request, json
app = Flask(__name__)

with urllib.request.urlopen("http://apis.is/petrol") as url:
	data = json.loads(url.read().decode())

company = []
for x in data["results"]:
	if x["company"] not in company:
		company.append(x["company"])

nafn95 = ""
nafnD = ""
laegst95 = 100000
laegstD = 100000
for i in data["results"]:
	if i["bensin95"] < laegst95:
		laegst95 = i["bensin95"]
		nafn95 = i["company"] + " - " + i["name"]
	if i["diesel"] < laegstD:
		laegstD = i["diesel"]
		nafnD = i["company"] + " - " + i["name"]
laegst = [nafn95, laegst95, nafnD, laegstD]


@app.route('/')
def index():
	return render_template("index.html", company=company, laegst=laegst)

@app.route("/til/<ft>")
def fyrirtaeki(ft):
	return render_template("fyrirtaeki.html", data=data, ft=ft, laegst=laegst)

@app.route("/til/<ft>/<name>")
def stadur(ft,name):
	return render_template("stadur.html", data=data, ft=ft, name=name, laegst=laegst)

@app.errorhandler(404)
def error404(error):
	return "Error 404 síðan var ekki fundin vinsamlegast reyndu eitthvað annað", 404

if __name__ == "__main__":
	app.run(debug=True)