from flask import  Flask,render_template,request,jsonify
from selenium import webdriver
from selenium .webdriver.common.by import By
import pandas as pd

import mysql.connector
import requests

app=Flask(__name__)

conn=mysql.connector.connect(host="localhost",user="root",password="",database="pythondb")
print(conn)


@app.route('/',methods=["POST","GET"])
def home():
    return render_template("emp.html")

@app.route('/data',methods=["POST","GET"])
def index():
    search= request.form["productName"]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.amazon.com")

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.clear()
    search_box.send_keys(search)

    driver.find_element(By.ID, "nav-search-submit-button").click()

    names = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    title = []
    for name in names:
        title.append(name.text)


    price = driver.find_elements(By.CLASS_NAME, "a-price-whole")
    prices = []
    for p in price:
        if p==' ':
            prices.append(' ')
        prices.append(p.text)

    print(title)
    print(prices)

    data={
        "Names of products":title,
        "price of products":prices
    }

    # df = pd.DataFrame(data)
    # # table = df.to_html(index=False)
    products = [{"name": name, "price": price} for name, price in zip(title, prices)]
    #
    return render_template('product.html', products=products)


    #return jsonify(data)



if __name__=="__main__":
    app.run(debug=True)