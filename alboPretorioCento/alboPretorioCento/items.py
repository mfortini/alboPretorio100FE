# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AlbopretoriocentoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    id_registro_anno = Field()
    id_registro_num  = Field()
    oggetto          = Field()
    data_inizio_pub  = Field()
    data_fine_pub    = Field()
    tipo_documento   = Field()
    documenti        = Field()
