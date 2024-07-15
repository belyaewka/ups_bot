from signal import pause
import logging
from gpiozero import Button
import requests
from config import BOT_TOKEN, CHAT_ID

# GPIO item config
UPS_1 = Button(4, pull_up=True, bounce_time=5.0)
UPS_2 = Button(18, pull_up=True, bounce_time=5.0)
UPS_3 = Button(11, pull_up=True, bounce_time=5.0)
UPS_4 = Button(1, pull_up=True, bounce_time=5.0)

# UPS config
ibp1 = ['UPS_1', 'Kuhner Incubators 2-607', '(group 2.3.1-2)']
ibp2 = ['UPS_2', 'left 2L bioreactors \n B2_5,B2_6,B2_7,B2_8', '(group 2.3.1-5 QF9)']
ibp3 = ['UPS_3', 'right 5L bioreactor B5_1', '(group 2.2.1-8)']
ibp4 = ['UPS_4', 'right 2L bioreactors \n B2_1,B2_2,B2_3,B2_4', '(group 2.2.1-7)']

# messages config
IF_ONLINE = ['IS ONLINE \U00002705', 'IS ON THE BATTERY! \U0001F198 \U0001F198 \U0001F198']

# logging config
logging.basicConfig(filename='ups.log',
                    format='%(asctime)s '
                           'LOGGER=%(name)s '
                           'MODULE=%(module)s.py '
                           'FUNC=%(funcName)s '
                           ' %(levelname)s '
                           ' %(message)s ',
                    datefmt='%d-%m-%Y %H:%M:%S',  
                    level='INFO',
                    encoding='utf8')
 
# make the logger                   
logger = logging.getLogger('ups_bot')
                           
# url for telegram API bot send message, text message required to add here
URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text='


class UPS:
    def __init__(self, configuration, gpio_item):
        self.gpio_item = gpio_item  
        self.name = configuration[0]
        self.description = configuration[1]
        self.electrical_group = configuration[2]
        
    
    def ups_on_battery(self):
        logger.info(f'{self.name} is on the battery')
        self.send_message(IF_ONLINE[1])
            
    def ups_online(self):
        logger.info(f'{self.name} is online')
        self.send_message(IF_ONLINE[0])
    
    def __str__(self):
        return f"{self.gpio_item.pin}, {self.name}, {self.description},{self.electrical_group}"


    def send_message(self, if_online: str)->None:
        try:
            url_to_send = URL + f'{self.name} {if_online} \n {self.description} \n {self.electrical_group}'
            requests.get(url_to_send)
        except:
            logger.error('telegram API send message error')
    
# making a class UPS objects (ups units)
u1 = UPS(ibp1, UPS_1)
u2 = UPS(ibp2, UPS_2)
u3 = UPS(ibp3, UPS_3)
u4 = UPS(ibp4, UPS_4)


if __name__ == '__main__': 
    
    UPS_1.when_pressed = u1.ups_on_battery
    UPS_1.when_released = u1.ups_online
    
    UPS_2.when_pressed = u2.ups_on_battery
    UPS_2.when_released = u2.ups_online
    
    UPS_3.when_pressed = u3.ups_on_battery
    UPS_3.when_released = u3.ups_online
    
    UPS_4.when_pressed = u4.ups_on_battery
    UPS_4.when_released = u4.ups_online
    
    pause()
  
