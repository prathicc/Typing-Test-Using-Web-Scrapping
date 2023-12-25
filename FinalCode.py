import pygame
import time
from bs4 import BeautifulSoup
import random
import requests
import csv
import matplotlib.pyplot as plt
import pandas as pd


pygame.init()

#Setting Up Variables

screen_width = 1200
screen_height = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)



clock = pygame.time.Clock() #defining clock
win = pygame.display.set_mode((screen_width, screen_height))
input_rect = pygame.Rect(190,420,140,50)
attempts = 0


#loading and scaling images
background_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/1.jpg")
background_img = pygame.transform.scale(background_load, (screen_width, screen_height))
menutxt_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/menu_text.png")
menutxt_img = pygame.transform.scale(menutxt_load, (2132/4, 359/4))
start_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/start.png")
start_img = pygame.transform.scale(start_load, (270*0.75, 97*0.75))
exit_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/exit.png")
exit_img = pygame.transform.scale(exit_load, (270*0.75, 97*0.75))
qbox_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/q_box.png")
qbox_img = pygame.transform.scale(qbox_load, (950*1.1, 300*1.1))
nxtsen_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/next_sentence.png")
nxtsen_img = pygame.transform.scale(nxtsen_load, (759*0.7, 76*0.7))
back_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/back.png")
back_img = pygame.transform.scale(back_load, (145*0.8, 76*0.8))
progress_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/show_progress.png")
progress_img = pygame.transform.scale(progress_load, (500, 97*0.75))
border_load = pygame.image.load("C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/border.png")
border_img = pygame.transform.scale(border_load, (screen_width, screen_height*1.5))

#fonts
text_font = pygame.font.SysFont('comicsans', 25)
input_font = pygame.font.SysFont('comicsans', 30)


def display_text(text, color, x, y):
    screen_text = text_font.render(text, 1, color) #antialias (for smooth edges)
    win.blit(screen_text, [x, y])
    pygame.display.update()


def main_window():
    draw_main_window()
    main_menu = True
    while main_menu:
        
        clock.tick(60)
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                main_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (x>480 and y>180 and x<705 and y<235):
                    main_menu = False
                    start_game()
                if (x>340 and y>275 and x<840 and y<330):
                    plot()
                if (x>490 and y>370 and x<700 and y<435):
                    main_menu = False


def get_sentence(): #SCRAPER
    url = "https://sentence.yourdictionary.com/a"
    website_html = requests.get(url).text
    soup = BeautifulSoup(website_html, 'html.parser')
    sentences = soup.find_all('p', class_ = "sentence-item__text")
    sentence_list = list()
    for i in sentences:
        if len(i.text)<80:
            sentence_list.append(i.text)

    return(random.choice(sentence_list))


def start_game():
    draw_game_window()

    global sentence
    sentence = get_sentence()
    display_text(sentence, BLACK, 170, 195)
    test_started = True
    global input_text
    input_text = ''
    global time_initial
    time_initial = time.time()
    while test_started:
        clock.tick(60)  


        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (x>20 and y>532 and x<150 and y<582):
                    main_window()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[0:-1]
                elif event.key == pygame.K_RETURN:
                    global time_final
                    time_final = time.time()
                    give_results()
                    win.blit(nxtsen_img, (665,530))
                elif event.key == pygame.K_TAB:
                    start_game()
                else:
                    input_text+=event.unicode
        
        pygame.draw.rect(win, WHITE, input_rect)
        text_surface = input_font.render(input_text, True, BLACK)
        win.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        input_rect.w = max(text_surface.get_width() + 10, 30)
        pygame.display.update()



def give_results():
    #TIME REQUIRED
    global attempts
    attempts+=1
    time_required = time_final - time_initial
    display_text(f'TIME REQUIRED: {time_required} sec'[0:-13], BLACK, 5,10)
    #ACCURACY
    words = len(sentence.split())
    words_right = len(set(input_text.split()) & set(sentence.split()))
    accuracy = words_right/len(set(sentence.split()))*100
    display_text(f'ACCURACY: {accuracy}%', BLACK, 500,10)
    #WPM
    wpm = (words/(float(time_required)/60))
    display_text(f'WPM: {wpm}'[:-13], BLACK, 1000,10)
    #data storage
    result_list = []
    result_list.append(attempts)
    result_list.append(accuracy)
    result_list.append(wpm)
    with open(('C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/Type_Info.csv'),"a") as File:
        writer = csv.writer(File)
        writer.writerow(result_list)
    File.close()
    plt.style.use('dark_background')
    #data frame variable: reads the csv file
    df = pd.read_csv('C:/Users/pawar/Desktop/CODE/PYTHON/VIIT/PBL/Type_Info.csv')
    global x1,y1,y2
    x1 = df['Attempts']
    y1 = df['Accuracy']
    y2 = df['Wpm']


def draw_main_window():
    pygame.display.set_caption("Typing Game")#
    win.blit(background_img, (0,0))
    win.blit(border_img, (0,-155))
    win.blit(menutxt_img, ((screen_width/2) - (2132/4)/2,screen_height/10))
    win.blit(start_img, ((screen_width/2) - (270*0.75)/2,175))
    win.blit(progress_img, ((screen_width/2) - (500)/2,270))
    win.blit(exit_img, ((screen_width/2) - (270*0.75)/2,365))
    pygame.display.update()


def draw_game_window():
    win.blit(background_img, (0,0))
    win.blit(qbox_img, ((screen_width/2) - (950*1.1)/2,50))
    win.blit(back_img, (30,530))
    pygame.display.update()



def plot():
    plt.title('Graph of Accuracy, Wpm')


    #Line graph
    plt.xlabel('Attempts', fontsize=18)

    plt.plot(x1,y1, label = 'Accuracy')
    plt.plot(x1,y2, label = 'Wpm')
    plt.scatter(x1,y1)
    plt.scatter(x1, y2)


    plt.legend()
    plt.show()



main_window()
pygame.quit()
