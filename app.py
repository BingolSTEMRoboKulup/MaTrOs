# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 12:43:19 2022

@author: BGBRSASUS
"""

import numpy as np

#import typing
#from typing import Any, Tuple

import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing

import tensorflow_text as tf_text

#import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker


import os
from flask import Flask, request, redirect, url_for, render_template,flash,jsonify
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__, static_url_path="/static")
api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def giris():
    return render_template('giris.html',page_title='MaTrOs 1.0')


@app.route('/cevir',methods=['POST'])
def sonuc():
    metin=(request.form['metin'])
    
    metinler = tf.constant([metin],)
    
    model = tf.saved_model.load('translator')
    
    cevrilmis_metin=model.tf_translate(metinler)
    for tr in cevrilmis_metin['text']:
        cevrilmis_metin=tr.numpy().decode()
       
    return render_template('sonuc.html', page_title='Ceviri Sonucu', metin=metin, cikarim=cevrilmis_metin,)
 
# ****************************************** RESTApi Kısmı *************************************
CORS(app)


class status (Resource):
    def get(self):
        try:
            return jsonify({'data': 'Api çalışıyor...'})
        except:
            return jsonify({'data': 'REST-Api veriyi alamadı...'})


class Cevir(Resource):
    def post(self, a):

    
        metin=a
    
        metinler = tf.constant([metin],)
    
        model = tf.saved_model.load('translator')
    
        cevrilmis_metin=model.tf_translate(metinler)
        for tr in cevrilmis_metin['text']:
            cevrilmis_metin=tr.numpy().decode()

        return jsonify({'data': a+'->'+cevrilmis_metin})


api.add_resource(status, '/durum')
api.add_resource(Cevir, '/cevir/<string:a>')



if __name__ == '__main__':
    app.run(debug=True)
