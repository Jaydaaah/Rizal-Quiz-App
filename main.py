from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import time, random, string

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

#control variables
cur_item = 0
accept_answer = False
quiz_key = "A"
scores = {} # dict() // resp['stdname'] = int
   
def wait():
    return render_template('wait.html')

@app.route('/check_for_update')
def check_for_update():
    if accept_answer and session['last_item'] != cur_item:
        return jsonify({'redirect': True, 'redirect_url': '/'})
    else:
        return jsonify({'redirect': False})

@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        for i in range(1, 3):
            stdname = request.form[f'stdname{i}']
            session[f'stdname{i}'] = stdname
            session['last_item'] = cur_item
            scores[stdname] = 0
        return redirect('/')
    else:
        if 'stdname1' in session or 'stdname2' in session:
            return redirect('/')
        return render_template('reg.html')

@app.route('/logout')
def logout():
    for i in range(1, 3):
        session.pop(f'stdname{i}', None)
    return redirect('/')
        

@app.route('/', methods=['GET', 'POST'])
def quizmain():
    if not 'stdname1' in session and not 'stdname2' in session:
        return redirect('/reg')
    if not accept_answer or session['last_item'] == cur_item:
        return wait()
    if request.method == 'POST' and 'choices_btn' in request.form:
        choice = request.form["choices_btn"]
        for i in range(1, 3):
            stdname = session[f'stdname{i}']
            if stdname != '':
                if choice.upper() == quiz_key:
                    scores[stdname] += 1
                session['last_item'] = cur_item
                print(f'user: {stdname} answered')
        return wait()
    return render_template('choices.html', num=cur_item)
    
@app.route('/admin071802', methods=['GET', 'POST'])
def admin():
    global accept_answer, cur_item, quiz_key
    if request.method == 'POST':
        accept_answer = "accept_answer" in request.form
        cur_item = request.form["cur_item"]
        quiz_key = request.form["ans_key"]
    return render_template("admin.html", is_checked=accept_answer, cur_num=cur_item, ans_key=quiz_key, adminlink="admin071802", data_dict=scores)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    