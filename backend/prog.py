def ingred(list):
    x = 0
    for ingredient in list:
        x += 1
        print({
            "model": "recipes.ingredient",
            "pk": f"{x}",
            "fields": ingredient
                },','
        )
 