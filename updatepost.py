import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import mammoth
from base2 import get_courses_html
import datetime
from base2 import get_courses_html, build_html, authorize_credentials, update_post
from flask import Flask, render_template, request
import csv

# app = Flask(__name__)
app = Flask(__name__)

@app.route('/')
def index():
    # return 'Welcome to the Flask app!'
    return render_template('index.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # Get the submitted name from the form
        name = request.form['name']

        with open('form_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name])

        # Specify the post ID, blog ID, title, and content to update
        post_id = '8097252119400957177'
        blog_id = '5651255862571344247'
        test_post_id = '3359690114760599976'
        test_blog_id = '3481597162520342949'

        # Build HTML content from files
        html1 = build_html('first.html')
        html4 = "Updated Time (IST): " + datetime.datetime.now().strftime("%d/%m/%Y, %H:%M") + "\n"
        html2 = get_courses_html()
        html3 = build_html('file2.docx')
        all_html = html1 + html4 + html2 + html3

        # Get the current date
        from datetime import date
        today = date.today().strftime("%d-JUNE-%y")
        title = f"UDEMY COURSES WITH FREE CERTIFICATE | {today} | {name}"

        content = all_html
        # update_post(post_id, blog_id, title, content)
        update_post(test_post_id, test_blog_id, title, content)

        return render_template('success.html')
    else:
        return render_template('failure.html')



if __name__ == '__main__':
    app.run(debug=True)
