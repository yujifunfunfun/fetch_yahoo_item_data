import eel
from yahoo import *


@eel.expose
def main(item_name_str):
    fetch_item_from_item_name(item_name_str)

@eel.expose
def main2(seller_id_str):
    fetch_item_from_seller_id(seller_id_str)

eel.init("web")
eel.start("main.html",size=(600, 600))


