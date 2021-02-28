from flask import Flask,render_template,request
from services import movie_recommender_completed as mr
import os
app = Flask(__name__)


@app.route("/")
def hello():
   return render_template('index.html')


@app.route("/movieIn",methods=['POST'])
def movieIn():
    #print("here")
    #name property in html used to extract data from the html form
    mname = request.form['moviename']
    sim_mov,img_list=mr.get_similar_movies(mname)
    
    
    if(os.path.realpath(__file__)[:-8]!=os.getcwd()):
        os.chdir(os.path.realpath(__file__)[:-8])
    return render_template('movies.html',sim_mov=sim_mov,img_list=img_list)
    
@app.route("/aboutus")
def about():
   return render_template('aboutus.html')

@app.route("/contactus")
def contact():
   return render_template('contactus.html')