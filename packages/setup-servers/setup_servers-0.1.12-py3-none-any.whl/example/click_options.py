import click


@click.command()
@click.option('--one', '--one-two', help='Some help text')
def example(one, *args, **kwargs):
    print(one)
    print(args)
    print(kwargs)


example()
