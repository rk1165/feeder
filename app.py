from flask import Flask, request, render_template
from rss import ExtractionParameters, create_feed
import xml.etree.cElementTree as ET

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    title = request.form["title"]
    url = request.form["url"]
    description = request.form["description"]

    params = ExtractionParameters()
    item_filter = (request.form.get("item_el"), request.form.get("item_cl"))
    title_filter = (request.form.get("title_el"), request.form.get("title_cl"))
    link_filter = (request.form.get("link_el"), request.form.get("link_cl"))
    description_filter = (request.form.get("desc_el"), request.form.get("desc_cl"))

    print(title, url, description)
    print(item_filter)
    print(title_filter)
    print(link_filter)
    print(description_filter)

    params.item_filter = item_filter
    params.title_filter = title_filter
    params.link_filter = link_filter
    params.description_filter = description_filter

    rss = create_feed(title, url, description, params)
    tree = ET.ElementTree(rss)
    tree.write(f"./static/{title}.xml", encoding="utf-8", xml_declaration=True)

    return render_template('index.html')


app.run(port=9999, debug=True)
