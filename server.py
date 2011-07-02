import os, logging
from mako.template import Template
import tornado.ioloop
import tornado.web

logging.basicConfig(level=logging.INFO)

from game.game import Game
from game.player import Player
from game.serialize import game_to_json

from message import MessageMixin

GAMES = {}

CURRENT_DIR = os.path.join(os.path.dirname(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, 'static')
TEMPLATE_DIR = os.path.join(CURRENT_DIR, 'static', 'html')

def render_template(name):
    t = Template(filename=os.path.join(TEMPLATE_DIR, name))
    return t.render()
    
class WebPlayer(Player):
    def make_decision(self, decision):
        logging.info('Presenting clients with decision %s Phase:%d Step:%d Data:%s' % (decision, self.game.phase, self.game.step, decision.__dict__))
        self.game.current_decision = decision
        MessageMixin().new_messages([game_to_json(self.game)])

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/connect", ConnectHandler),
            (r"/submit", SubmitHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
        ]
        settings = dict(
            static_path=STATIC_DIR,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(render_template('board.html'))
        
class ConnectHandler(tornado.web.RequestHandler):
    def get(self):
        
        id = self.get_argument('id')
        player = int(self.get_argument('player'))
        create = self.get_argument('create') == '1'
        
        if create:
            game = Game(player, WebPlayer)
            game.id = id
            game.continuous = True
            player = 0
            GAMES[game.id] = game
            game.begin_turn()
            game.step_game()
        else:
            game = GAMES[id]
                        
        data = game_to_json(game)
        self.write(data)
        
class SubmitHandler(tornado.web.RequestHandler):
    def post(self):
        game = GAMES[self.get_argument('id')]
        game.make_decision(game.current_decision, int(self.get_argument('i')))
        
        self.write('Ok')
        
        
class MessageUpdatesHandler(tornado.web.RequestHandler, MessageMixin):
    @tornado.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        self.wait_for_messages(self.async_callback(self.on_new_messages),
                               cursor=cursor)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))
            
        


if __name__ == "__main__":
    application = Application()
    PORT = 8080
    application.listen(PORT)
    print 'Server started on port %d' % PORT
    tornado.ioloop.IOLoop.instance().start()