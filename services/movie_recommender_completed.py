import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from services import web_scrapper_test
###### helper functions. Use them when needed #######
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]

def get_release_date_from_index(index):
	return df[df.index == index]["release_date"].values[0]

def get_overview_from_index(index):
	return df[df.index == index]["overview"].values[0]

def get_vote_average_from_index(index):
	return df[df.index == index]["vote_average"].values[0]

def get_genre_from_index(index):
	return df[df.index == index]["genres"].values[0]

def get_runtime_from_index(index):
	return df[df.index == index]["runtime"].values[0]
##################################################

##Step 1: Read CSV File
df = pd.read_csv("services/movie_dataset.csv")
#print df.columns
##Step 2: Select Features

features = ['keywords','cast','genres','director']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print("Error:", row	)

df["combined_features"] = df.apply(combine_features,axis=1)

# print("Combined Features:", df["combined_features"].head())

##Step 4: Create count matrix from this new combined column
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix) 

def get_movie_details(movie_name):
        movie_index = get_index_from_title(movie_name)
        relDate = get_release_date_from_index(movie_index)
        overView = get_overview_from_index(movie_index)
        voteAvg = get_vote_average_from_index(movie_index)
        genre = get_genre_from_index(movie_index)
        rT = get_runtime_from_index(movie_index)
        return relDate, overView, voteAvg, genre, rT

## Step 6: Get index of this movie from its title
def get_similar_movies(movie_name):
        try:
                movie_index = get_index_from_title(movie_name)
        except:
                return [-1,-1]

        similar_movies =  list(enumerate(cosine_sim[movie_index]))

        ## Step 7: Get a list of similar movies in descending order of similarity score
        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

        ## Step 8: Print titles of first 5 movies
        i=0
        print("The Top 5 movies recommended for you are: ")
        movie_list=[]
        img_paths=[]
        for element in sorted_similar_movies:
                if i!=0:
                        print(str(i)+"]\t",get_title_from_index(element[0]))
                        img_paths.append('static/img/web_images/'+web_scrapper_test.get_image(get_title_from_index(element[0])).replace(":",""))
                        #img_paths.append(web_scrapper_test.get_image(get_title_from_index(element[0])))

                        movie_list.append(get_title_from_index(element[0]))
                i=i+1
                if i>5:
                        break
        return movie_list,img_paths


def getAllMovies():
        #print(df['title'].head())
        return list(df['title'])

if __name__=="__main__":
        print(getAllMovies()[0])
        movie_user_likes = input("Enter Movie Name: ")
        get_similar_movies(movie_user_likes)
