

def there(t, *args, **kwargs):
    print('there')

    def again(f):
        print('again')
        f
    return again


@there('a')
def hello():
    print('hello')


hello()
