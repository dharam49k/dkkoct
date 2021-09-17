from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json,time
import logging
from telegram.ext import Updater


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

my_url = 'https://www.octafx.com/copy-trade/master/11457156/history/open/0/'

print("Url is : " + my_url)

uClient = uReq(my_url)
page_html= uClient.read()
uClient.close()

Token = "2047565924:AAEZaWLx7N7wmIzAxmtnKC_lvxjDJnfGkrc"
chatid = "-1001392493031"
delay = 10

temp_data= "octa_temp_data.json" 
main_data = "octa_main_data.json"
expand_data=[]
def new_repeator(context):

    my_url = 'https://www.octafx.com/copy-trade/master/18276567/history/open/0/'
    uClient = uReq(my_url)
    page_html= uClient.read()
    uClient.close()
      
    data_soup = soup(page_html,"html.parser")    
    data = data_soup.string.strip()[8:-(13-len(data_soup.text))]
    profile_data = json.loads(data)

    with open(temp_data,"w", encoding='UTF-8') as wf:
        json.dump(profile_data, wf)

    wf.close()
    a= []
    b= []
    with open(temp_data, 'r') as r:
        newsl = json.load(r)
        for i in newsl :

            new1_list = {
                'openTime' : i['openTime'],
                'date' :i['date'],
                'icon': i['icon'],
                'symbol' : i['symbol'],
                'volume' : i['volume']
            }

            a.append(new1_list)
    r.close()        

    #os.remove(temp_file)   

    with open(main_data, 'r') as rf:
        news = json.load(rf)
        for i in news :

            new2_list = {
                'openTime' : i['openTime'],
                'date' :i['date'],
                'icon': i['icon'],
                'symbol' : i['symbol'],
                'volume' : i['volume']
            }
            b.append(new2_list)
    rf.close()


    for i in range(len(a)):
        if a[i] not in b:
            context.bot.send_message(chatid,"New Entry: \n" +a[i]['symbol'] + " " +a[i]['icon'] +"\n" +"Lot size: " +str(a[i]['volume']))
            #print(a[i])
            b.append(a[i])
            time.sleep(5)
        else:
            continue

    z=[]
    with open(main_data,'r+') as gwf:
        z=json.load(gwf)
        for d in range(len(b)):
            new3_list = {
               'openTime' : b[d]['openTime'],
               'date' :b[d]['date'],
               'icon':b[d]['icon'],
               'symbol' :b[d]['symbol'],
                'volume' : b[d]['volume']
            }

        z.append(new3_list)
        gwf.seek(0)    

        json.dump(z,gwf)
        gwf.truncate()  
    gwf.close()       

updater = Updater(token=Token, use_context=True)
job_queue = updater.job_queue
dp = updater.dispatcher

job_queue.run_repeating(new_repeator, delay)

updater.start_polling()
updater.idle()