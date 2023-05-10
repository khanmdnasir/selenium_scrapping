from baseBot import BaseBot
from producer import publish
 
# main program
if __name__ == '__main__':
    try:
        keywords = ['laptop', 'smartphone', 'book', 'toys', 'clothes']
        for keyword in keywords:
            bot = BaseBot()
            bot.search(keyword)
            publish()

    except Exception as e:
        print(str(e))
    
    
    

