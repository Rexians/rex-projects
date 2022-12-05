import os

import qrcode
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_file, url_for
from pytube import YouTube
from werkzeug.utils import secure_filename

from helpers.downloader import ytdownload

load_dotenv()

token = os.environ.get("TOKEN")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")
oauth_uri = os.environ.get("OAUTH_URI")

app = Flask(__name__, static_folder="files")
app.config["SECRET_KEY"] = "IndominusRexian"


@app.route("/")
def home():
    return render_template("projects.html")


@app.route("/test/")
def test():
    return "Test Page"


@app.route("/qrcreate/", methods=["GET", "POST"])
def qrcreate():
    if request.method == "POST":
        text_qr = request.form.get("textqr")
        qr = qrcode.make(f"{text_qr}")
        qr.save("qr_code.png")
        filename = "qr_code.png"
        return send_file(filename, mimetype="image/gif")
    return render_template(
        "qrcreate.html",
    )


@app.route("/downloader/", methods=["GET", "POST"])
def downloader():
    if request.method == "POST":
        yt = ytdownload()
        link = YouTube(request.form.get("ytlink"))
        url = yt.download(link)
        return render_template(
            "video_watch.html",
            filetitle=link.title,
            filepath=url,
            thumbnail=link.thumbnail_url,
        )
    return render_template(
        "downloader.html",
    )


@app.route("/download/", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        url = request.form.get("filepath")
        return send_file(url, as_attachment=True)
    return redirect(url_for("downloader"))

    return render_template(
        "discord_redirect.html",
    )


@app.route("/uploader/", methods=["GET", "POST"])
def uploader():
    if request.method == "POST":
        f = request.files["file"]
        if f.filename != "":
            media_type = request.form.get("media-type")
            file_name = request.form.get("filename")
            if media_type:
                if media_type == "Select Media type":
                    return render_template("uploader.html", error="No Media Type specified")
                else:
                    media_types = {
                        "1": "JPG",
                        "2": "PNG",
                        "3": "JPEG",
                        "4": "GIF",
                        "5": "WEBM",
                        "6": "MP4",
                        "7": "MOV",
                        "8": "MKV",
                        "9": "MPEG",
                        "10": "WEBM",
                    }
                    media_type = media_types[media_type].lower()
                    if media_type in f.filename:
                        filename = f.filename.removesuffix(media_type)
                        if file_name is not None and file_name is not '':
                            filename_secure = (
                                "./files/"
                                + secure_filename(file_name)
                                + "."
                                + media_type
                            )
                            filename = file_name
                        else:
                            filename_secure = (
                                "./files/"
                                + secure_filename(filename)
                                + "."
                                + media_type
                            )
                        f.save(filename_secure)
                        base_url = request.base_url.replace("/uploader/", "")
                        return render_template(
                            "uploader.html",
                            done=True,
                            link=f"{base_url}/files/{secure_filename(filename)}.{media_type}",
                        )
                    else:
                        return render_template(
                            "uploader.html", error="Specified media type is Invalid"
                        )
        else:
            return render_template("uploader.html", empty="No file selected")

    return render_template("uploader.html")


if __name__ == "__main__":
    app.run(debug=True)
