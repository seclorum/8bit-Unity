"""
 * Copyright (c) 2018 Anthony Beaucamp.
 *
 * This software is provided 'as-is', without any express or implied warranty.
 * In no event will the authors be held liable for any damages arising from
 * the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 *   1. The origin of this software must not be misrepresented * you must not
 *   claim that you wrote the original software. If you use this software in a
 *   product, an acknowledgment in the product documentation would be
 *   appreciated but is not required.
 *
 *   2. Altered source versions must be plainly marked as such, and must not
 *   be misrepresented as being the original software.
 *
 *   3. This notice may not be removed or altered from any distribution.
 *
 *   4. The names of this software and/or it's copyright holders may not be
 *   used to endorse or promote products derived from this software without
 *   specific prior written permission.
"""

from Tkinter import *
import tkMessageBox as messagebox
from tkFileDialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import os, pickle, pygubu

def FileBase(filepath, suffix):
    # Return asset file base
    return os.path.basename(filepath).lower().replace(suffix, '')

class Application:

    version = 1
    listbox_AppleBitmap = None
    listbox_AppleSprites = None
    listbox_AppleMusic = None
    listbox_AtariBitmap = None
    listbox_AtariSprites = None
    listbox_AtariMusic = None
    listbox_C64Bitmap = None
    listbox_C64Sprites = None
    listbox_C64Music = None
    listbox_OricBitmap = None
    listbox_OricSprites = None
    listbox_OricMusic = None
    listbox_Shared = None
    listbox_Code = None
    lists = None
    cwd = None
        
    def __init__(self, master):

        # Save working directory
        self.cwd = os.getcwd()
        self.cwd, dump = os.path.split(self.cwd)
        self.cwd, dump = os.path.split(self.cwd)
        self.cwd = self.cwd.replace(os.sep, "/")
        self.cwd += "/"

        # Create a builder
        self.builder = pygubu.Builder()

        # Load an ui file
        self.builder.add_from_file('builder.ui')

        # Show tite
        master.title("8bit-Unity Disk Builder") 
        
        # Add file menu
        menubar = Menu(master)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="New", command=self.FileNew)
        fileMenu.add_command(label="Load", command=self.FileLoad)
        fileMenu.add_command(label="Save", command=self.FileSave)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.FileExit)        
        menubar.add_cascade(label="File", menu=fileMenu)
        master.config(menu=menubar)
        
        # Create widgets using a master as parent
        self.mainwindow = self.builder.get_object('mainwindow', master)        
                
        # Connect callbacks
        self.builder.connect_callbacks(self)
        
        # Get list boxes and fields
        self.listbox_AppleBitmap = self.builder.get_object('Listbox_AppleBitmap')        
        self.listbox_AppleSprites = self.builder.get_object('Listbox_AppleSprites')        
        self.listbox_AppleMusic = self.builder.get_object('Listbox_AppleMusic')        
        self.listbox_AtariBitmap = self.builder.get_object('Listbox_AtariBitmap')        
        self.listbox_AtariSprites = self.builder.get_object('Listbox_AtariSprites')        
        self.listbox_AtariMusic = self.builder.get_object('Listbox_AtariMusic')     
        self.Checkbutton_AtariNoText = self.builder.get_object('Checkbutton_AtariNoText');
        self.Combobox_AtariDiskSize = self.builder.get_object('Combobox_AtariDiskSize');
        self.listbox_C64Bitmap = self.builder.get_object('Listbox_C64Bitmap')        
        self.listbox_C64Sprites = self.builder.get_object('Listbox_C64Sprites')        
        self.listbox_C64Music = self.builder.get_object('Listbox_C64Music')     
        self.listbox_OricBitmap = self.builder.get_object('Listbox_OricBitmap')        
        self.listbox_OricSprites = self.builder.get_object('Listbox_OricSprites')        
        self.listbox_OricMusic = self.builder.get_object('Listbox_OricMusic')     
        self.listbox_Shared = self.builder.get_object('Listbox_Shared')
        self.listbox_Code = self.builder.get_object('Listbox_Code')
        self.entry_Disk = self.builder.get_object('Entry_Disk');
        
        # Set some defaults
        self.Checkbutton_AtariNoText.state(['!selected'])
        self.Combobox_AtariDiskSize.current(0)

        # Make lists of various GUI inputs (adding new inputs to the end of each list will guarantee backward compatibility)
        self.entries = [ self.entry_Disk ]
        self.listboxes = [ self.listbox_Code, 
                           self.listbox_AppleBitmap, self.listbox_AppleSprites, self.listbox_AppleMusic,
                           self.listbox_AtariBitmap, self.listbox_AtariSprites, self.listbox_AtariMusic,
                           self.listbox_C64Bitmap,   self.listbox_C64Sprites,   self.listbox_C64Music,
                           self.listbox_OricBitmap, self.listbox_OricSprites, self.listbox_OricMusic,
                           self.listbox_Shared ]
        self.checkbuttons = [ self.Checkbutton_AtariNoText ]
        self.comboboxes = [ self.Combobox_AtariDiskSize ]
                       
    def FileNew(self):
        # Reset all fields
        for l in self.listboxes:
            l.delete(0, END)
        self.entry_Disk.delete(0, END)
        self.entry_Disk.insert(0, 'diskname')
        
    def FileLoad(self):
        filename = askopenfilename(initialdir = "../../", title = "Load Builder Project", filetypes = (("Project files","*.builder"),)) 
        if filename is not '':
            # Unpickle data
            with open(filename, "rb") as fp:
                # Version number
                print "File version: " + str(pickle.load(fp))
                data = pickle.load(fp)
                                
                # Entry boxes
                while data != 'entries':
                    data = pickle.load(fp)                    
                for item in self.entries:
                    data = pickle.load(fp)
                    if data == 'lists':
                        break   # Legacy file
                    item.delete(0, END)
                    item.insert(0, data)
                    
                # List boxes                     
                while data != 'listboxes' and data != 'lists':  # Legacy files
                    data = pickle.load(fp)                    
                for item in self.listboxes:
                    data = pickle.load(fp)
                    if data == 'checkbuttons':
                        break   # Legacy file
                    item.delete(0, END)
                    for row in data:
                        item.insert(END, row)
                        
                # Check buttons
                while data != 'checkbuttons':
                    data = pickle.load(fp)                    
                for item in self.checkbuttons:                
                    data = pickle.load(fp)
                    if data == 'comboboxes':
                        break   # Legacy file
                    item.state(data)

                # Combo boxes
                while data != 'comboboxes':
                    data = pickle.load(fp)                    
                for item in self.comboboxes:                
                    data = pickle.load(fp)
                    item.set(data)
                    
    def FileSave(self):
        filename = asksaveasfilename(initialdir = "../../", title = "Save Builder Project", filetypes = (("Project files","*.builder"),))
        if filename is not '':
            # Fix extension
            if ".builder" not in filename.lower():
                filename += ".builder"
                
            # Pickle data
            with open(filename, "wb") as fp:
                # Version number
                pickle.dump(self.version, fp)
                
                # Entry boxes
                pickle.dump('entries', fp)
                for item in self.entries:
                    data = item.get()
                    pickle.dump(data, fp)
                    
                # List boxes                     
                pickle.dump('listboxes', fp)
                for item in self.listboxes:
                    data = list(item.get(0, END))
                    pickle.dump(data, fp)

                # Check buttons
                pickle.dump('checkbuttons', fp)
                for item in self.checkbuttons:
                    data = item.state()
                    pickle.dump(data, fp)

                # Check buttons
                pickle.dump('comboboxes', fp)
                for item in self.comboboxes:
                    data = item.get()
                    pickle.dump(data, fp)
                    
    def FileExit(self):
        sys.exit()
        
    def AppleBitmapAdd(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Bitmap", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_AppleBitmap.insert(END, filename)

    def AppleBitmapRem(self):
        self.listbox_AppleBitmap.delete(0, ACTIVE)
        
    def AppleSpritesSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Sprite Sheet", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_AppleSprites.delete(0, END)
            self.listbox_AppleSprites.insert(END, filename)

    def AppleMusicSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Music Track", filetypes = (("DUET files","*.duet"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_AppleMusic.delete(0, END)
            self.listbox_AppleMusic.insert(END, filename)
            
    def AtariBitmapAdd(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Bitmap", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_AtariBitmap.insert(END, filename)

    def AtariBitmapRem(self):
        self.listbox_AtariBitmap.delete(0, ACTIVE)
        
    def AtariSpritesSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Sprite Sheet", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_AtariSprites.delete(0, END)
            self.listbox_AtariSprites.insert(END, filename)

    def AtariMusicSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Music Track", filetypes = (("RMT files","*.rmt"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_AtariMusic.delete(0, END)
            self.listbox_AtariMusic.insert(END, filename)     

    def C64BitmapAdd(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Bitmap", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_C64Bitmap.insert(END, filename)

    def C64BitmapRem(self):
        self.listbox_C64Bitmap.delete(0, ACTIVE)
        
    def C64SpritesSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Sprite Sheet", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_C64Sprites.delete(0, END)
            self.listbox_C64Sprites.insert(END, filename)

    def C64MusicSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Music Track", filetypes = (("SID files","*.sid"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_C64Music.delete(0, END)
            self.listbox_C64Music.insert(END, filename)     

    def OricBitmapAdd(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Bitmap", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_OricBitmap.insert(END, filename)

    def OricBitmapRem(self):
        self.listbox_OricBitmap.delete(0, ACTIVE)
        
    def OricSpritesSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Sprite Sheet", filetypes = (("PNG files","*.png"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_OricSprites.delete(0, END)
            self.listbox_OricSprites.insert(END, filename)

    def OricMusicSel(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Music Track", filetypes = (("RMT files","*.rmt"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_OricMusic.delete(0, END)
            self.listbox_OricMusic.insert(END, filename)                   

    def SharedAdd(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Asset File", filetypes = (("All files","*.*"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_Shared.insert(END, filename)

    def SharedRem(self):
        self.listbox_Shared.delete(0, ACTIVE)
            
    def CodeAdd(self):
        filename = askopenfilename(initialdir = "../../", title = "Select Code File", filetypes = (("C files","*.c"),)) 
        if filename is not '':
            filename = filename.replace(self.cwd, '')
            self.listbox_Code.insert(END, filename)

    def CodeRem(self):
        self.listbox_Code.delete(0, ACTIVE)
        
    def GenerateBuilder(self):
        diskname = self.entry_Disk.get()
        shared = list(self.listbox_Shared.get(0, END))
        code = list(self.listbox_Code.get(0, END))
        if len(code) < 1:
            messagebox.showinfo('Error', 'Please add C source file(s)!')
            return

        ####################################################
        # Apple script
        bitmaps = list(self.listbox_AppleBitmap.get(0, END))
        sprites = list(self.listbox_AppleSprites.get(0, END))
        music = list(self.listbox_AppleMusic.get(0, END))
        with open("../../"+diskname+"-apple.bat", "wb") as fp:
            # Info
            fp.write('echo off\n\n')
            fp.write('rm [build]\\apple\\*.* \n\n')
            fp.write('echo --------------- CONVERT ASSETS ---------------  \n\n')
            
            # Bitmaps / Sprites
            for item in bitmaps:
                fp.write('utils\\py27\\python utils\\scripts\\apple\\AppleBitmap.py ' + item + ' [build]/apple/' + FileBase(item, '-apple.png') + '.map\n')
            if len(sprites) > 0:
                fp.write('utils\\py27\\python utils\\scripts\\apple\\AppleSprites.py ' + sprites[0] + ' [build]/apple/sprites.dat\n')

            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- COMPILE PROGRAM ---------------\n\n')

            # Compilation
            comp = 'utils\\cc65\\bin\\cl65 -o [build]/apple/' + diskname.lower() + '.bin -Cl -O -t apple2 -C unity/Apple/apple2e.cfg -I unity '
            for item in code:
                comp += item
                comp += ' '
            fp.write(comp + 'unity/bitmap.c unity/chars.s unity/math.s unity/network.c unity/sfx.c unity/sprites.c unity/Apple/CLOCK.c unity/Apple/DHR.c unity/Apple/DUET.s unity/Apple/JOY.s unity/Apple/MOCKING.s unity/Apple/PADDLE.s unity/IP65/ip65.lib unity/IP65/ip65_apple2.lib\n')
            
            # Compression
            cmd = 'utils\\scripts\\exomizer sfx $0803 -t162 -Di_load_addr=$0803 [build]/apple/' + diskname.lower() + '.bin@$0803,4'
            if len(sprites) > 0:
                cmd += ' [build]/apple/sprites.dat'
            if len(music) > 0:    
                cmd += ' ' + music[0]
            cmd += ' -o [build]/apple/loader\n'
            fp.write(cmd)

            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- APPLE DISK BUILDER --------------- \n\n')

            # Disk builder
            fp.write('copy utils\\scripts\\apple\\AppleProDOS190.dsk [build]\\' + diskname + '-apple.dsk\n')
            fp.write('java -jar utils\\scripts\\apple\\AppleCommander.jar -cc65 [build]/' + diskname + '-apple.dsk LOADER bin 0x0803 < [build]/apple/loader\n')
            for item in shared:
                fp.write('java -jar utils\\scripts\\apple\\AppleCommander.jar -p [build]/' + diskname + '-apple.dsk ' + FileBase(item, '').upper() + ' bin < ' + item + '\n')
            for item in bitmaps:
                fp.write('java -jar utils\\scripts\\apple\\AppleCommander.jar -p [build]/' + diskname + '-apple.dsk ' + FileBase(item, '-apple.png').upper() + '.MAP bin < [build]/apple/' + FileBase(item, '-apple.png') + '.map\n')

            # Info
            fp.write('\necho DONE\n')
            fp.write('pause\n\n')
            
            # Start emulator?
            fp.write('cd "utils\emulators\AppleWin-1.26.3.1"\n')
            fp.write('Applewin.exe -d1 "..\..\..\[build]\\' + diskname + '-apple.dsk"\\n')
            
        ####################################################
        # Atari script
        bitmaps = list(self.listbox_AtariBitmap.get(0, END))
        sprites = list(self.listbox_AtariSprites.get(0, END))
        music = list(self.listbox_AtariMusic.get(0, END))
        with open("../../"+diskname+"-atari.bat", "wb") as fp:
            # Info
            fp.write('echo off\n\n')
            fp.write('rm [build]\\atari\\*.* \n\n')
            fp.write('echo --------------- CONVERT ASSETS ---------------  \n\n')
            
            # Bitmaps / Sprites
            for item in bitmaps:
                fp.write('utils\\py27\\python utils\\scripts\\atari\\AtariBitmap.py ' + item + ' [build]/atari/' + FileBase(item, '-atari.png') + '.map\n')
            if len(sprites) > 0:
                fp.write('utils\\py27\\python utils\\scripts\\atari\\AtariSprites.py ' + sprites[0] + ' [build]/atari/sprites.dat\n')

            # Shared Data
            for item in shared:
                fp.write('copy ' + item.replace('/','\\') + ' [build]\\atari\n')

            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- COMPILE PROGRAM ---------------\n\n')

            # Compilation
            if len(self.Checkbutton_AtariNoText.state()):
                configFile = 'atarixl-notext.cfg'
            else:
                configFile = 'atarixl.cfg'
            comp = 'utils\\cc65\\bin\\cl65 -o [build]/atari/program.bin -Cl -O -t atarixl -C unity/Atari/' + configFile + ' -I unity '
            for item in code:
                comp += item
                comp += ' '
            fp.write(comp + 'unity/bitmap.c unity/chars.s unity/math.s unity/network.c unity/sfx.c unity/sprites.c unity/Atari/POKEY.s unity/IP65/ip65.lib unity/IP65/ip65_atarixl.lib\n')
            fp.write('utils\\cc65\\bin\\cl65 -t atarixl -C atari-asm.cfg -o [build]/atari/basicoff.bin unity/Atari/BASICOFF.s\n')
            fp.write('utils\\scripts\\atari\\mads.exe -o:[build]/atari/dli.bin unity/Atari/DLI.a65\n')
            fp.write('utils\\scripts\\atari\\mads.exe -o:[build]/atari/rmt.bin unity/Atari/RMT.a65\n')

            # Merging
            cmd = 'utils\\py27\\python utils\\scripts\\atari\\AtariMerge.py [build]/atari/autorun [build]/atari/basicoff.bin [build]/atari/program.bin [build]/atari/dli.bin [build]/atari/rmt.bin'
            if len(music) > 0:    
                cmd += ' ' + music[0]
            if len(sprites) > 0:
                cmd += ' [build]/atari/sprites.dat'
            cmd += '\n'                
            fp.write(cmd)
            
            # Clean-up
            fp.write('rm [build]\\atari\\*.bin\n')
            fp.write('rm [build]\\atari\\*.dat\n')

            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- ATARI DISK BUILDER --------------- \n\n')

            # Disk builder
            if self.Combobox_AtariDiskSize.get() == '180KB':                
                diskSize = '720'
            else:
                diskSize = '1440'
            fp.write('utils\\scripts\\atari\\dir2atr.exe -dm -B utils/scripts/atari/AtariXboot.obx ' + diskSize + ' [build]/' + diskname + '-atari.atr [build]\\atari\n')

            # Info
            fp.write('\necho DONE\n')
            fp.write('pause\n\n')
            
            # Start emulator?
            fp.write('cd "utils\emulators\Altirra-2.90"\n')
            fp.write('Altirra.exe "..\..\..\[build]\\' + diskname + '-atari.atr"\n')             

        ####################################################
        # C64 script
        bitmaps = list(self.listbox_C64Bitmap.get(0, END))
        sprites = list(self.listbox_C64Sprites.get(0, END))
        music = list(self.listbox_C64Music.get(0, END))
        with open("../../"+diskname+"-c64.bat", "wb") as fp:
            # Info
            fp.write('echo off\n\n')
            fp.write('rm [build]\\c64\\*.* \n\n')
            fp.write('echo --------------- CONVERT ASSETS ---------------  \n\n')
            
            # Bitmaps / Sprites
            for item in bitmaps:
                fp.write('utils\\py27\\python utils\\scripts\\c64\\C64Bitmap.py ' + item + ' [build]/c64/' + FileBase(item, '-c64.png') + '.map\n')
            if len(sprites) > 0:
                fp.write('utils\\py27\\python utils\\scripts\\c64\\C64Sprites.py ' + sprites[0] + ' [build]/c64/sprites.dat\n')

            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- COMPILE PROGRAM ---------------\n\n')
            
            # Compilation
            comp = 'utils\\cc65\\bin\\cl65 -o [build]/c64/' + diskname.lower() + '.bin -Cl -O -t c64 -C unity/C64/c64.cfg -I unity '
            for item in code:
                comp += item
                comp += ' '
            fp.write(comp + 'unity/bitmap.c unity/chars.s unity/math.s unity/network.c unity/sfx.c unity/sprites.c unity/C64/JOY.s unity/c64/ROM.s unity/C64/SID.s unity/IP65/ip65.lib unity/IP65/ip65_c64.lib\n')
            
            # Compression
            cmd = 'utils\\scripts\\exomizer.exe sfx 2061 [build]/c64/' + diskname.lower() + '.bin'
            if len(sprites) > 0:
                cmd += ' [build]/c64/sprites.dat'
            if len(music) > 0: 
                cmd += ' ' + music[0]
            cmd += ' -o [build]/c64/loader.prg\n'
            fp.write(cmd)

            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- C64 DISK BUILDER --------------- \n\n')

            # Disk builder
            fp.write('utils\\scripts\\c64\\c1541 -format loader,666 d64 [build]/' + diskname + '-c64.d64 -attach [build]/' + diskname + '-c64.d64 ')
            fp.write('-write [build]/c64/loader.prg loader.prg ')
            for item in shared:
                fp.write('-write ' + item + ' ' + FileBase(item, '') + ' ')                
            for item in bitmaps:
                fp.write('-write [build]/c64/' + FileBase(item, '-c64.png') + '.map ' + FileBase(item, '-c64.png') + '.map ')                
                
            # Info
            fp.write('\n\necho DONE\n')
            fp.write('pause\n\n')
            
            # Start emulator?
            fp.write('cd "utils\emulators\WinVICE-2.4"\n')
            fp.write('x64.exe "..\..\..\[build]\\' + diskname + '-c64.d64"\n')              

        ####################################################
        # Oric script
        bitmaps = list(self.listbox_OricBitmap.get(0, END))
        sprites = list(self.listbox_OricSprites.get(0, END))
        music = list(self.listbox_OricMusic.get(0, END))
        with open("../../"+diskname+"-oric.bat", "wb") as fp:
            # Info
            fp.write('echo off\n\n')
            fp.write('rm [build]\\oric\\*.* \n\n')
            fp.write('echo --------------- CONVERT ASSETS ---------------  \n\n')
            
            # Process Shared / Bitmaps / Sprites
            for item in shared:
                filebase = FileBase(item, '')
                fp.write('utils\\scripts\\oric\\header -a0 ' + item + ' [build]/oric/' + filebase + ' $A000\n')
            for item in bitmaps:
                filebase = FileBase(item, '-oric.png')
                fp.write('utils\\py27\\python utils\\scripts\\oric\\OricBitmap.py ' + item + ' [build]/oric/' + filebase + '.raw 19\n')
                fp.write('utils\\scripts\\oric\\header -a0 [build]/oric/' + filebase + '.raw [build]/oric/' + filebase + '.map $A000\n')
            if len(sprites) > 0:
                fp.write('utils\\py27\\python utils\\scripts\\oric\\OricSprites.py ' + sprites[0] + ' [build]/oric/sprites.raw\n')
                fp.write('utils\\scripts\\oric\\header -a0 [build]/oric/sprites.raw [build]/oric/sprites.dat $9000\n')

            # Clean-up
            fp.write('rm [build]\\oric\\*.raw\n')
                
            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- COMPILE PROGRAM ---------------\n\n')

            # Compilation
            comp = 'utils\\cc65\\bin\\cl65 -o [build]/oric/launch.bin -Cl -O -t atmos -C unity/Oric/oric.cfg -I unity '
            for item in code:
                comp += item
                comp += ' '
            fp.write(comp + 'unity/bitmap.c unity/chars.s unity/math.s unity/network.c unity/sfx.c unity/sprites.c unity/Oric/files.c unity/Oric/joysticks.c unity/Oric/keyboard.s unity/Oric/libsedoric.s unity/Oric/utils.s \n')

            # Fix header
            fp.write('utils\\scripts\\oric\\header.exe [build]/oric/launch.bin [build]/oric/launch.com $0501\n')
            
            # Clean-up
            fp.write('rm [build]\\oric\\*.bin\n')

            # Info
            fp.write('\necho DONE!\n\n')
            fp.write('echo --------------- ORIC DISK BUILDER --------------- \n\n')

            # Disk builder
            cmd = 'utils\\scripts\\oric\\tap2dsk.exe -iLAUNCH.COM [build]/oric/launch.com [build]/oric/sprites.dat'
            for item in shared:
                cmd += ' [build]/oric/' + FileBase(item, '')
            for item in bitmaps:
                cmd += ' [build]/oric/' + FileBase(item, '-oric.png') + '.map'
            cmd += ' [build]/' + diskname + '-oric.dsk\n'
            fp.write(cmd)
            fp.write('utils\\scripts\\oric\\old2mfm.exe [build]/' + diskname + '-oric.dsk\n')
            
            # Info
            fp.write('\necho DONE\n')
            fp.write('pause\n\n')
            
            # Start emulator?
            fp.write('cd "utils\emulators\Oricutron-1.2"\n')
            fp.write('oricutron.exe -d "..\..\..\[build]\\' + diskname + '-oric.dsk"\n')            
   
        # Done!
        messagebox.showinfo('Completed', 'Scripts generated in 8bit-Unity root folder!')
        
        
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.iconbitmap('builder.ico')
    root.resizable(False, False)
    root.mainloop()