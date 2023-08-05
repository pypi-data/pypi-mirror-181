#######################################
#                                     #
#   name : html_editor                #
#   by : LesCodeursProLFJM            #
#   version : 1.0                     #
#   date : 28/10/2022                 #
#######################################

from os import *
def h1(title, page_name):
    page = page_name + '.html'
    fichier = open(page, "a")
    fichier.write('<h1>' + title + '<h1>')
def paragraph(text, page_name):
    page = page_name + '.html'
    fichier = open(page, "a")
    fichier.write('<p>' + text + '<p>')
def new_line(page_name):
    page = page_name + '.html'
    fichier = open(page, "a")
    fichier.write('<br>')
def title(title, page_name):
    page = page_name + '.html'
    fichier = open(page, "a")
    fichier.write('<title>' + title + '<title>')
def view(page_name):
    system(page_name)
def link(link, link_name, page_name):
    page = page_name + '.html'
    fichier = open(page, "a")
    fichier.write('<a href=' + link + '>' + link_name + '</a>')
def image(image_name, page_name, width):
    page = page_name + '.html'
    fichier = open(page, "a")    
    fichier.write('<img width=' + width + ' src = ' + image_name + '>')