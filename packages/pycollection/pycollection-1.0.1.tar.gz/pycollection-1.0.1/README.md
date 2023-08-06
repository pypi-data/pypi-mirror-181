# collection

Collection is an amazing library that allows you to iterate through a list, but it returns a transformed item. It has a lot of methods to interact with the collection. It works similar than laravel collections. Current version is 1.0.0

## Basic usage
    
    class NumberCollection(Collection):

        def item(self, item):
            return Number(item)


    class Number:

        def __init__(self, item):
            self._item = item

        def value(self):
            return self._item


    numbers = NumberCollection([1,2,3,4,5])


    for element in elements:
        print(element.value())

    # output
    # > 1
    # > 2
    # > 3
    # > 4
    # > 5

## Available methods

| methods   | 
|------------|
| count       |
| json         |
| find         |
| where      |
| item        |
| first       |
| append    |
| items      |
