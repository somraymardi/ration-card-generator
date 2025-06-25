from flask import Flask, request, render_template, send_file
import pdfkit

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.form.to_dict()
    rendered = render_template("card_template.html", **data)
    pdfkit.from_string(rendered, "ration_card.pdf")
    return send_file("ration_card.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
