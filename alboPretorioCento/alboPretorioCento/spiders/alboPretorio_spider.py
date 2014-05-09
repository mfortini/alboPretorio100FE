from scrapy.spider import Spider
from scrapy.selector import Selector

from alboPretorioCento.items import AlbopretoriocentoItem

class alboPretorioSpider(Spider):
    name = "alboPretorio"
    allowed_domains="ulisse.comune.cento.fe.it"
    start_urls= [
            "http://ulisse.comune.cento.fe.it/ULISS-e/Bacheca/coatti02.aspx?bac_codice=50&SORT=DDPUB",
            ]

    def parse(self, response):

        sel = Selector(response)
        table = sel.xpath('//table[@id="tbl_dett"]')
        rows = table.xpath('.//tr')
        items = []
        for row in rows:
            item = AlbopretoriocentoItem()
            #id_registro     = Field()
            #oggetto         = Field()
            #data_inizio_pub = Field()
            #data_fine_pub   = Field()
            #tipo_documento  = Field()
            #documenti       = Field()
            try:
                id_registro = row.xpath('.//td/span[re:test(@id,"Reg\d*")]/text()').extract()[0]
                (anno,num) = id_registro.split('/')
                item['id_registro_anno'] = anno.strip()
                item['id_registro_num'] = num.strip()
                item['oggetto'] = row.xpath('.//td/span[re:test(@id,"ogg\d*")]/text()').extract()[0]
                item['data_inizio_pub'] = row.xpath('.//td/span[re:test(@id,"dtinip\d*")]/text()').extract()[0]
                item['data_fine_pub'] = row.xpath('.//td/span[re:test(@id,"dtfinp\d*")]/text()').extract()[0]
                item['tipo_documento'] = row.xpath('.//td/span[re:test(@id,"TAtto\d*")]/text()').extract()[0]
                item['documenti'] = row.xpath('.//td/a[re:test(@id,"link\d*")]/@href').extract()[0]

                items.append(item)
            except IndexError:
                pass


        return items

