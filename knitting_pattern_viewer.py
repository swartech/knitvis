from __future__ import print_function
import re, pygame, sys
from pygame.locals import *

pattern = []

def wrong_side(stitch):
    if stitch == 'K':
        return 'P'
    elif stitch  == 'P':
        return 'K'

def draw_stitch(stitch, x, y):
    if stitch == 'K':
        #draw knit stitch at x,y
        window.blit(knit_surface_obj, (x, y))
    elif stitch  == 'P':
        #draw purl stitch at x,y
        window.blit(purl_surface_obj, (x, y))

#parse the pattern from file
with open('pattern.txt') as pattern_file:
    expression = [line.rstrip('\n').split(" ") for line in pattern_file]

#print given pattern
print("INPUT GIVEN")
for i in expression:
    print(i)
print()

number_of_rows = int(expression[0][0])
length_of_row = int(expression[1][0])

expression = expression[2:]
print("PATTERN GIVEN")
print(number_of_rows, 'rows of', length_of_row, 'stitches')
for i in expression:
    print(i)
print()

#convert the pattern to an expression
for r in range(0, number_of_rows):
    temp = []
    repeats = []
    end = []
    after_brackets = False
    in_brackets = False
    for s in range(0, len(expression[r])):
        this_string = expression[r][s]
        if this_string[0] == '(':
            in_brackets = True
            this_string = this_string[1:]

        #check for numbers eg K2
        if len(this_string) > 1:
            foo = int(re.findall(r'\d+', this_string)[0])
            for i in range(foo):
                if in_brackets:
                    repeats.append(this_string[0])
                elif after_brackets:
                    end.append(this_string[0])
                else:
                    temp.append(this_string[0])
        #if just K or P
        else:
            if in_brackets:
                repeats.append(this_string)
            elif after_brackets:
                end.append(this_string)
            else:
                temp.append(this_string)
        #if the end of a repeat
        if this_string[-1] == '*':
            in_brackets = False
            after_brackets = True

    #repeat the pattern until the end border
    repeat_limit = length_of_row - len(end)
    while len(temp) < repeat_limit:
        for i in repeats:
            temp.append(i)
    for e in end:
        temp.append(e)

    #add this row to the pattern
    pattern.append(temp)

#print interpreted pattern
print("INTERPRETED PATTERN")
for i in pattern:
    print(i)
print()

stitch_height = 26
stitch_width = 32

WIDTH = length_of_row * stitch_width
HEIGHT = number_of_rows * stitch_height

pygame.init()
fps_clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Knitting Pattern Visualiser')

#load images
purl_surface_obj = pygame.image.load('purlbw.png')
knit_surface_obj = pygame.image.load('knitbw.png')

x = 0
y = HEIGHT - stitch_height

show_wrong_side = False

#rendering loop
while True:
    window.fill(pygame.Color(0, 0, 0)) #clear the screen with a grey colour
    y = HEIGHT - stitch_height
    x = 0

    #draw stitches
    if show_wrong_side:
        for r in range(number_of_rows):
            #if working on the wrong side going left to right
            if r % 2 == 0:
                for s in range(0, length_of_row):
                    draw_stitch(wrong_side(pattern[r][s]), x, y)
                    x += stitch_width
            else:
                #working on the right side going right to left
                for s in reversed(range(length_of_row)):
                    draw_stitch(pattern[r][s], x, y)
                    x += stitch_width

            y -= stitch_height
            x = 0
    else:
        for r in range(number_of_rows):
            #if working on the wrong side going left to right
            if r % 2 != 0:
                for s in range(0, length_of_row):
                    draw_stitch(wrong_side(pattern[r][s]), x, y)
                    x += stitch_width
            else:
                #working on the right side going right to left
                for s in reversed(range(length_of_row)):
                    draw_stitch(pattern[r][s], x, y)
                    x += stitch_width

            y -= stitch_height
            x = 0

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #if space is pressed swap sides
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if show_wrong_side:
                    show_wrong_side = False
                    pygame.display.set_caption('Knitting Pattern Visualiser - RIGHT SIDE')
                else:
                    show_wrong_side = True
                    pygame.display.set_caption('Knitting Pattern Visualiser - WRONG SIDE')

    pygame.display.update()
    fps_clock.tick(30)