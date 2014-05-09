# Scrapy settings for alboPretorioCento project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'alboPretorioCento'

SPIDER_MODULES = ['alboPretorioCento.spiders']
NEWSPIDER_MODULE = 'alboPretorioCento.spiders'

ITEM_PIPELINES = {
    'alboPretorioCento.pipelines.AlbopretoriocentoPipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'alboPretorioCento (+http://www.yourdomain.com)'
