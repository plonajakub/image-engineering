if __name__ == '__main__':
    import pandas as pd

    columns = ['x', 'y', 'z']
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    df = pd.DataFrame(columns=columns, data=data)

    print(df.describe())
    print(df)
