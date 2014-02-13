# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
def resume():
    return dict()

def pricing():
    return dict()

def examples():
    return dict()

def about_me():
    return dict()

def import_csv(table, file): 
    table.import_from_csv_file(file) 
    
def index():
     documents = db().select(db.documents.ALL)
     return dict(documents=documents)

def upload_docs():
     upload = crud.create(db.documents)
     if request.vars.csvfile != None: 
        import_csv(db[request.vars.table],request.vars.csvfile.file) 
        response.flash = T('data uploaded') 
     return dict(upload=upload)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)

    
def see_documents():
      table = SQLFORM.grid(db.documents, deletable=True, editable=True, csv=True, paginate=10)
      return dict(table=table)
      


def grid():
    response.tagline = "SQLFORM.grid example"
    grid = SQLFORM.grid(db.auth_user.id>0, ui="jquery-ui")
    code = CODE('grid = SQLFORM.grid(db.auth_user.id>0, ui="jquery-ui")',language='web2py')
    return dict(item=grid,code=code)

def table():
    response.view = 'default/item.html'
    response.tagline = "SQLTABLE example"
    rows = db(db.auth_user).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name,db.auth_user.email)
    table = SQLTABLE(rows, _class='zebra-striped sorted',headers='labels')
    table.elements()[-1].append(SCRIPT(""" 
          $(function() {
            $(".sorted").tablesorter({ sortList: [[1,0]] });
          });
    """))
    code = CODE("""
rows = db(db.auth_user).select()
table = SQLTABLE(rows, _class='zebra-striped sorted', headers='labels')
                """.strip())
    return dict(item=table, code=code)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
