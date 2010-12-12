import os, pickle

from mako.template import Template

from google.appengine.api import channel
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from serialize import *

def paths( *args ):
    "Returns normalized paths"
    return os.path.abspath( os.path.join( os.path.dirname(__file__), *args) )

def render_template(fname, **kwargs):
    template = Template(filename=paths('static', 'html', fname))
    return template.render(**kwargs)
    

class GameState(db.Model):
    id = db.StringProperty()
    data = db.BlobProperty()

def load_gamestate(id):
    try:
        gamestates = db.GqlQuery("SELECT * FROM GameState WHERE id = :1", id)
        return gamestates[0]
    except IndexError:
        return None


def load_game(id):
    return pickle.loads(load_gamestate(id).data)
    
def save_game(game):
    old = load_gamestate(game.id)
    if old:
        old.data = pickle.dumps(game)
        old.put()
    else:
        gamestate = GameState()
        gamestate.id = game.id
        gamestate.data = pickle.dumps(game)
        gamestate.put()


class WebPlayer(Player):
    def make_decision(self, decision):
        self.game.current_decision = decision
        save_game(self.game)
        logging.info('Presenting client with decision %s Phase:%d Step:%d Data:%s' % (decision, self.game.phase, self.game.step, decision.__dict__))
        channel.send_message(self.clientid, game_to_json(self.game))

class MainPage(webapp.RequestHandler):
    ''' Simply returns the static html and javascript '''
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(render_template('board.html'))
        
class Connect(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        game = Game(1, WebPlayer)
        game.id = self.request.get('id')
        game.continuous = True
        
        clientid = str(random.randint(1, 100000))
        token = channel.create_channel(clientid)
        game.players[0].clientid = clientid
        game.players[0].channel = token
        
        game.begin_turn()
        game.step_game()
        data = game_to_json(game)
        save_game(game)
        self.response.out.write(data)

class Submit(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        
        
        game = load_game(self.request.get('id'))
        game.make_decision(game.current_decision, int(self.request.get('i')))
        save_game(game)
        
        self.response.out.write('OK')

        


application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/connect', Connect), ('/submit', Submit)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

