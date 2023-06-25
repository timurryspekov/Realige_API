from selenium import webdriver 
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import os
import re
from datetime import datetime
import base64

options = webdriver.FirefoxOptions()

options.headless = True
options.add_argument("--headless")

driver = webdriver.Firefox(executable_path = GeckoDriverManager().install(),options=options)

def norm(url = 'https://29a.ch/photo-forensics/#noise-analysis', image_name = 'test3.png'):
    try:
        driver.quit()
    except:
        pass
    driver = webdriver.Firefox(executable_path = GeckoDriverManager().install(),options=options)
    driver.get(url)
    
    
    try:
        time.sleep(1.5)
        path_file = os.path.abspath(image_name)
        
        input_file =driver.find_element(By.NAME, "file")
        print(input_file)
        input_file.send_keys(path_file)
        time.sleep(1.5)
        png_url = driver.execute_script('return document.getElementsByClassName("full-analysis-canvas")[0].toDataURL("image/png");')
        str_base64 = re.search(r'base64,(.*)',png_url).group(1)
       
        str_decoded = base64.b64decode(str_base64)
 
        #Write out the image somewhere
        output_img_path = image_name        
        fp = open(output_img_path,'wb')
        fp.write(str_decoded)
        fp.close()
        
        
        driver.quit()
        return output_img_path
    
    except Exception as error:
        print(error)

import coremltools
from PIL import Image


model = coremltools.models.MLModel('Realige.mlmodel')

def classify_image(image_path):
    image_path = image_path
    image = Image.open(image_path)
    image = image.resize((299, 299))  
    image = image.convert('RGB')  


    input_data = {'image': image}


    output = model.predict(input_data)


    predicted_class = output['classLabel']
    probability = output['classLabelProbs'][predicted_class]


    print('Predicted class:', predicted_class)
    print('Probability:', probability)

    return predicted_class + ': '+ str(probability)
    
    
def analysis(image_path):
    path = norm(image_name = image_path)
    return classify_image(path)
    


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      d_path = secure_filename(f.filename)
      f.save(d_path)
      return analysis(d_path)
      

if __name__ == '__main__':
   app.run(debug = True, host = '0.0.0.0', port = '9090')