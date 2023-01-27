import os, sys
from flask import render_template, Flask, request, redirect
import datetime
today = datetime.date.today()

app = Flask(__name__)
requests_num = 0

def add_to_file(Content, heading, User):
    from_replace = '    <!--New-->'

    html_to_replace = f'''
    <!--New-->

    <div class="para-box">
        <h2 class="para-heading">{heading} @ {today} By {User}</h2>
        <p>{Content}</p>
    </div>

'''

    file = open('templates/index.html', 'r')
    FileData = file.read()
    file.close()
    FileData = FileData.replace(from_replace, html_to_replace)                  #  replace(" ", "&nbsp;")
    file = open('templates/index.html', 'w')
    file.write(FileData)

@app.route('/')
def main_page():
    global requests_num
    if requests_num > 55:
        print(f"Backing up Request_num = {requests_num}")
        with open("templates/index.html", "r") as source_file:
            with open(f"backups/index.html.{today}.html", "w") as target_file:
                target_file.write(source_file.read())
        requests_num = 0

    requests_num = requests_num + 1
    return render_template('index.html')

@app.route('/submit', methods =['POST'])
def mainget():
    if request.method == 'POST' and 'title' in request.form and 'Content' in request.form and 'User' in request.form:
        title = request.form['title']
        User = request.form['User']
        Content = request.form['Content']
        
        Content_lines = Content.split("\n")

        content = []
        
        #Content = Content.replace("\n", "<br>")
        for line in Content_lines:
            if "IMAGE=" in line:
                try:
                    linet = line.split("'")
                    url = linet[1]
                    line = f'<img src="{url}">'
                    content.append(line)
                except:
                    content.append(line)
            else:
                content.append(line)

        Content = '<br>'.join(content)
        Content = Content.replace(" ", "&nbsp;")

        add_to_file(Content=Content, heading=title, User=User)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
