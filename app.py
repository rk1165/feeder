import os
import xml.etree.cElementTree as ET

from flask import Flask, request, render_template, url_for, redirect

from models import *
from rss import ExtractionParameters, create_feed, FormData

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///feeds.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/feed/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    form_data = get_form_data(request.form)

    rss = create_feed(form_data.channel_title, form_data.feed_url,
                      form_data.channel_desc, form_data.extraction_parameters)
    tree = ET.ElementTree(rss)
    tree.write(f"./static/{form_data.channel_title.lower()}.xml",
               encoding="utf-8", xml_declaration=True)
    ex_params = form_data.extraction_parameters
    new_feed = Feed(path=f"{form_data.channel_title.lower()}.xml", title=form_data.channel_title,
                    url=form_data.feed_url, description=form_data.channel_desc,
                    item_tag=ex_params.item_tag, item_cls=ex_params.item_cls,
                    title_tag=ex_params.title_tag, title_cls=ex_params.title_cls,
                    link_tag=ex_params.link_tag, link_cls=ex_params.link_cls,
                    description_tag=ex_params.description_tag, description_cls=ex_params.description_cls)

    db.session.add(new_feed)
    db.session.commit()
    return redirect(url_for('feeds'))


def get_form_data(form):
    channel_title = form.get("title")
    feed_url = form.get("url")
    channel_desc = form.get("description")

    (item_tag, item_cls) = (form.get("item_tag"), form.get("item_cls"))
    (title_tag, title_cls) = (form.get("title_tag"), form.get("title_cls"))
    (link_tag, link_cls) = (form.get("link_tag"), form.get("link_cls"))
    (description_tag, description_cls) = (form.get("desc_tag"), form.get("desc_cls"))

    form_data = FormData(channel_title, feed_url, channel_desc)
    # print("Form data", form_data)
    params = ExtractionParameters(item_tag, item_cls, title_tag, title_cls,
                                  link_tag, link_cls, description_tag, description_cls)
    # print("params", params)

    form_data.extraction_parameters = params
    return form_data


@app.route("/feeds", methods=["GET"])
def feeds():
    all_feeds = Feed.query.all()
    return render_template("feeds.html", feeds=all_feeds)


@app.route("/feed/<int:feed_id>", methods=["GET"])
def feed(feed_id):
    obj = Feed.query.filter_by(id=feed_id).first()
    return render_template("feed.html", feed=obj)


@app.route("/feed/<int:feed_id>/delete", methods=["GET"])
def delete(feed_id):
    obj = Feed.query.filter_by(id=feed_id).one()
    path = obj.path
    db.session.delete(obj)
    db.session.commit()
    os.remove(f"./static/{path}")
    return redirect(url_for("feeds"))


@app.route("/feed/<feed_id>/update", methods=["POST"])
def edit(feed_id):
    obj = Feed.query.filter_by(id=feed_id).one()
    return render_template("update.html", feed=obj)


@app.route("/feed/<int:feed_id>/save", methods=["POST"])
def save(feed_id):
    obj = Feed.query.filter_by(id=feed_id).first()
    form_data = get_form_data(request.form)
    obj.title = form_data.channel_title
    obj.url = form_data.feed_url
    obj.description = form_data.channel_desc
    ex_params = form_data.extraction_parameters
    obj.item_tag = ex_params.item_tag
    obj.item_cls = ex_params.item_cls
    obj.title_tag = ex_params.title_tag
    obj.title_cls = ex_params.title_cls
    obj.link_tag = ex_params.link_tag
    obj.link_cls = ex_params.link_cls
    obj.description_tag = ex_params.description_tag
    obj.description_cls = ex_params.description_cls
    print(obj)
    # db.session.add(obj)
    db.session.commit()
    return redirect(url_for("feed", feed_id= feed_id))


app.run(port=9999, debug=True)
