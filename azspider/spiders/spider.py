import scrapy
import time
from twilio.rest import Client

class AuthorSpider(scrapy.Spider):
    name = 'amazon-reminder'
    URL = ''                                       # Mention URL
    time_delay = 600                               # Specify time delay in seconds


    account = ''                                   # Twilio Account
    token = ''                                     # Twilio Token
    twilio_to = ''                                 # Your phone number
    twilio_from = ''                               # Trial twilio number
    client  = Client(account, token)
    start_urls = [URL]

    def parse(self, response):
        # Xpath searched to check if it is available
        a = response.xpath('//*[@id="availability"]/span//text()').extract()[0]
        
        if 'Currently unavailable' in a:
            time.sleep(self.time_delay)
            yield scrapy.Request(url = self.URL,
                                callback = self.parse,
                                dont_filter=True)
        else:
            call = self.client.calls.create(to = self.twilio_to,
                                        from_ = self.twilio_from,
                                        url = "http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")