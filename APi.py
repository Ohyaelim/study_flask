from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def findinfo(cname):
    totalresult = []
    country = cname
    url = "https://www.worldometers.info/coronavirus/country/{countryname}/".format(countryname = country)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        result = soup.find_all('div',class_="maincounter-number")
        for i in result:
            totalresult.append(i.find("span").text)
    else:
        totalresult.append("No Result")
    return totalresult


@app.route("/info/", methods = ["GET"])
def findinformation():
    country = request.args.get("country")
    try:
        return jsonify({"Total Cases":findinfo(country)[0], "Total Recovered:":findinfo(country)[2], "Total Deaths:":findinfo(country)[1]})
    except:
        return jsonify({"No country found": ""})


if __name__ == "__main__" :
    app.run()