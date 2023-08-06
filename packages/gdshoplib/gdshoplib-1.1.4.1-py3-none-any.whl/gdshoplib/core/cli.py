import typer
from rich import print

# from gdshoplib import Description, Media, NotionManager
from gdshoplib import Product
from gdshoplib.apps.platforms.ula.manager import UlaManager

app = typer.Typer()


# @app.command()
# def update_descriptions(sku=None):
#     description = Description()
#     if not sku:
#         for product in description.notion_manager.get_products(as_generator=True):
#             description.update(product["sku"])
#             print(f"Обновлен продукт {product['sku']}")
#         return

#     description.update(sku)
#     print(f"Обновлен продукт {sku}")


# @app.command()
# def update_media(sku=None):
#     media = Media()
#     if sku:
#         media.product_update(sku)
#         print(f"Медия {sku} обновлены")

#     for product in NotionManager().get_products(format="model", as_generator=True):
#         media.save(product)
#         print(f"Медия {product.dict()['sku']} обновлены")


# @app.command()
# def update_sku():
#     NotionManager().set_sku()


@app.command()
def ula_feed():
    return print(UlaManager().feed(Product()))


if __name__ == "__main__":
    app()
