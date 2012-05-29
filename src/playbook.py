# -*- coding: UTF-8 -*-
'''
Created on Apr 17, 2012

@author: House.Li
'''


#===============================================================================
# Imports
from pygame import *
font.init()

import logging
import ConfigParser
from math import cos, radians
from datetime import datetime

import singleplayer
#===============================================================================


'''
GameBuilder is the main class
'''
class GameBuilder():

    def __init__( self, inifile ):

        # initialize logger
        self.__init_logger()

        # initial config
        self.__init_options( inifile )

    def __init_logger( self ):
        time_tuple = datetime.now().timetuple()
        time_now = "%d_%d_%d_%d_%d_%d" \
            % ( time_tuple[0], time_tuple[1], time_tuple[2],
                time_tuple[3], time_tuple[4], time_tuple[5] )
        self.logger = logging.getLogger( "PlayBook" )
        self.logger.setLevel( logging.INFO )
        self.fh = logging.FileHandler( "playbook_" + time_now + ".log" )
        self.fh.setLevel( logging.INFO )
        self.logger.addHandler( self.fh )

    def __init_options( self, inifile ):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp( open( inifile ) )

        # Create the parts of the interface
        # which can be modified by subclasses
        #
    def run( self ):
        time.Clock()
        from os.path import join

        screen = display.set_mode( ( self.config.getint( 'Elements', 'screen_width' ),
                                   self.config.getint( 'Elements', 'screen_height' ) ) )
        #self.logger.info( GameBuilder.__doc__ )


        #TODO use different fonts for different meanings 
        #Set up fonts in menu
        title_font = font.Font( join( self.config.get( 'Elements', 'title_font_in_menu' ) ),
                                self.config.getint( 'Elements', 'title_size_in_menu' ) )

        menu_font = font.Font( join( self.config.get( 'Elements', 'menuentry_font_in_menu' ) ),
                               self.config.getint( 'Elements', 'menuentry_size_in_menu' ) )

        info_font = font.Font( join( self.config.get( 'Elements', 'info_font_in_menu' ) ),
                               self.config.getint( 'Elements', 'info_font_size_in_menu' ) )

        mainmenu = title_font.render( 'PLAY BOOK', 1,
                                      ( self.config.getint( 'Elements', 'main_font_color_red' ),
                                        self.config.getint( 'Elements', 'main_font_color_green' ),
                                        self.config.getint( 'Elements', 'main_font_color_blue' ) ) )
        r = mainmenu.get_rect()
        r.centerx = self.config.getint( 'Elements', 'screen_center_x' )
        r.top = self.config.getint( 'Elements', 'screen_top_padding' )
        #screeneen.blit(image.load(join('data/bg.png')),(0,0)) if time.get_ticks()&1 else screen.fill(-1)
        background_main = image.load( self.config.get( 'Elements', 'background_picture' ) ).convert()
        screen.blit( background_main, ( 0, 0 ) )
        bg = screen.copy()
        screen.blit( mainmenu, r )
        display.flip()

        menu_color = ( self.config.getint( 'Menu_General', 'menu_color_red' ),
                        self.config.getint( 'Menu_General', 'menu_color_green' ),
                        self.config.getint( 'Menu_General', 'menu_color_blue' ) )

        info_color = ( self.config.getint( 'Menu_General', 'info_color_red' ),
                        self.config.getint( 'Menu_General', 'info_color_green' ),
                        self.config.getint( 'Menu_General', 'info_color_blue' ) )


        menu1 = {"menu":['PLAY', 'OPTION', 'ABOUT', 'EXIT'],
                 "font1":menu_font,
                 "pos":'center',
                 "color1":menu_color,
                 "light":self.config.getint( 'Menu_Main', 'animation_light' ),
                 "speed":self.config.getint( 'Menu_Main', 'animation_speed' ),
                 "lag":self.config.getint( 'Menu_Main', 'animation_lag' )}

        menu2 = {"menu":['Image', 'Audio' , 'Video', 'BACK'],
                 "font1":menu_font,
                 "font2":title_font,
                 "pos":'center',
                 "color1":menu_color,
                 "light":self.config.getint( 'Menu_Main', 'animation_light' ),
                 "speed":self.config.getint( 'Menu_Main', 'animation_speed' ),
                 "lag":self.config.getint( 'Menu_Main', 'animation_lag' )}

        menu4 = {"menu":['BACK'],
                 "font2":menu_font,
                 "pos":( self.config.getint( 'Menu_BACK', 'menu_position_x' ),
                         self.config.getint( 'Menu_BACK', 'menu_position_y' ) ),
                 "color1":menu_color,
                 "light":self.config.getint( 'Menu_BACK', 'animation_light' ),
                 "speed":self.config.getint( 'Menu_BACK', 'animation_speed' ),
                 "justify":self.config.getint( 'Menu_BACK', 'animation_justify' )}

#        menus = ( menu1, menu2, menu4, menu5 )
#        playlist = [menu1, menu2, menu4, menu5]

        resp = "re-show"
        while resp == "re-show":
            resp = self.__create_menu( **menu1 )[0]
        #=======================================================================
        # 
        # ABOUT entry in the menu
        #=======================================================================
        if resp == 'ABOUT':
            display.update( screen.blit( bg, r, r ) )

            display.update( screen.blit( info_font.render( '@author: ever',
                                                           1, info_color ),
                                                           ( 200, 450 ) ) )
            display.update( screen.blit( info_font.render( 'mailbox_address',
                                                           1, info_color ),
                                                           ( 205, 470 ) ) )
            display.update( screen.blit( info_font.render( 'Spring 2012',
                                                           1, info_color ),
                                                           ( 235, 490 ) ) )

            #screen.blit(background_main,(0,0))
            display.update( screen.blit( title_font.render( '***ABOUT***',
                                                            1, menu_color ),
                                                            ( 200, 120 ) ) )
            resp = self.__create_menu( **menu4 )[0]

        #=======================================================================
        # 
        # BACK entry in the menu
        #=======================================================================
        if resp == 'BACK':
            screen.blit( background_main, ( 0, 0 ) )
            display.update( screen.blit( title_font.render( 'PLAY BOOK ',
                                                            1, menu_color ),
                                                            ( 185, 120 ) ) )
            resp = self.__create_menu( **menu1 )[0]

        #=======================================================================
        # 
        # PLAY entry in the menu
        #=======================================================================
        if resp == 'PLAY':
            display.update( screen.blit( bg, r, r ) )
            display.update( screen.blit( title_font.render( 'PLAY',
                                                            1, menu_color ),
                                                            ( 255, 120 ) ) )
            resp = self.__create_menu( **menu2 )[0]

        #=======================================================================
        # 
        # Image entry in the menu
        #=======================================================================
        if resp == 'Image':
            self.logger.info( '===========Image Book Begins to Play!!========' )
            book = singleplayer.ImageBook( self.config, self.logger )
            book.play()

        #=======================================================================
        # 
        # Audio entry in the menu
        #=======================================================================
        if resp == 'Audio':
            print "not implemented yet"
#            book = singleplayer.AudioBook()
#            book.run()

        #=======================================================================
        # 
        # Video entry in the menu
        #=======================================================================
        if resp == 'Video':
            print "not implemented yet"
#            book = singleplayer.VideoBook()
#            book.run()

        #=======================================================================
        # 
        # OPTION entry in the menu
        #=======================================================================
        if resp == 'OPTION':
            print "not implemented yet"


    def __create_menu( self, menu, pos = 'center', font1 = None, font2 = None,
                       color1 = ( 128, 128, 128 ), color2 = None, interline = 5,
                       justify = True, light = 5, speed = 300, lag = 30 ):
        class Item( Rect ):

            def __init__( self, menu, label ):
                Rect.__init__( self, menu )
                self.label = label

        def show():
            i = Rect( ( 0, 0 ), font2.size( menu[idx].label ) )
            if justify: i.center = menu[idx].center
            else: i.midleft = menu[idx].midleft
            display.update( ( surface.blit( bg, menu[idx], menu[idx] ),
                              surface.blit( font2.render( menu[idx].label,
                                                          1, ( 255, 255, 255 ) ),
                                                          i ) ) )

            time.wait( 50 )
            surface.blit( bg, r2, r2 )
            [surface.blit( font1.render( item.label, 1, color1 ), item ) for item in menu if item != menu[idx]]
            r = surface.blit( font2.render( menu[idx].label, 1, color2 ), i )
            display.update( r2 )

            return r

        def anim():
            clk = time.Clock()
            a = [menu[0]] if lag else menu[:]
            c = 0
            while a:
                for i in a:
                    g = i.copy()
                    i.x = i.animx.pop( 0 )
                    r = surface.blit( font1.render( i.label, 1, color1 ), i )
                    display.update( ( g, r ) )
                    surface.blit( bg, r, r )
                c += 1
                if not a[0].animx:
                    a.pop( 0 )
                    if not lag: break
                if lag:
                    foo, bar = divmod( c, lag )
                    if not bar and foo < len( menu ):
                        a.append( menu[foo] )
                clk.tick( speed )


        events = event.get()
        surface = display.get_surface()
        surface_rect = surface.get_rect()
        bg = surface.copy()
        if not font1: font1 = font.Font( None, surface_rect.h // len( menu ) // 3 )
        if not font2: font2 = font1
        if not color1: color1 = ( 128, 128, 128 )
        if not color2: color2 = list( map( lambda x:x + ( 255 - x ) * light // 10, color1 ) )
        m = max( menu, key = font1.size )
        r1 = Rect( ( 0, 0 ), font1.size( m ) )
        ih = r1.size[1]
        r2 = Rect( ( 0, 0 ), font2.size( m ) )
        r2.union_ip( r1 )
        w, h = r2.w - r1.w, r2.h - r1.h
        r1.h = ( r1.h + interline ) * len( menu ) - interline
        r2 = r1.inflate( w, h )

        try: setattr( r2, pos, getattr( surface_rect, pos ) )
        except: r2.topleft = pos
        if justify: r1.center = r2.center
        else : r1.midleft = r2.midleft

        menu = [Item( ( ( r1.x, r1.y + e * ( ih + interline ) ), font1.size( i ) ), i ) for e, i in enumerate( menu )if i]
        if justify:
            for i in menu:
                i.centerx = r1.centerx

        if speed:
            for i in menu:
                z = r1.w - i.x + r1.x
                i.animx = [cos( radians( x ) ) * ( i.x + z ) - z for x in list( range( 90, -1, -1 ) )]
                i.x = i.animx.pop( 0 )
            anim()
            for i in menu:
                z = surface_rect.w + i.x - r1.x
                i.animx = [cos( radians( x ) ) * ( -z + i.x ) + z for x in list( range( 0, -91, -1 ) )]
                i.x = i.animx.pop( 0 )


        mpos = Rect( mouse.get_pos(), ( 0, 0 ) )
        event.post( event.Event( MOUSEMOTION, {'pos': mpos.topleft if mpos.collidelistall( menu ) else menu[0].center} ) )
        idx = -1
        display.set_caption( self.config.get( 'Elements', 'caption' ) )

        while True:

            ev = event.wait()
            if ev.type == MOUSEMOTION:
                idx_ = Rect( ev.pos, ( 0, 0 ) ).collidelist( menu )
                if idx_ > -1 and idx_ != idx:
                    idx = idx_
                    r = show()
            elif ev.type == MOUSEBUTTONUP and r.collidepoint( ev.pos ):
                ret = menu[idx].label, idx
                break
            elif ev.type == KEYDOWN:
                try:
                    idx = ( idx + {K_UP:-1, K_DOWN:1}[ev.key] ) % len( menu )
                    r = show()
                except:
                    if ev.key in ( K_RETURN, K_KP_ENTER ):
                        ret = menu[idx].label, idx
                        break
                    elif ev.key == K_ESCAPE:
                        ret = None, None
                        break
        surface.blit( bg, r2, r2 )

        if speed:
            [surface.blit( font1.render( i.label, 1, color1 ), i ) for i in menu]
            display.update( r2 )
            time.wait( 50 )
            surface.blit( bg, r2, r2 )
            anim()
        else: display.update( r2 )

        for ev in events: event.post( ev )
        return ret


if __name__ == "__main__" :

    mygame = GameBuilder( 'cfg.ini' )
    mygame.run()

