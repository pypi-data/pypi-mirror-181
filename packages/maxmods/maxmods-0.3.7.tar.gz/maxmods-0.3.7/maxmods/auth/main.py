'''An all-in-one user authenticator and data manager'''

from maxmods.auth.imports import *

class AuthSesh:
    '''
    Main class of the Auth module
    
    AuthSesh() connects to database internally
    
    AuthSesh(Address) connects to backend Auth server at address in path

    AuthSesh(Path) connects to database internally to database at Path location

    repr(AuthSesh) returns the current username
    '''
    
    def __init__(self, Address: str = None, Path: str = None):
        self._Path = Path
        self._Address = Address
        self._Id = Fernet.generate_key().hex()

        if self._Address == None:
            self._sesh = Session(self._Path)
            self._Path = ''
        else:
            self._sesh = requests.Session()
            self._Path = self._Address
        try:
            warnings.filterwarnings('ignore')
            self._requestHandle(self._sesh.post(self._Path + 'Cert', None, {}, verify=False).json())
            self._requestHandle(self._sesh.post(self._Path + 'Greet', None, {'Id':self._Id}, verify=True).json())
            
        except requests.ConnectionError as err:
            raise LocationError('Couldn\'t connect to backend server\nMessage:\n' + str(err))

    def __repr__(self):
        return f'AuthSesh({self._Path}).set_vals({self._Name}, {self._Pass})'        
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, val, trace):
        if str(val) != 'Username does not exist':
            self.terminate()
        

    def _certadder(self, server):
        with open('cacerts.pem', 'wb') as f:
            f.write(bytes(server.encode()))
        self._sesh.verify = 'cacerts.pem'
        
    @property
    def Pass(self):
        return self._Pass
    
    @property
    def Name(self):
        return self._Name
    
    def set_vals(self, Name: str, Pass:str):
        '''
        Sets the desired username and password 
        '''
        self._Name = Name
        self._Pass = Pass
        return self
    
    def save(self, Location: str, Data):
        '''
        Saves data to the specified location. Creates location if it doesn't exist

        If no location is specified and the data is a Dict, it will replace everythin with the Dict

        rasies LocationError if it fails

        Auth.Save('Loc1/Loc2/Loc3', 'Data') 
        '''
        Data = json.dumps(Data)
        
        return self._requestHandle(self._sesh.post(self._Path+'Save', None, {'Location':Location, 'Data':Data, 'Hash':self._Hash, 'Id':self._Id}, verify=True).json())
    def load(self, Location = ''):
        '''
        Loads data at specified location. Raises an exception if location doesn't exist

        Auth.Load('Loc1/Loc2/Loc3') Returns data in Loc1/Loc2/Loc3/
        '''
        return self._requestHandle(self._sesh.post(self._Path+'Load', None, {'Location':Location, 'Hash':self._Hash, 'Id':self._Id}, verify=True).json())
    
    def delete(self, Location: str):
        '''
        Deletes data at specified location. Raises an exception if location doesn't exist.

        Auth.Delete('Loc1/Loc2/Loc3') Deletes data in Loc1/Loc2/Loc3/
        '''
        return self._requestHandle(self._sesh.post(self._Path+'Delete', None, {'Location':Location, 'Hash':self._Hash, 'Id':self._Id}, verify=True).json())

    def login(self):
        '''
        Attempts to login with specified Auth.Name and Auth.Pass values
        
        Raises an exception if it fails
        '''
        self._requestHandle(self._sesh.post(self._Path+ 'Logout', None, {'Hash':self._Hash, 'Id':self._Id}, verify=True).json())
        return self._requestHandle(self._sesh.post(self._Path+'Login', None, {'Username':self._Name, 'Password':self._Pass, 'Hash':self._Hash, 'Id':self._Id}, verify=True).json())
        
    def signup(self):
        '''
        Attempts to signup with specified Auth.Name and Auth.Pass values
        
        Raises an exception if it fails
        '''
        return self._requestHandle(self._sesh.post(self._Path+'Signup', None, {'Username':self._Name, 'Password':self._Pass}, verify=True).json())
    
    def remove(self):
        '''
        Attempts to remove the user with specified Auth.Name and Auth.Pass values
        
        Raises an exception if it fails
        '''
        return self._requestHandle(self._sesh.post(self._Path+'Remove', None, {'Hash':self._Hash, 'Id':self._Id}, verify=True).json())
    
    def terminate(self):
        '''
        Closes connection to backend and saves cache
        
        if you do not manually call this, you are at the mercy of the garbage collector (unless you are using the context manager!)
        '''
        self._requestHandle(self._sesh.post(self._Path+ 'Logout', None, {'Hash':self._Hash, 'Id':self._Id}, verify=True).json())
        self._requestHandle(self._sesh.post(self._Path+'Leave', None, {'Hash':self._Hash, 'Id':self._Id}, verify=True).json())

    
    def _requestHandle(self, request):
        if request['Code'] == 200:
            return self
        
        elif request['Code'] == 202:
            return request['Data']
        
        elif request['Code'] == 416:
            raise LocationError('Loaction does not exist')
        
        elif request['Code'] == 401:
            raise PasswordError('Incorrect password')
        
        elif request['Code'] == 404:
            raise UsernameError('Username does not exist')
        
        elif request['Code'] == 406:
            raise UsernameError('Invalid username')
        
        elif request['Code'] == 409:
            raise UsernameError('Username already exists')
        
        elif request['Code'] == 423:
            raise AuthenticationError('Failed to authenticate user')

        elif request['Code'] == 101:
            self._Hash = request['Hash']
        
        elif request['Code'] == 102:
            self._certadder(request['Server'])
            
        elif request['Code'] == 420:
            raise DataError(f"An error occured during the request, here is the data we could recover: {request['Data']}/n Error: {request['err']}" )
            

def simple_syntax():        
    from maxmods import menu as Menu
    class AuthMenu:
        def MainMenu(self):
            self.Menu = Menu.BasicMenu('Auth Menu')
            self.Menu.add_item(1, 'Login', self.Login, 1)
            self.Menu.add_item(2, 'Signup', self.Login, 2)
            return self.Menu
        def Login(self, val):
            Name = str(input('Username: '))
            Pass = str(input('Password: '))
            self.Auth = AuthSesh().set_vals(Name, Pass)
            try:
                if val == 1:
                    self.Auth.login()
                elif val == 2:
                    self.Auth.signup()
                self.Menu.update_item(1, 'Logout', self.Logout)
                self.Menu.remove_item(2)
                self.Menu.add_item(2, 'Load', self.Load)
                self.Menu.add_item(3, 'Save', self.Save)
                self.Menu.add_item(4, 'Delete', self.Delete)
                self.Menu.Title = f'Welcome {self.Auth.Name}'
            except AuthenticationError as err:
                print(err)
                input('Press enter')
        def Delete(self):
            Loc = str(input('From where: '))
            try:
                self.Auth.delete(Loc)
                input('Press enter')
            except LocationError as err:
                raise err
                input('Press enter')
        def Load(self):
            Loc = str(input('From where: '))
            try:
                print(self.Auth.load(Loc))
                input('Press enter')
            except LocationError as err:
                print(err)
                input('Press enter')
        def Save(self):
            Loc = str(input('To where: '))
            Dat = str(input('What to save: '))
            try:
                self.Auth.save(Loc, Dat)
                input('Press enter')
            except LocationError as err:
                print(err)
                input('Press enter')
        def Logout(self):
            self.Menu.update_item(1, 'Login', self.Login, 1)
            self.Menu.update_item(2, 'Signup', self.Login, 2)
            self.Menu.remove_item(3)
            self.Menu.remove_item(4)
            self.Menu.Title = 'Auth Menu'
            del(self.Auth)
    menu = AuthMenu().MainMenu()
    menu.run()
    
if __name__ == '__main__':
    simple_syntax()
