from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import filebase

app = Flask(__name__)


@app.route("/")
def hello():
    #home page
    index = filebase.get_full_index()
    return render_template('home.html',data=index)

@app.route("/about")
def about():
    #about page
    return render_template('about.html')

@app.route("/manual")
def manual():
    #manual page
    return render_template('manual.html')


@app.route("/add")
def display_add_page():
    #displays page to add data
    return render_template('add.html')

@app.route("/submit",methods=['POST'])
def submit():
    #receives submitted data when new entry is added
    index = filebase.store_data_add(request.form)
    return redirect('/index/'+str(index))

@app.route("/edit/<index>")
def edit_page(index):
    #display edit page
    data = filebase.get_data(index)
    return render_template('edit.html',data=data)

@app.route("/update",methods=['POST'])
def update():
    #receives data when entry is edited
    filebase.store_data_update(request.form)
    return redirect('/index/'+str(request.form['index']))

@app.route("/index/<index>")
def display(index):
    #displays entry
    data = filebase.get_data(index)
    if data=="404":
        return "Not found"
    else:
        return render_template('display.html',data = data)

@app.route("/codonopt/<index>")
def codon(index):
    #opens codon optimizer for host index
    return render_template('codon.html',index=index)



'''
@app.route("/admin")
@app.route("/admin/pending")
@app.route("/admin/edit")
@app.route("/admin/submit")
'''

if __name__ == '__main__':
    app.run(debug=True)
