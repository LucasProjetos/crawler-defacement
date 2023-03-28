from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.utils.url import url_is_from_any_domain
from mycrawler.items import MycrawlerItem
import logging, base64
 
 
class DefacementCrawler(CrawlSpider):
  logger = logging.getLogger(__name__)
  handle_httpstatus_list = range(200, 300) # 200 - 299: success http status codes
  name = 'defacementcrawler'
  allowed_domains = ['www.exemplo.com', 'www.exemplo2.com', 'ww2.exemplo.com', 'ww2.exemplo2.com']

  start_urls = ['https://ww2.exemplo.com/']
  custom_settings = {
    'LOG_FILE': 'logs/defacementcrawler.log',
    'LOG_LEVEL': 'DEBUG'
  }
 
  rules = (
Rule( LinkExtractor(tags=('a', 'area', 'map'), attrs='href', unique=True), callback='parse_item', cb_kwargs={'follow': True}, follow=True),
Rule( LinkExtractor(tags=('base', 'basefont'), attrs='href', unique=True), callback='parse_item', cb_kwargs={'follow': False},follow=False),
Rule( LinkExtractor(tags=('embed', 'link', 'object'), attrs=('src', 'href', 'data'),unique=True), callback='parse_item', cb_kwargs={'follow': False}, follow=False),
Rule( LinkExtractor(tags=('frame', 'iframe'), attrs='src', unique=True), callback='parse_item', cb_kwargs={'follow': True}, follow=True),
Rule( LinkExtractor(tags=('img', 'script', 'source', 'track'), attrs=('src','srcset'), unique=True), callback='parse_item', cb_kwargs={'follow': False}, follow=False),
Rule( LinkExtractor(tags='form', attrs='action', unique=True), callback='parse_item', cb_kwargs={'follow': False}, follow=False),
Rule( LinkExtractor(tags=('applet'), attrs='code', unique=True), callback='parse_item', cb_kwargs={'follow': False}, follow=False),
  )
 
  def parse_item(self, response, follow):
      item_list = []
      for link in LinkExtractor(allow=(),deny=self.allowed_domains).extract_links(response):
          off_item = MycrawlerItem()
          off_item['title']   = link.text.strip()
          off_item['desturl'] = link.url
          off_item['referer'] = response.url
          off_item['status']  = 0
          off_item['follow']  = False
          off_item['offsite'] = True
          off_item['base64']  = base64.urlsafe_b64encode(link.url.encode("utf-8")).decode("utf-8")
          #yield off_item
          item_list.append(off_item)
      item = MycrawlerItem()
      item['title']     = response.css('title::text').extract_first().encode("utf-8")
      item['desturl']   = response.url
      item['referer']   = response.request.headers["Referer"].decode("utf-8")
      item['status']    = response.status
      item['follow']    = follow
      item['offsite']   = False
      item['base64']    = base64.urlsafe_b64encode(response.url.encode("utf-8")).decode("utf-8")
      item['file_urls'] = [response.url]  #deactivate this to deactive page download
      item_list.append(item)
      return item_list
