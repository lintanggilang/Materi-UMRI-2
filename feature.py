def umur(x):
    if x <= 12:
        return "1"
    elif 13 <= x <= 18:
        return "2"
    elif 19 <= x <= 40:
        return "3"
    elif 41 <= x <= 65:
        return "4"
    else:
        return "5"

def new_feature(df):
    df['umur'] = df['Age'].apply(lambda x: umur(x))
    df['WA'] = 0
    df.loc[(df['umur'] == '1') | (df['Sex'] == 'female'), 'WA'] = 1
    return df