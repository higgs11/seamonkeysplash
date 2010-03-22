import os
from controlmodule import ControlModule
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        controlmodules_query = ControlModule.all()
        controls = controlmodules_query.fetch(10)        

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'controls': controls,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Submit(webapp.RequestHandler):
    def post(self):
        contModule = ControlModule()
      
        if(users.get_current_user()):
            contModule.author = users.get_current_user()
            
        contModule.name = self.request.get('name')      
        contModule.wins = 0
        contModule.losses = 0
        
        contModule.put()
        self.redirect('/')
        
class AddWin(webapp.RequestHandler):
    def post(self):
        
        name = self.request.get('name')
        
        sameidresults = db.GqlQuery("SELECT * FROM ControlModule WHERE name = :1", name)
        for result in sameidresults:
            result.wins = result.wins + 1
            result.put()
        
        self.redirect('/')
        
class AddLoss(webapp.RequestHandler):
    def post(self):
        
        name = self.request.get('name')
        
        sameidresults = db.GqlQuery("SELECT * FROM ControlModule WHERE name = :1", name)
        for result in sameidresults:
            result.losses = result.losses + 1
            result.put()
        
        self.redirect('/')                   
  
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/submit', Submit),
                                      ('/addwin', AddWin),
                                      ('/addloss', AddLoss)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()