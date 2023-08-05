import pandas as pd


def split_datecolumns(df, date_column):
    """日付を分割させカテゴリ値として処理させたいときにもちいる
    これは日付date_columnをインデックスにしている。
    月~日 = 0~6
    
    :param df: urlなどを取り除きたい文章。
    :type df: data series
    :param text: datetimeのcolumn
    :type text: text
    :return: 余分なデータが取り除かれた文章
    :rtype: pandas data series
    """

    df_date = pd.DataFrame()
    df_date['year'] = df[date_column].dt.year
    df_date['month'] = df[date_column].dt.month
    df_date['weekday'] = df[date_column].dt.weekday
    df_date['day'] = df[date_column].dt.day
    df_date['hour'] = df[date_column].dt.hour
    df_date['minute'] = df[date_column].dt.minute

    return df_date


def cleaning_content(law_ds):
    """文章からurlなどの余分なデータを取り除く

    :param law_ds: urlなどを取り除きたい文章。
    :type law_ds: data series
    :return: 余分なデータが取り除かれた文章
    :rtype: pandas data series
    """

    prep_ds = law_ds.replace(r'(http|https)://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?', "", regex=True
                             ).replace(r'\n', "", regex=True
                                       ).replace(r'\r', "", regex=True
                                                 ).apply(lambda x: x.split('https://t.co')[0]
                                                         ).apply(lambda x: x.split('#Peing')[0])

    return prep_ds


def url_count(law_ds):
    """urlリンクの出現回数のカウント

    :param law_ds: urlの出現回数をカウントしたい配列
    :type law_ds: data series
    :return: url
    :rtype: pandas data series int
    """
    prep_ds = law_ds.apply(
        lambda x: len([w for w in str(x).lower().split() if 'http' in w or 'https' in w]))

    return prep_ds


def cahr_count(law_ds):
    """urlなどの余分な要素を排除したコンテンツから文字数をカウント

    :param law_ds: 文字数をカウントしたい配列
    :type law_ds: pandas data series
    :return: 文字数
    :rtype: pandas data series int
    """
    prep_ds = law_ds.replace(r'(http|https)://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?', "", regex=True
                             ).replace(r'\n', "", regex=True
                                       ).replace(r'\r', "", regex=True
                                                 ).apply(lambda x: x.split('https://t.co')[0]
                                                         ).apply(lambda x: x.split('#Peing')[0]
                                                                 ).apply(lambda x: len(x))
    return prep_ds


def hashtag_count(law_ds):
    """ハッシュタグをカウントするハッシュタグ以降の文字を削除しようとすると文章途中から削除されるツイートもあるため、カウントに留める

    :param law_ds: 文字数をカウントしたい配列
    :type law_ds: data series
    :return: ハッシュタグ数
    :rtype: pandas data series int
    """

    prep_ds = law_ds.apply(lambda x: len([c for c in str(x) if c == '#']))
    return prep_ds


def mention_count(law_ds):
    """メンションをカウントするメンション以降の文字を削除しようとすると文章途中から削除されるツイートもあるため、カウントに留める

    :param law_ds: 文字数をカウントしたい配列
    :type law_ds: data series
    :return: メンション数
    :rtype: pandas data series int
    """

    prep_ds = law_ds.apply(lambda x: len([c for c in str(x) if c == '@']))
    return prep_ds

#     仕掛中def add_jp_holiday(law_df, date_column_name):
#     """祝日・振替休日を日曜もしくは指定の記号に変換する。
#     これは日付date_column_nameをjoinするときの軸にしている。
#     月~日 = 0~6　とし、規定値を日曜(6)としているが、祝日を'祝日'として扱いたいのであれば7等の値を代入する。
#
#     :param law_df: 日本の祝日を日曜と同列に扱いたいlaw_df
#     :type law_df: data series
#     :return: jp_holidayカラムを足した新たなdf
#     :rtype: pandas data series int
#     """
#
#     # 日本の祝日を日曜もしくは指定の記号と同列に扱う
#     jp_h_df = pd.read_csv('https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv',
#                           encoding="shift-jis", parse_dates=[0])
#
#     jp_h_df.columns = [date_column_name, 'holiday_name']
#
#     # 祝日・振替休日は日曜もしくは指定の記号に変換する。新しくインスタンスが作成されるのでdeep copy必要なし
#     prep_df = pd.merge(law_df, jp_h_df, how='left', on=date_column_name)
#
#     prep_df['jp_holiday'] = True
#     # 行数分だけ処理を回す
#     for i in range(prep_df.shape[0]):
#         if prep_df.holiday_name[i] != np.NaN:
#             prep_df['jp_holiday'][i] = False
#
#     return prep_df
