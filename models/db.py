# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()


## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.define_table('category',
    Field('category', requires=IS_NOT_EMPTY()))

db.define_table('products',
    Field('title'),
    Field('category', readable=True, writable=True, requires=IS_IN_DB(db, db.category.category, '%(category)s', IS_NOT_EMPTY())),
    Field('product_id', readable=False, writable=False),
    Field('description','text'),
    Field('price1', 'double'),
    Field('price3_5', 'double'),
    Field('price7', 'double'),
    Field('price14', 'double'),
    Field('price28', 'double'),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
    Field('votes', 'integer', readable=False, writable=False, default=0),    
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob', readable=False, writable=False)
)

db.define_table('documents',
  Field('file_name', 'string'),
  Field('category', 'string'),
  Field('file', 'upload', uploadfield='file_store'),
  Field('file_store', 'blob'))

db.define_table('routes',
        Field('route', 'upload', uploadfield='route_data'), 
        Field('route_data', 'blob') ,
        Field('best', 'string', default='')

)
  
db.define_table('parameters',

    Field('route', 'blob', requires=IS_IN_DB(db, db.routes.route, '%(route)s', IS_NOT_EMPTY())),
    Field('image_file_name', 'string'),
    Field('image_file_store', 'blob'),    
    Field('move_operator', requires=IS_IN_SET(['reversed_sections', 'swapped_cities'])),
    Field('max_iterations', 'integer'), 
    Field('start_temp', 'integer'),
    Field('alpha', 'double'),
    Field('verbose', 'boolean'),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=True)
)

db.define_table('clients',
    Field('name', 'string'),
    Field('address', 'string'),
    Field('phone_num', 'string'),
    Field('lat', 'double'),
    Field('lon', 'double')
    )
    
db.define_table('addresses',
    Field('active', 'boolean', default=False),
    Field('address', 'string')
    
)

db.define_table('orders',
    Field('name', requires=IS_IN_DB(db, db.clients.name, '%(name)s', IS_NOT_EMPTY())),
    Field('address', requires=IS_IN_DB(db, db.clients.address, '%(address)s', IS_NOT_EMPTY())),
    Field('price', 'integer'),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=True)
    )
