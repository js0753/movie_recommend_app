from flask import Flask,render_template,request
from services import movie_recommender_completed as mr
import os
import datetime
app = Flask(__name__)

"""
#When two same app.route("/") first one counts  
@app.route("/")
def hello1():
   return render_template('aboutus.html')

"""
@app.route("/")
def hello():
   return render_template('index.html',mov_list=mr.getAllMovies())




@app.route("/movieIn",methods=['POST'])
def movieIn():
   #print("here")
   #name property in html used to extract data from the html form
   mname = request.form['moviename']
   sim_mov,img_list=mr.get_similar_movies(mname)     
   

   
   if(os.path.realpath(__file__)[:-8]!=os.getcwd()):
      os.chdir(os.path.realpath(__file__)[:-8])
   

   if(sim_mov==-1):
       return render_template('error.html')

   else:

      link = []
      temp = []
      releaseDate = []
      overview = []
      voteAverage = []
      genres = []
      runTime = []
      
      for i in range(5):
         temp = str(sim_mov[i]).replace(":","")
         temp = temp.replace("& ","")
         temp = temp.replace(" ","+")
         link.append("http://www.google.com/search?q="+temp)      
         relDate,overView,voteAvg,genre,rT=mr.get_movie_details(sim_mov[i])
         releaseDate.append(relDate[0:4])
         overview.append(overView[0:600]) 
         voteAverage.append(voteAvg) 
         genres.append(genre) 
         conversion = datetime.timedelta(seconds=rT*60)
         converted_time = str(conversion)
         converted_time = converted_time[:-3]
         converted_time = converted_time.replace(":","h ")

         runTime.append(converted_time)

      return render_template('movies.html',sim_mov=sim_mov,img_list=img_list,link=link,releaseDate=releaseDate,overview=overview,voteAverage=voteAverage,genres=genres,runTime=runTime)
    
@app.route("/aboutus")
def about():
   return render_template('aboutus.html')

@app.route("/contactus")
def contact():
   return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)