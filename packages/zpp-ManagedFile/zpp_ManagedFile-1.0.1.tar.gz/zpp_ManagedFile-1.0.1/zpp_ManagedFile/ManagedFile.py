####################################################################
#/ Nom du projet: py-zpp_ManagedFile                              /#
#/ Nom du fichier: ManagedFile.py                                 /#
#/ Type de fichier: fichier principal                             /#
#/ Fichier annexe:                                                /#
#/                                                                /#
#/ Auteur: ZephyrOff  (Alexandre Pajak)                           /#
#/ Version: 1.0.1                                                 /#
#/ Description: Système de fichier managé pour le contrôle des    /#
#/              actions sur un fichier                            /#
#/ Date: 16/12/2022                                               /#
####################################################################

from io import BytesIO, StringIO
from tempfile import NamedTemporaryFile
from uuid import uuid1
from re import search


class ManagedFile:
    def __init__(self, filename=None, mode='r', typefile="stringio", encoding=None, closable=True):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        
        self.closed = False
        self.closable = closable
        
        self.typefile = typefile.lower()
        self.file = self.init_file()
        if self.file is None:
            return

        self.set_permissions()

    def init_file(self):
        try:
            fuuid = str(uuid1()).replace("-", "")
            
            if self.typefile == 'string':  #Simulation d'un fichier avec une chaîne
                self.name = "String"+fuuid
                self.seeker = 0
                return self.init_content()
            elif self.typefile == 'file':   #Ouverture d'un fichier
                if self.filename is not None:
                    self.name = self.filename
                    return open(self.filename, mode=self.mode, encoding=self.encoding)
                else:
                    print("Error: filename is not init")
                    return None
            elif self.typefile == 'bytesio':  #Création d'un bytesio
                self.name = "BytesIO"+fuuid
                return BytesIO()
            elif self.typefile == 'stringio':  #Création d'un stringio
                self.name = "StringIO"+fuuid
                return StringIO()
            elif self.typefile == 'tempfile':  #Création d'un fichier temporaire
                cp = NamedTemporaryFile(mode=self.mode, encoding=self.encoding)
                self.name = cp.name
                return cp
        except:
            return None

    def init_content(self):
        if "b" in self.mode:
            self.bytecontent = True
            return b''
        else: 
            self.bytecontent = False
            return ''

    def set_permissions(self):

        if self.typefile == 'stringio' or self.typefile == 'bytesio':
            self.readable = True
            self.writable = True

        else:
            self.readable = False
            self.writable = False

            if "r" in self.mode:
                self.readable = True
                if "+" in self.mode:
                    self.writable = True

            elif "w" in self.mode:
                self.writable = True
                if "+" in self.mode:
                    self.readable = True

            elif "a" in self.mode:
                self.writable = True
                if "+" in self.mode:
                    self.readable = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        if self.closed is False:
            self.close()

    def fileno(self):
        if self.typefile != 'string' and hasattr(self.file, 'fileno'):
            return self.file.fileno()
        else:
            return None

    def buffer(self):
        if self.typefile != 'string' and hasattr(self.file, 'buffer'):
            return self.file.buffer
        else:
            return None

    def flush(self):
        if self.typefile != 'string' and hasattr(self.file, 'flush'):
            return self.file.flush()
        else:
            return None

    def isatty(self):
        if self.typefile != 'string' and hasattr(self.file, 'isatty'):
            return self.file.isatty()
        else:
            return False

    @property
    def errors(self):
        if self.typefile != 'string' and hasattr(self.file, 'errors'):
            return self.file.errors
        else:
            return  None

    @property
    def newlines(self):
        if self.typefile == 'string' and hasattr(self.file, 'newlines'):
            return self.file.newlines
        else:
            return None

    def close(self):
        if self.closable:
            self.closed = True
            if self.typefile != 'string':
                self.file.close()

    def write(self,data):
        if self.closed is False:
            if self.writable:
                if self.typefile != 'string':
                    self.file.write(data)
                else:
                    if self.bytecontent:
                        if isinstance(data, bytes):
                            self.file+=data
                        else:
                            print("Error: data must be a bytes")
                    else:
                        if isinstance(data, str):
                            if self.encoding is not None:
                                self.file+=data.encode(self.encoding)
                            else:
                                self.file+=data
                        else:
                            print("Error: data must be a str")
            else:
                print("Error: File is not writable")
        else:
            print("Error: File is closed")

    def read(self, size=None):
        if self.closed is False:
            if self.readable:
                if self.typefile != 'string':
                    return self.file.read(size)
                else:
                    if size is None:
                        buff = self.file[self.seeker:]
                        self.seeker=len(self.file)
                        return buff
                    elif isinstance(size, int):
                        buff = self.file[self.seeker:size] 
                        self.seeker=size
                        return buff
            else:
                print("Error: File is not readable")
        else:
            print("Error: File is closed")

    def readline(self, size=None):
        if self.closed is False:
            if self.readable:
                if self.typefile != 'string':
                    if size is None:
                        return self.file.readline()
                    elif isinstance(size, int):
                        return self.file.readline(size)
                else:
                    if size is None:
                        content = self.file[self.seeker:]
                    elif isinstance(size, int):
                        content = self.file[self.seeker:size]
                    else:
                        return None
                    
                    if self.bytecontent:
                        content = content.decode()
                    
                    r = search('\n',content)
                    if r is None:
                        self.seeker=self.seeker+len(content)
                        return content
                    else:
                        index = r.span()[len(r.span())-1]
                        buff = content[:index]
                        self.seeker=self.seeker+index
                        return buff

            else:
                print("Error: File is not readable")
        else:
            print("Error: File is closed")

    def readlines(self):
        if self.closed is False:
            if self.readable:
                if self.typefile != 'string':
                    return self.file.readlines()
                else:
                    return self.file.split("\n")
            else:
                print("Error: File is not readable")
        else:
            print("Error: File is closed")

    def tell(self):
        if self.closed is False:
            if self.typefile != 'string':
                return self.file.tell()
            else:
                return self.seeker
        else:
            print("Error: File is closed")

    def seek(self, position, whence=0):
        if isinstance(whence, int) and whence>=0 and whence<=2:
            if self.closed is False:
                if self.typefile != 'string':
                    self.file.seek(position, whence)
                else:
                    if whence==0:
                        self.seeker=position
                    elif whence==1:
                        self.seeker+=position
                    elif whence==2:
                        self.seeker=len(self.file)-position
                    print(self.seeker)
                    if self.seeker>len(self.file):
                        self.seeker=len(self.file)
                    if self.seeker<0:
                        self.seeker=0
            else:
                print("Error: File is closed")
        else:
            print("Error: whence format not acceptable")

    def truncate(self, size=None):
        if self.closed is False:
            if self.writable:
                if self.typefile != 'string':
                    self.file.truncate(size)
                else:
                    if size is None:
                        if self.bytecontent:
                            self.file = b''
                        else:
                            self.file = ''
                    else:
                        self.file = self.file[:size]
            else:
                print("Error: File is not readable")
        else:
            print("Error: File is closed")

    def writelines(self, data):
        if isinstance(data, list):
            if self.closed is False:
                if self.writable:
                    if self.typefile != 'string':
                        self.file.writelines(data)
                    else:
                        if self.bytecontent:
                            self.file = ("".join(data)).encode(self.encoding)
                        else:
                            self.file+="".join(data)
                else:
                    print("Error: File is not readable")
            else:
                print("Error: File is closed")
        else:
            print("Error: data is not a list")

    def isClosable(self, action):
        if isinstance(action, bool):
            self.closable = action
        else:
            print("Error: Bad action")
