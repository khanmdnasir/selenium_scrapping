from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# database credentials
db_host = os.environ.get('DBHOST')
db_name = os.environ.get('DBNAME')
db_user = os.environ.get('DBUSER')
db_pass = os.environ.get('DBPASS')
db_port = os.environ.get('DBPORT')


# base bot class having product search method, store_product method, and update product method
class BaseBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass,port=db_port)
        self.cur = self.conn.cursor()
        table_name = 'products'

        self.cur.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname=%s)", (table_name,))
        table_exists = self.cur.fetchone()[0]

        if table_exists:
            print(f"The table {table_name} already exists.")
        else:
            create_table_command = """
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                price NUMERIC(10, 2) NOT NULL,
                rating NUMERIC(3, 1) NOT NULL,
                description TEXT,
                image_url TEXT
            );
            """

            # Execute the SQL command
            self.cur.execute(create_table_command)
            print(f"Create {table_name} table.")
            
    def search(self, keyword):
        self.driver.get("https://www.amazon.com")
        search_box = self.driver.find_element(By.CSS_SELECTOR, '[name="field-keywords"]')
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        products = self.driver.find_elements(By.XPATH,"//div[contains(@class, 's-result-item')]")
        for product in products:
            try:
                title = product.find_element(By.XPATH, './/h2/a/span').text
                price_text = product.find_element(By.CSS_SELECTOR, '.a-price-whole').text
                price_fraction = product.find_element(By.CSS_SELECTOR, '.a-price-fraction').text
                rating_text = product.find_element(By.XPATH, './/div[contains(@class, "a-row") and contains(@class, "a-size-small")]/span').get_attribute('aria-label')
                image_url = product.find_element(By.XPATH,".//img").get_attribute('src')
            except Exception as e:
                pass
            else:
                price = float(price_text.replace(',','')+'.'+price_fraction)
                rating = float(rating_text.split(' ')[0])
                print({
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'image_url': image_url
                })
                self.store_product(title, price , rating, image_url)
        self.driver.close()

    def store_product(self, title, price, rating, image_url):
        self.cur.execute("INSERT INTO products (title, price,rating, image_url) VALUES (%s, %s, %s, %s)", (title, price, rating, image_url))
        self.conn.commit()
    
    
# main program
if __name__ == '__main__':
    try:
        bot = BaseBot()
        keywords = ['laptop', 'smartphone', 'book', 'toys', 'clothes']
        for keyword in keywords:
            bot.search(keyword)
    except Exception as e:
        print(str(e))
    
    

