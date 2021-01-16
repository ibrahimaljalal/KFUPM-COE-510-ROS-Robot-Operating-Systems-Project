while True:

    try:
        item = next(result1)
        print(item)

    except StopIteration:
        break