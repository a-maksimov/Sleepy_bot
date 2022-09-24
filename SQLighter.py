# -*- coding: utf-8 -*-
'''
Created on Oct 22, 2017

@author: Administrator
'''
import sqlite3

class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self,table):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM {}'.format(table)).fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM sotd WHERE id = ?', (rownum,)).fetchall()[0]
        
    def select_last(self):
        """ Получаем последню строку """
        with self.connection:
            return self.cursor.execute('SELECT * FROM sotd WHERE id IN (SELECT MAX(id) FROM sotd)').fetchall()[0]
                                                                                            
    def select_random(self):
        """ Получаем одну случайную строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM sotd WHERE id IN (SELECT id FROM sotd ORDER BY RANDOM() LIMIT 1)').fetchall()[0]
    
    def select_username(self, username):
        """ Получаем строки от username """
        with self.connection:
            return self.cursor.execute('SELECT * FROM sotd WHERE name = ?', (username,)).fetchall()

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM sotd').fetchall()
            return len(result)

    def add(self, table, song):
        """ Add a new song into the table """
        with self.connection:
            return self.cursor.execute('INSERT INTO {}(file_id,title,name) VALUES(?,?,?)'.format(table), song)
        
    def add_twitter(self, table, account):
        """ Add a new account into the table """
        with self.connection:
            return self.cursor.execute('INSERT INTO {}(screen_name,user_id,favourites_count,like_id,submitter) VALUES(?,?,?,?,?)'.format(table), account)
        
    def add_subscriber(self, table, name, tg_id, screen_name):
        """ Add a new subscriber into the table """
        with self.connection:
            return self.cursor.execute('INSERT INTO {}(name,tg_id,screen_name) VALUES(?,?,?)'.format(table), (name, tg_id, screen_name,))
        
    def delete_twitter(self, table, screen_name):
        """ Delete twitter user from the table """
        with self.connection:
            # https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta/16856730
            return self.cursor.execute('DELETE FROM {} WHERE screen_name = ?'.format(table), (screen_name,))
            self.connection.commit()
            
    def delete_subscriber(self, table, tg_id):
        """ Delete subscriber from the table """
        with self.connection:
            return self.cursor.execute('DELETE FROM {} WHERE tg_id = ?'.format(table), (tg_id,))
            self.connection.commit()
    
    def select_one_account(self, table, screen_name):
        """ Получаем аккаунт"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM {} WHERE screen_name = ?'.format(table),(screen_name,)).fetchone()
        
    def select_one_subscriber(self, table, tg_id):
        """ Получаем подписчика"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM {} WHERE tg_id = ?'.format(table),(tg_id,)).fetchall()
        
    
    def update_twitter(self, table, likes_num, like_id, screen_name):
        """ Обновляем количество лайков """
        with self.connection:
            self.cursor.execute('UPDATE {} SET favourites_count = ?, like_id = ? WHERE screen_name = ?'.format(table),(likes_num, like_id, screen_name))
            self.connection.commit()
        
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()