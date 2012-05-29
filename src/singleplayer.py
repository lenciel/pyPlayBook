# -*- coding: UTF-8 -*-
'''
Created on May 28, 2012

@author: House.Li

This is the game constructor for single player mode
'''

#===============================================================================
# Imports
from os import listdir
from os.path import isfile, join, splitext
import time, sys, pygame, string
import ConfigParser
from pygame.locals import *
#===============================================================================

class ImageBook():
    '''
    Book class is the container class of the vedio/audio/image resources to play
    '''

    def __init__( self, configer, logger ):
        '''
        Initialization: start timer, load resources, load config file
        '''
        self.time = 0
        self.step = 0.01
        self.keys = []
        self.type = "image book"
        self.config = configer
        self.logger = logger
        self.black_color = ( 0, 0, 0 )
        self.white_color = ( 255, 255, 255 )
        self.player_name = self.config.get( 'Game', 'player_name' )
        self.image_list = self.read_image_list( 'data/test_images' )
        self.width = self.config.getint( 'Game', 'init_width' )
        self.height = self.config.getint( 'Game', 'init_height' )
        #for filename in self.image_list:
        #   extension = string.upper( splitext( filename )[1][1:] )
        #  print extension
        self.state = "start"

    def read_image_list( self, dirname ):
        '''
        get the file list in a directory
        #TODO: validate file MIME type to make sure it's a image
        '''
        files = [ join( dirname, f ) for f in listdir( dirname ) if isfile( join( dirname, f ) ) ]
        return files

    def show_image( self ):
        '''
        show image on the surface(display)
        '''
        self.graphic = pygame.image.load( self.image_list.pop() ).convert()
        display = pygame.display.set_mode( self.graphic.get_size() )
        display.blit( self.graphic, ( 0, 0 ) )
        pygame.display.flip()

    def play( self ):
        '''
        nothing but play
        '''
        pygame.init()
        display = pygame.display.set_mode( ( self.width, self.height ) )
        pygame.display.set_caption( self.config.get( 'Game', 'title' ) )

        #-----------------------------------------------------------------------
        #TEXT
        #-----------------------------------------------------------------------
        font = pygame.font.Font( 'data/FEASFBRG.ttf', 20 )
        font_h3 = pygame.font.Font( 'data/FEASFBRG.ttf', 60 )

        #TODO: maybe show the player name when he playing the game?
        text_player1 = font.render( self.player_name, True, self.black_color )

        text_player_finished = font_h3.render( "FINISHED!", True, self.white_color )
        text_pause = font_h3.render( "PAUSE", True, self.white_color )
        text_start = font_h3.render( "PRESS SPACE...", True, self.white_color )
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        #MUSIC
        #-----------------------------------------------------------------------
        pygame.mixer.pre_init( 44100, 16, 2, 4096 )
        background_music = pygame.mixer.Sound( 'data/sound/background.ogg' )
        background_music.set_volume( 0.3 )
        background_music.play( -1 )
        #-----------------------------------------------------------------------


        #-----------------------------------------------------------------------
        #GAME
        #-----------------------------------------------------------------------
        while True:
            #The time of game
            self.time += self.step
            #
            if len( self.image_list ) == 0 :
                display = pygame.display.set_mode( ( self.width, self.height ) )
                display.blit( text_player_finished, ( self.width / 2 - 120, self.height / 2 - 80 ) )
                self.state = "EndLevel"
#            elif self.state == "play":
#                self.step = 1
#                print self.keys
#                self.write_log( '\n' + '1player' + ',' + str( self.level ) + ',' + self.player_name + ',' + str( self.time ) + ',' + str( self.keys ) + ',' + ' ' )
#                self.keys = []
#                #play the image
#                graphic = pygame.image.load( self.image_list.pop() ).convert()
#                display = pygame.display.set_mode( graphic.get_size() )
#                display.blit( graphic, ( 0, 0 ) ) #Display image at 0, 0
#                pygame.display.flip()   #Update screen

            #--------------------------------------------------
            #Check Event
            #--------------------------------------------------
            for event in pygame.event.get():

                if event.type == QUIT:
                    self.logger.info( '===========Game Ends!!===================' )
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "start":
                        self.state = "play"
                        self.show_image()
                    elif event.key == pygame.K_SPACE and self.state == "play":
                        display.fill( self.black_color )
                        pygame.display.set_mode( ( self.width, self.height ) )
                        pygame.display.flip()
                        self.state = "pause"
                    elif event.key == pygame.K_SPACE and self.state == "pause":
                        self.state = "play"
                        pygame.display.set_mode( ( self.graphic.get_size() ) )
                        display.blit( self.graphic, ( 0, 0 ) )
                        pygame.display.flip()

                    if self.state == "play":
                        if event.key == pygame.K_PAGEDOWN :
                            self.logger.info( '\n' + '1player' + ',' + str( self.type ) + ',' + self.player_name + ',' + str( self.time ) + ',' + str( self.keys ) + ',' + ' ' )
                            self.keys = []
                            self.show_image()
                        else:
                            self.keys.append( event.key )

            if self.state == "start":
                display.blit( text_start, ( self.width / 2 - 140, self.height / 2 - 50 ) )

            if self.state == "pause":
                display.blit( text_pause, ( self.width / 2 - 70, self.height / 2 - 50 ) )

            pygame.display.update()
            time.sleep( self.step )

            if self.state == "EndLevel":
                background_music.stop()


if __name__ == "__main__" :

    book = ImageBook()
    book.play()


