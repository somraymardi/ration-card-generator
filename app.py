from flask import Flask, render_template, request, make_response
import pdfkit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_pdf():
    data = request.form.to_dict()
    members = []
    for i in range(5):
        name = data.get(f'member_name{i}')
        if name:
            members.append({
                'name': name,
                'age': data.get(f'member_age{i}'),
                'gender': data.get(f'member_gender{i}'),
                'relation': data.get(f'member_relation{i}')
            })

    rendered = render_template("ration_template.html", data=data, members=members)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=ration_card.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
