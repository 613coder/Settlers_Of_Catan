import pygame
pygame.init()
import random
import sys
import time
clock = pygame.time.Clock()

def roll_dice():
    first_die = random.randint(1, 6)
    second_die = random.randint(1, 6)
    dice_rolled = first_die + second_die
    return dice_rolled


def redraw_board():
    screen.fill(pink)
    screen.blit(player_turn_text, (635, 30))
    screen.blit(dice_roll_text, (50, 400))
    resources1 = font.render(resource_text1, True, (0, 0, 0))
    resources2 = font.render(resource_text2, True, (0, 0, 0))
    screen.blit(resources1, (1200, 300))
    screen.blit(resources2, (1200, 350))
    dev_cards1 = font.render(dev_card_text1, True, (0, 0, 0))
    dev_cards2 = font.render(dev_card_text2, True, (0, 0, 0))
    screen.blit(dev_cards1, (1200, 500))
    screen.blit(dev_cards2, (1200, 550))
    for hex in hex_list:
        hex.draw()
    for player in player_class_list:
        for settlement in player.settlements:
            pygame.draw.rect(screen, player.color, ((settlement[0] - 15), (settlement[1] - 15), 30, 30))
    for player in player_class_list:
        for city in player.cities:
            pygame.draw.polygon(screen, player.color, (city[0], city[1], city[2]))
    for player in player_class_list:
        for end_points in player.roads:
            pygame.draw.line(screen, player.color, end_points[0], end_points[1], 7)
    screen.blit(robber, (robberX, robberY)) 

    pygame.display.flip()
                                                              #Functions for building stuff
def check_for_road(player, mouseX, mouseY):
    road_ends = "invalid"
    for hex in hex_list:
        #need to check if there is a settlement or road adjacent
        for point in hex.points:
            #top point
            if hex.points.index(point) == 0:
                #straight up
                if abs(point[0] - mouseX) < 5 and 0 < (point[1] - mouseY) < 70:    
                    road_ends = (point, (point[0], (point[1] - 90)))
                #down left
                if 0 < (point[0] - mouseX) < 70 and 0 < (mouseY - point[1]) < 35:    
                    road_ends = (point, ((point[0] - 77.94), (point[1] + 45)))
                #down right
                if 0 < (mouseX - point[0]) < 70 and 0 < (mouseY - point[1]) < 35:    
                    road_ends = (point, ((point[0] + 77.94), (point[1] + 45)))
            #top right point
            if hex.points.index(point) == 1:
                #straight down
                if abs(point[0] - mouseX) < 5 and 0 < (mouseY - point[1]) < 70:    
                    road_ends = (point, hex.points[2])
                #up right
                if 0 < (mouseX - point[0]) < 70 and 0 < (point[1] - mouseY) < 35:    
                    road_ends = (point, ((point[0] + 77.94), (point[1] - 45)))

                    #check to see if it's next to another road (to make it valid)
    not_next_to_road = False
    for ends in player.roads:
        if ends[0] == road_ends[0] or ends[0] == road_ends[1] or ends[1] == road_ends[0] or ends[1] == road_ends[1]:
            road_ends = road_ends
            not_next_to_road = False
            break
        else:
            not_next_to_road = True
                    #check to see if it's next to a settlement (to make it valid)
    not_next_to_settlement = False
    for coordinates in player.settlements:
        if coordinates == road_ends[0] or coordinates == road_ends[1]:
            road_ends = road_ends
            not_next_to_settlement = False
            break
        else:
            not_next_to_settlement = True
    
    if not_next_to_road and not_next_to_settlement:
        road_ends = "invalid"
    return road_ends

road_list = list()
def build_road(player):
            #taking the necessary resources
    if 'wood' in player.resources and 'brick' in player.resources:
        player.remove_resource('wood')
        player.remove_resource('brick')
        print("Building Road")
    else:
        print("You don't have the resources to build a road.")
        return

    #placing the road
    road_not_placed = True
    while road_not_placed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = pygame.mouse.get_pos()
                points = check_for_road(player, mouseX, mouseY)

                if points != "invalid" and points not in road_list:
                    pygame.draw.line(screen, player.color, points[0], points[1], 7)
                    player.add_road(points)
                    road_list.append(points)
                    pygame.display.flip()
                    road_not_placed = False
                    print("road placed")


settlement_list = list()
def build_settlement(player):
    #taking the necessary resources
    if 'brick' in player.resources and 'wood' in player.resources and 'wool' in player.resources and 'wheat' in player.resources:
        player.remove_resource('brick')
        player.remove_resource('wood')
        player.remove_resource('wool')
        player.remove_resource('wheat')
        print("Building Settlement")
    else:
        print("You don't have the resources to build a settlement.")
        return
    #placing the settlement
    settlement_not_placed = True
    while settlement_not_placed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = pygame.mouse.get_pos()
                        #seeing which hex neighbors this corner
                for hex in hex_list:
                    for point in hex.points:                        
                        if (point[0], point[1]) in player.roads or setting_up:
                            if abs(point[0] - mouseX) < 30 and abs(point[1] - mouseY) < 30:
                                player.add_neighbor(hex.letter)
                                if (point[0], point[1]) not in settlement_list:
                                    pygame.draw.rect(screen, player.color, ((point[0] - 15), (point[1] - 15), 30, 30))
                                    pygame.display.flip()
                                    player.add_settlement((point[0], point[1]))
                                    settlement_list.append((point[0], point[1]))
    
                                    settlement_not_placed = False
                
    player.add_point(1)

city_list = list()
def build_city(player):
    #taking the necessary resources
    if player.resources.count('ore') >= 3 and player.resources.count('wheat') >= 2:
        player.remove_resource('ore')
        player.remove_resource('ore')
        player.remove_resource('ore')
        player.remove_resource('wheat')
        player.remove_resource('wheat')
    else:
        print("You don't have the resources to build a city.")
        return

    city_not_placed = True
    while city_not_placed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = pygame.mouse.get_pos()
                        #seeing which hex neighbors this corner
                for hex in hex_list:
                    for point in hex.points:
                        if abs(point[0] - mouseX) < 20 and abs(point[1] - mouseY) < 20 and (point[0], point[1]) in player.settlements:
                            print("placing city")
                            player.add_neighbor(hex.letter)
                            pygame.draw.polygon(screen, player.color, (((point[0] - 15), (point[1] - 15)), (point[0], point[1] - 30), ((point[0] + 14), (point[1] - 15))))
                            pygame.display.flip()
                            player.add_city((((point[0] - 15), (point[1] - 15)), (point[0], point[1] - 30), ((point[0] + 14), (point[1] - 15))))
                            city_list.append((((point[0] - 15), (point[1] - 15)), (point[0], point[1] - 30), ((point[0] + 14), (point[1] - 15))))
                            city_not_placed = False
                
    player.add_point(1)

                                               #Development cards
dev_card_stack = ['knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'victory point', 'victory point', 'victory point', 'victory point', 'victory point', 'road building', 'road building', 'year of plenty', 'year of plenty', 'monoply', 'monoply']
random.shuffle(dev_card_stack)

def draw_dev_card():
    card_drawn = dev_card_stack[0]
    dev_card_stack.remove(card_drawn)
    return card_drawn

def buy_dev_card(player):
        #taking the necessary resources
    if 'ore' in player.resources and 'wheat' in player.resources and 'wool' in player.resources:
        player.remove_resource('ore')
        player.remove_resource('wheat')
        player.remove_resource('wool')
    else:
        print("You don't have the resources to buy a development card.")
        return

    #drawing the card and adding it to the player's list of development cards
    drawn_dev_card = draw_dev_card()
    player.add_dev_card(drawn_dev_card)
    if drawn_dev_card == 'victory point':
        player.add_point(1)
    pygame.display.flip()

def use_dev_card(player, card):
    if card not in player.dev_cards:
        print("You don't have a", card)
        return
    if card == "knight":
        place_robber()      #need to add stealing resource from another player
    if card == "road building":
        player.add_resource('brick')
        player.add_resource('brick')
        player.add_resource('wood')
        player.add_resource('wood')
        build_road(player)
        build_road(player)
    if card == "year of plenty":
        redraw_board()
        resource_rects = [(200, 100, 65, 32), (410, 100, 60, 32), (705, 100, 65, 32), (1000, 100, 60, 32), (1210, 100, 50, 32)]
        resources = ['brick', 'wood', 'wheat', 'wool', 'ore']

        choices = 0
        while choices != 2:
                #draw boxes of events to choose
            for rect in resource_rects:
                pygame.draw.rect(screen, black, pygame.Rect(rect))
                resource_num = resource_rects.index(rect)
                resource = resources[resource_num]
                resource_text = font.render(resource, True, (255, 255, 255))
                screen.blit(resource_text, (rect[0]+5, rect[1]+5))
            pygame.display.flip()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.quit()
   
               
                if event.type == pygame.MOUSEBUTTONUP:   
                    for resource_rect in resource_rects:
                        if pygame.Rect(resource_rect).collidepoint(event.pos):
                            resource_num = resource_rects.index(resource_rect)
                            resource = resources[resource_num]
                            choices += 1
                            
                            player.add_resource(resource)
                            #updating what resource what they just chose
                            resource_text1 = "Resources: " 
                            resource_text2 = ""    
                            for r in range(len(player.resources)):
                                if r < 5:
                                    resource_text1 += player.resources[r]
                                    if r != (len(player.resources) - 1):
                                        resource_text1 += ", "
                                if r >= 5:
                                    resource_text2 += player.resources[r]
                                    if r != (len(player.resources) - 1):
                                        resource_text2 += ", "
                            resources1 = font.render(resource_text1, True, (0, 0, 0))
                            resources2 = font.render(resource_text2, True, (0, 0, 0))
                            screen.blit(resources1, (1200, 300))
                            screen.blit(resources2, (1200, 350))
                            pygame.display.flip()
    if card == "monoply":
        redraw_board()
        resource_rects = [(200, 100, 65, 32), (410, 100, 60, 32), (705, 100, 65, 32), (1000, 100, 60, 32), (1210, 100, 50, 32)]
        resources = ['brick', 'wood', 'wheat', 'wool', 'ore']

        action = "choosing"
        while action != 'chosen':
                #draw boxes of events to choose
            for rect in resource_rects:
                pygame.draw.rect(screen, black, pygame.Rect(rect))
                resource_num = resource_rects.index(rect)
                resource = resources[resource_num]
                resource_text = font.render(resource, True, (255, 255, 255))
                screen.blit(resource_text, (rect[0]+5, rect[1]+5))
            pygame.display.flip()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.quit()
   
               
                if event.type == pygame.MOUSEBUTTONUP:   
                    for resource_rect in resource_rects:
                        if pygame.Rect(resource_rect).collidepoint(event.pos):
                            resource_num = resource_rects.index(resource_rect)
                            resource = resources[resource_num]
                            action = 'chosen'
                            break
        for P in player_class_list:
            for i in range(P.resources.count(resource)):
                P.remove_resource(resource)
                player.add_resource(resource)

        #updating what resource what they just chose
        resource_text1 = "Resources: " 
        resource_text2 = ""    
        for r in range(len(player.resources)):
            if r < 5:
                resource_text1 += player.resources[r]
                if r != (len(player.resources) - 1):
                    resource_text1 += ", "
            if r >= 5:
                resource_text2 += player.resources[r]
                if r != (len(player.resources) - 1):
                    resource_text2 += ", "
        resources1 = font.render(resource_text1, True, (0, 0, 0))
        resources2 = font.render(resource_text2, True, (0, 0, 0))
        screen.blit(resources1, (1200, 300))
        screen.blit(resources2, (1200, 350))
        pygame.display.flip()
    player.played_dev_card(card)

            #checking for largest army
    for P in player_class_list:
        if player.dev_cards_played.count('knight') > P.dev_cards_played.count('knight'):
            larger_army_than_everyone = True
        else:
            larger_army_than_everyone = False
    if player.dev_cards_played.count('knight') >= 3 and larger_army_than_everyone:
        for P in player_class_list:
            P.lost_largest_army()
        player.got_largest_army()

                                                                        #placing a robber
robber = pygame.image.load(second_robber_image_unedited.png)
def place_robber():
            #covering over past robber by redrawing the map
    redraw_board()

    for hex in hex_list:
        hex.remove_robber()

    robber_text = font_big.render("Place the robber on a different resource", True, black)
    screen.blit(robber_text, (350, 75))
    pygame.display.flip()
    robber_not_placed = True
    while robber_not_placed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = pygame.mouse.get_pos()
                for hex in hex_list:
                    if abs(hex.hexX - mouseX) < 20 and abs(hex.hexY - mouseY) < 20 and not hex.robber:
                        hex.set_robber()
                        global robberX
                        robberX = hex.hexX - 10
                        global robberY
                        robberY = hex.hexY - 10
                        screen.blit(robber, (robberX, robberY)) 
                        #pygame.draw.rect(screen, white, ((hex.hexX - 15), (hex.hexY - 15), 30, 30))
                        redraw_board()
                        robber_not_placed = False


                                                                            #PLAYER CLASS
class Player():
    def __init__(self, name, place_in_order, color):
        self.name = name
        self.hex_neighbors = list()
        self.resources = ['brick', 'wood', 'wheat', 'wool', 'brick', 'wood', 'wheat', 'wool', 'brick', 'wood', 'brick', 'wood']    #start with some resources to build 2 settlements and roads to start the game
        self.points = 0
        self.dev_cards = []
        self.dev_cards_played = list()
        self.largest_army = False
        self.cities = list()
        self.settlements = list()
        self.roads = list()
        self.place_in_order = place_in_order
        self.color = color

    def add_resource(self, resource):
        self.resources.append(resource)
    def remove_resource(self, resource):
        self.resources.remove(resource)

    def add_neighbor(self, hexagon):
        self.hex_neighbors.append(hexagon)

    def add_dev_card(self, card):
        self.dev_cards.append(card)
    def played_dev_card(self, card):
        self.dev_cards_played.append(card)
        self.dev_cards.remove(card)

    def got_largest_army(self):
        self.largest_army = True
    def lost_largest_army(self):
        self.largest_army = False

    def add_city(self, coordinates):
        self.cities.append(coordinates)
    def add_settlement(self, coordinates):
        self.settlements.append(coordinates)
    def add_road(self, coordinates):
        self.roads.append(coordinates)

    def add_point(self, number):
        self.points += number
    def remove_point(self, number):
        self.points -= number

    def __str__(self):
        return self.name
                        #player dictionaries
player_hex_neighbors = {}
player_resources = {}
player_points = {}
player_dev_cards = {}
dev_cards_played = {}
                          #inputting the players playing

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
brown = (58.8, 29.4, 0)
pink = (255,200,200)
yellow = (255,255,0)
orange = (255,127,80)
real_orange = (204, 102, 0)
real_pink = (153, 0, 153)
player_colors = [real_orange, real_pink, blue, white]
player_names = list()
player3 = 0
player4 = 0
player5 = 0
num_players = int(input("How many players are playing?"))

for player in range(num_players):
    name = input("Name of player #" + str(player + 1) + ": ")
    if player == 0:
        color = random.choice(player_colors)
        player_colors.remove(color)
        player1 = Player(name, player, color)
        player_class_list = [player1]
    if player == 1:
        color = random.choice(player_colors)
        player_colors.remove(color)
        player2 = Player(name, player, color)
        player_class_list.append(player2)
    if player == 2:
        color = random.choice(player_colors)
        player_colors.remove(color)
        player3 = Player(name, player, color)
        player_class_list.append(player3)
    if player == 3:
        color = random.choice(player_colors)
        player_colors.remove(color)
        player4 = Player(name, player, color)
        player_class_list.append(player4)
    if player == 4:
        color = random.choice(player_colors) #need to add another color to the list for the fifth player
        player_colors.remove(color)
        player5 = Player(name, player, color)
        player_class_list.append(player5)
   


                                                                                        #displaying the board


red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
brown = (58.8, 29.4, 0)
pink = (255,200,200)
yellow = (255,255,0)
orange = (255,127,80)
real_orange = (204, 102, 0)
real_pink = (153, 0, 153)

hex_points = {}

resources = ('wood', 'brick', 'wool', 'ore', 'wheat')
hexagon_resources = {}
hexagon_numbers = {}
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']

                                                                                 #HEX CLASS
class hexes():
    def __init__(self, letter):
        self.letter = letter
        self.robber = False
    def calculate_coordinates_for_hexes(self, x, y, size):
        self.hexX = x      
        self.hexY = y      
        self.hexSize = size  
 
        self.point1 = (hexX, hexY - hexSize)
        self.point2 = (hexX + (0.866*hexSize), hexY - (hexSize/2))
        self.point3 = (hexX + (0.866*hexSize), hexY + (hexSize/2))
        self.point4 = (hexX, hexY + hexSize)
        self.point5 = (hexX - (0.866*hexSize), hexY + (hexSize/2))
        self.point6 = (hexX - (0.866*hexSize), hexY - (hexSize/2))
        self.points = [self.point1, self.point2, self.point3, self.point4, self.point5, self.point6]
                   
    def set_resource(self, resource):
        self.resource = resource

    def set_dice_roll(self, number):
        self.dice_roll = number


                                                             #drawing the hexes
    def draw(self):
        if self.resource == 'wood':
            color = brown
        if self.resource == 'brick':
            color = red
        if self.resource == 'ore':
            color = black
        if self.resource == 'wool':
            color = green
        if self.resource == 'wheat':
            color = orange
        if self.resource == 'desert':
            color = yellow
        pygame.draw.polygon(screen, color, (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6))

                    #labeling the hex with its number that has to be rolled
        text = font.render(str(self.dice_roll), True, white)
        textRect = text.get_rect()
        textRect.center = (self.point1[0], (self.point1[1] + 90))
        screen.blit(text, textRect)

    def set_robber(self):
        self.robber = True
    def remove_robber(self):
        self.robber = False

    def __str__(self):
        return self.letter


                                                            #assigning resource and dice roll values for the hexes
def assign_hex_values():
    habitats = ['brick', 'brick', 'brick', 'wheat', 'wheat', 'wheat', 'wheat', 'wood', 'wood', 'wood', 'wood', 'ore', 'ore', 'ore', 'wool', 'wool', 'wool', 'wool', 'desert']
    numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    for hex in hex_list:
        #establishing the corresponding resource for each hex
        environment = random.choice(habitats)
        hex.set_resource(environment)
        habitats.remove(environment)
        #establishing the numbers that have to be rolled for each hex
        if hex.resource == 'desert':
            hex.set_dice_roll(7)
            global robberX
            robberX = hex.hexX - 10
            global robberY
            robberY = hex.hexY - 10
        else:
            number = random.choice(numbers)
            hex.set_dice_roll(number)
            numbers.remove(number)





pygame.display.set_mode()
screen = pygame.display.set_mode((1800, 1000))
pygame.init()
pygame.display.set_caption('Show Text') 
font = pygame.font.Font(None, 32)
font_medium = pygame.font.Font(None, 50)
font_big = pygame.font.Font(None, 64)

screen.fill(pink)

                                                                        #make an object for each hex                    
hexA = hexes('a')
hexB = hexes('b')
hexC = hexes('c')
hexD = hexes('d')
hexE = hexes('e')
hexF = hexes('f')
hexG = hexes('g')
hexH = hexes('h')
hexI = hexes('i')
hexJ = hexes('j')
hexK = hexes('k')
hexL = hexes('l')
hexM = hexes('m')
hexN = hexes('n')
hexO = hexes('o')
hexP = hexes('p')
hexQ = hexes('q')
hexR = hexes('r')
hexS = hexes('s')
hex_list = [hexA, hexB, hexC, hexD, hexE, hexF, hexG, hexH, hexI, hexJ, hexK, hexL, hexM, hexN, hexO, hexP, hexQ, hexR, hexS]
                                                                #calculate coordinates for hexes
hexX = 600
hexY = 220
hexSize = 90
for hex in hex_list:    
    hex.calculate_coordinates_for_hexes(hexX, hexY, hexSize)

    if letters.index(hex.letter) < 2:
        hexX += 1.732 * hexSize
    if letters.index(hex.letter) == 2:                #going back to the left side of the board to set up the next row of hexes
        hexX -= 4.33 * hexSize
        hexY += 1.5 * hexSize
    if letters.index(hex.letter) > 2 and letters.index(hex.letter) < 6:      
        hexX += 1.732 * hexSize
    if letters.index(hex.letter) == 6:                #going back to the left side of the board to set up the next row of hexes
        hexX -= 6.062 * hexSize
        hexY += 1.5 * hexSize
    if letters.index(hex.letter) > 6 and letters.index(hex.letter) < 11:
        hexX += 1.732 * hexSize
    if letters.index(hex.letter) == 11:               #going back to the left side of the board to set up the next row of hexes
        hexX -= 6.062 * hexSize
        hexY += 1.5 * hexSize
    if letters.index(hex.letter) > 11 and letters.index(hex.letter) < 15:
        hexX += 1.732 * hexSize
    if letters.index(hex.letter) == 15:                #going back to the left side of the board to set up the next row of hexes
        hexX -= 4.33 * hexSize
        hexY += 1.5 * hexSize
    if letters.index(hex.letter) > 15 and letters.index(hex.letter) < 18:
        hexX += 1.732 * hexSize



                            #assign hex values
assign_hex_values()
                
                            #draw the hexes
for hex in hex_list:
    hex.draw() 

screen.blit(robber, (robberX, robberY))  
pygame.display.flip()
                            #randomizing the hexes as many times as the user wants
print("Type 'r' to randomize and 'p' to continue with the selected board. ")
randomizing = True
while randomizing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                randomizing = False  
            if event.key == pygame.K_r:
                assign_hex_values()
                for hex in hex_list:
                    hex.draw()

                screen.blit(robber, (robberX, robberY))  
                pygame.display.flip()


                                                                                #playing two settlements to start the game
randomized_player_list = random.sample(player_class_list, len(player_class_list))
setting_up = True
first_round_of_settlements = True
while first_round_of_settlements:
    for player in randomized_player_list:
        player_turn_text = font_medium.render("", True, black)
        dice_roll_text = font_medium.render("", True, black)
        resource_text1 = "" 
        resource_text2 = ""  
        dev_card_text1 = "" 
        dev_card_text2 = ""        
        beginning_turn_text = font_big.render("It's " + str(player) + "'s turn to play a settlement and road", True, black)
        screen.blit(beginning_turn_text, (325, 75))
        pygame.display.flip()
        build_settlement(player)
        build_road(player)
        redraw_board()
    first_round_of_settlements = False
second_round_of_settlements = True
while second_round_of_settlements:
    for player in reversed(randomized_player_list):      
        beginning_turn_text = font_big.render("It's " + str(player) + "'s turn to play a settlement and road", True, black)
        screen.blit(beginning_turn_text, (325, 75))
        pygame.display.flip()
        build_settlement(player)
        build_road(player)
        redraw_board()
    second_round_of_settlements = False
    setting_up = False

                                                                                                                              #RUNNING THE GAME
playing = True
turn_num = 0
while playing:

            #figuring out who's turn it is
    if turn_num == num_players:
        turn_num = 0
    for player in player_class_list:
        if player.place_in_order == turn_num:
            player_turn = player
    
                       #displaying who's turn it is
    player_turn_text = font_big.render("It's " + str(player_turn) + "'s turn", True, black)
    screen.blit(player_turn_text, (635, 30))
    pygame.display.flip()

            #player rolls
    roll = roll_dice()
    dice_roll_text = font_medium.render(str(player_turn) + " rolled a " + str(roll), True, black)
    screen.blit(dice_roll_text, (50, 400))
            #seeing what resources were rolled and who gets the resources
    for hex in hex_list:
        if hex.dice_roll == roll and not hex.robber:
            for player in player_class_list:
                for letter in range(player.hex_neighbors.count(hex.letter)):
                    player.add_resource(hex.resource)

    if roll == 7:
        place_robber()
                #if someone has more than 7 resource cards, they lose half their resources
        for player in player_class_list:
            if len(player.resources) > 7:
                if len(player.resources) % 2 == 1:
                    num_to_remove = int((len(player.resources) - 1) / 2)
                else:
                    num_to_remove = int(len(player.resources) / 2)
                print(player.name, "has more than 7 resource cards. A random " + str(num_to_remove) + " cards has been removed from them.")
                resources_to_remove = random.sample(player.resources, num_to_remove)
                print("They lost:", resources_to_remove)
                for resource in resources_to_remove:
                    player.remove_resource(resource)

                        #displaying what resources the player has
    resource_text1 = "Resources: " 
    resource_text2 = ""    
    for resource in range(len(player_turn.resources)):
        if resource < 4:
            resource_text1 += player_turn.resources[resource]
            if resource != (len(player_turn.resources) - 1):
                resource_text1 += ", "
        if resource >= 4:
            resource_text2 += player_turn.resources[resource]
            if resource != (len(player_turn.resources) - 1):
                resource_text2 += ", "
    resources1 = font.render(resource_text1, True, (0, 0, 0))
    resources2 = font.render(resource_text2, True, (0, 0, 0))

                        #displaying what development cards the player has
    dev_card_text1 = "Dev cards: " 
    dev_card_text2 = ""
    redraw_board()
    for dev_card in range(len(player_turn.dev_cards)):
        if dev_card < 3:
            dev_card_text1 += player_turn.dev_cards[dev_card]
            if dev_card != (len(player_turn.dev_cards) - 1):
                dev_card_text1 += ", "
        if dev_card >= 3:
            dev_card_text2 += player_turn.dev_cards[dev_card]
            if dev_card != (len(player_turn.dev_cards) - 1):
                dev_card_text2 += ", "
    dev_cards1 = font.render(dev_card_text1, True, (0, 0, 0))
    dev_cards2 = font.render(dev_card_text2, True, (0, 0, 0))
    pygame.display.flip()


                            



    redraw_board()

                                                                                #Trading, building and dev cards
    event_rects = [(200, 80, 60, 32), (410, 80, 145, 32), (705, 80, 145, 32), (1000, 80, 63, 32), (1210, 80, 57, 32)]
    events = ['build', 'buy dev card', 'use dev card', 'trade', 'pass']

    action = "checking"
    while action != 'pass':
        action = "checking"
            #draw boxes of events to choose
        for rect in event_rects:
            pygame.draw.rect(screen, black, pygame.Rect(rect))
            event_num = event_rects.index(rect)
            event = events[event_num]
            event_text = font.render(event, True, (255, 255, 255))
            screen.blit(event_text, (rect[0]+5, rect[1]+5))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()
   
               
            if event.type == pygame.MOUSEBUTTONUP:   
                for event_rect in event_rects:
                    if pygame.Rect(event_rect).collidepoint(event.pos):
                        event_num = event_rects.index(event_rect)
                        action = events[event_num]
                        break

          
                                                             #building
        
        if action == 'build':
            redraw_board()
        while action == 'build':
            creation_rects = [(300, 80, 60, 32), (450, 80, 59, 32), (650, 80, 128, 32), (955, 80, 51, 32)]
            creations = ['back', 'road', 'settlement', 'city']
            unavailable = 0
            for rect in creation_rects:
                if creation_rects.index(rect) == 1:
                                          #only displaying the creations the player has the resources to build
                    if 'wood' in player_turn.resources and 'brick' in player_turn.resources:
                        pass
                    else:
                      unavailable += 1
                      continue
                if creation_rects.index(rect) == 2:
                    if 'wood' in player_turn.resources and 'brick' in player_turn.resources and 'wheat' in player_turn.resources and 'wool' in player_turn.resources:
                        pass
                    else:
                      unavailable += 1
                      continue
                if creation_rects.index(rect) == 3:
                    if player_turn.resources.count('ore') == 3 and player_turn.resources.count('wheat') == 2:
                        pass
                    else:
                      unavailable += 1
                      continue
              
                pygame.draw.rect(screen, black, pygame.Rect(rect))
                creation_num = creation_rects.index(rect)
                creation = creations[creation_num]
                creation_text = font.render(creation, True, (255, 255, 255))
                screen.blit(creation_text, (rect[0]+5, rect[1]+5))
            if unavailable == 3:
                redraw_board()
                action = 'checking'
                break
            pygame.display.flip()
            creation = "not selected"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.quit()
               
                if event.type == pygame.MOUSEBUTTONUP:   
                    for creation_rect in creation_rects:
                        if pygame.Rect(creation_rect).collidepoint(event.pos):
                            creation_num = creation_rects.index(creation_rect)
                            creation = creations[creation_num]
                            
            if creation == 'road':
                build_road(player_turn)
                redraw_board()
                action = "checking"
                
            if creation == 'settlement':
                build_settlement(player_turn)
                redraw_board()
                action = "checking"

            if creation == 'city':
                build_city(player_turn)
                redraw_board()
                action = "checking"
              
            if creation == 'back':
                redraw_board()
                action = "checking"              

        if action == "buy dev card":
            buy_dev_card(player_turn)
            redraw_board()

                                                        #using a dev card
        if action == 'use dev card':
            redraw_board()
        while action == 'use dev card':
            card_rects = [(250, 80, 60, 32), (400, 80, 75, 32), (625, 80, 146, 32), (921, 80, 153, 32), (1224, 80, 98, 32)]
            cards = ['back', 'knight', 'road building', 'year of plenty', 'monoply']
            for rect in card_rects:
                pygame.draw.rect(screen, black, pygame.Rect(rect))
                card_num = card_rects.index(rect)
                card = cards[card_num]
                card_text = font.render(card, True, (255, 255, 255))
                screen.blit(card_text, (rect[0]+5, rect[1]+5))
            pygame.display.flip()
            card = "not selected"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.quit()
               
                if event.type == pygame.MOUSEBUTTONUP:   
                    for card_rect in card_rects:
                        if pygame.Rect(card_rect).collidepoint(event.pos):
                            card_num = card_rects.index(card_rect)
                            card = cards[card_num]
                            if card != 'back':
                              use_dev_card(player_turn, card)

                            action = "checking"
                            redraw_board()


    redraw_board()


    turn_num += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.quit()
            playing = False
            
    #checking to see if anyone won (by getting 10 points)
    for player in player_class_list:
        if player.points == 10:
            screen.fill(white)
            winning_text = font_big.render(str(player) + " won!", True, black)
            screen.blit(winning_text, (650, 500))
            pygame.display.flip()
            time.sleep(5)
            playing = False
        if player.points == 8 and player.largest_army:
            winning_text = font_big.render(str(player) + " won!", True, black)
            screen.blit(winning_text, (650, 500))
            pygame.display.flip()
            time.sleep(5)
            playing = False

    clock.tick(60)


