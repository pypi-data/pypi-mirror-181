import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np


class DataSet:
    """ class to clean up data and construct train
    """
    def __init__(self, filepath):
        data_paths = {}
        for dirname, _, filenames in os.walk(filepath):
            for filename in filenames:
                data_paths[filename] = f"{dirname}/{filename}"
        data = {}
        for file, path in data_paths.items():
            data[file.split('.')[0]] = pd.read_csv(path)
        self.train_sales = data["sales_train"]
        self.items = data["items"]
        self.item_categories = data["item_categories"]
        self.shops = data["shops"]
        self.test = data["test"]
        self.train = []
        self.category71_items = [7149, 13597, 13598, 21788, 21789]
        self.shops_to_remove = [0, 1, 9, 20]


    def remove_negative_price_value(self):
        """ remove negative price value"""
        neg_itm_price = self.train_sales[self.train_sales.apply(lambda x: x["item_price"] < 0, axis=1)]
        self.train_sales = self.train_sales.drop(index=neg_itm_price.index)

    def clean_items(self):
        """ remove certain items"""
        self.items.drop(self.category71_items, inplace=True)

    def clean_shops(self):
        """ remove certain shops"""
        self.shops.drop(self.shops_to_remove, inplace=True)

    def drop_outliers(self, max):
        """drop outliers in item_count"""
        self.train_sales = self.train_sales[self.train_sales.item_cnt_day.apply(lambda x: x < max)]

    def convert_negative_sales(self):
        """converts negative item counts to zero"""
        ind0 = (self.train_sales.item_cnt_day < 0)
        self.train_sales.item_cnt_day[ind0] = 0

    def convert_date(self):
        """ convert date to datetime and parse into month and day. clean out """
        self.train_sales.date = pd.to_datetime(self.train_sales.date)
        self.train_sales["year"] = self.train_sales.date.apply(lambda x: x.year)
        self.train_sales["month"] = self.train_sales.date.apply(lambda x: x.month)
        self.train_sales = self.train_sales[
            self.train_sales.date.apply(lambda x: not (x.year == 2015 and (x.month == 11 or x.month == 12)))]
        self.train_sales = self.train_sales.drop(columns='date')

    def dissect_shop_name(self):
        """ dissects shop name into two features
        takes first word of shop name as city. Takes the rest and categorizes as certain type
        """
        def tokenize(s):
            return list(filter(lambda x: x != '', re.split('\?|!|,| |$|\(|\)|"', s)))

        vector = TfidfVectorizer(tokenizer=tokenize)
        sklearn_tokenizer = vector.build_tokenizer()
        word_list = self.shops.shop_name.apply(lambda x: sklearn_tokenizer(x))
        tc = word_list[59][1]
        self.shops["city"] = word_list.apply(lambda x: x[0])
        self.shops["type"] = word_list.apply(lambda x: "mall" if bool(set(x) & {tc, "ТРЦ", "ТК", "МТРЦ", "ТРК"})
        else "online" if bool(set(x) & {"1С-Онлайн", "Интернет-магазин"}) else "store")
        self.shops = self.shops.drop(columns='shop_name')
        self.shops = pd.get_dummies(self.shops)

    def dissect_category_name(self):
        """ extract features from item_category_name

        Takes the first part as main big category. Takes rest as subcategory.
        """
        def tokenize(s):
            return list(filter(lambda x: x != '', re.split('\?|!|,|-|/|$|\(|\)|"', s)))

        vector = TfidfVectorizer(tokenizer=tokenize)
        sklearn_tokenizer = vector.build_tokenizer()
        word_list = self.item_categories.item_category_name.apply(lambda x: sklearn_tokenizer(x))
        self.item_categories["category"] = word_list.apply(lambda x: x[0])
        self.item_categories["subcategory"] = word_list.apply(lambda x: ' '.join(x[1:]))
        self.item_categories = self.item_categories.drop(columns='item_category_name')
        self.item_categories = pd.get_dummies(self.item_categories)

    def add_categories_to_items(self):
        """merge items and categories tables"""
        self.items = self.items.merge(self.item_categories, right_on='item_category_id', left_on='item_category_id')

    def compose_test(self, m, y):
        """merge test with shops and items"""
        self.test = self.test.merge(self.items, right_on="item_id", left_on="item_id")
        self.test = self.test.merge(self.shops, right_on="shop_id", left_on="shop_id")
        self.test["year"] = y
        self.test["month"] = m
        self.test = self.test.reindex(self.X.columns, axis=1)

    def compose_train(self):
        """merge train with shops and items and convert it to X and Y format"""
        self.items = self.items.drop(columns='item_name')
        self.train_sales = self.train_sales.drop(columns=['item_price', 'date_block_num'])
        self.train_sales = self.train_sales.groupby(['item_id', 'shop_id', 'year', 'month']).agg(
            {"item_cnt_day": "sum"}).reset_index()
        # self.train_sales = self.train_sales.drop(columns=['date_block_num'])
        self.train = self.train_sales.merge(self.items, right_on="item_id", left_on="item_id")
        self.train = self.train.merge(self.shops, right_on="shop_id",left_on= "shop_id").sort_values(
            by=["year", "month"]).reset_index(drop=True)
        self.Y = self.train.item_cnt_day
        self.X = self.train.drop(columns=['item_cnt_day', 'item_id', 'shop_id'])
        self.Y_t = np.log1p(self.Y)

    def compose_train_test(self, m, y):
        """ runs all the methods to compose train and test"""
        self.remove_negative_price_value()
        self.clean_shops()
        self.clean_items()
        self.drop_outliers(800)
        self.convert_date()
        self.dissect_category_name()
        self.dissect_shop_name()
        self.add_categories_to_items()
        self.compose_train()
        self.compose_test(m,y)