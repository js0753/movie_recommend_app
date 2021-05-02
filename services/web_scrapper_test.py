from selenium import webdriver
import os
def get_image(data_name):
        #data_name.lower
        APP_PATH = os.getcwd()
        
        data_spaced=data_name
        data_name=data_name.replace(" ","")
        data_name=data_name.replace(":","")
        # print("No white space :",data_name)
        #print(os.getcwd())
        #print(os.path.realpath(__file__)[:-21])
        if(os.path.realpath(__file__)[:-21]!=os.getcwd()):
                os.chdir(os.path.realpath(__file__)[:-21])
        if(os.path.realpath(__file__)[:-21]==os.getcwd()):
                # print("hello ")
                os.chdir('../static/img/web_images')
        path=data_name
        if(os.path.isdir(path)==False):
                os.mkdir(path)
                os.chdir(path)
                options=webdriver.ChromeOptions()
                options.add_argument('headless')
                print("App path : "+APP_PATH)
                driver=webdriver.Chrome(APP_PATH+'/services/ChromeDriver/chromedriver',chrome_options=options)
                        
                try:
                        
                        url = "https://www.google.com/search?q={}&tbm=isch".format(data_spaced)

                        driver.get(url)

                        image_links=driver.find_elements_by_class_name('rg_i.Q4LuWd')
                        print(image_links[0])

                        data_src_links = [image_links[i].get_attribute('data-src') for i in range(5)]
                        src_links = [image_links[i].get_attribute('src') for i in range(5)]

                        import urllib.request
                        import numpy as np
                        from tqdm import tqdm

                        for i,element in enumerate(data_src_links):
                            if element == None:
                                data_src_links[i] = src_links[i]
                        
                        for i,link in enumerate(data_src_links):
                                name = data_name+f'{i}.jpeg'
                                urllib.request.urlretrieve(link, name)
                                break
                                
                except Exception as e:
                        print(e)
                finally:
                        print("Done")
                        driver.quit()
                        os.chdir('..')
        else:
                print("Image already exists at "+data_name+f'/{data_name}0.jpeg',"\n")
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        return data_name+f'/{data_name}0.jpeg'

if __name__=="__main__":
        movie_string=input("Enter your movie : ")
        get_image(movie_string)