# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def home():
    return dict()

def about():
    return dict()

def membership():
    return dict()

def addMember():
    form = SQLFORM(db.members)
    if form.process(session=None, formname='members').accepted:
        response.flash = 'Members added successfully'
        redirect(URL('showMembersAdmin'))
    else:           
        response.flash = 'An error occurred'
    return dict()

def showMembers():
    members = db().select(db.members.ALL, orderby=~db.members.id)
    return dict(members=members)

def showMembersAdmin():
    members = db().select(db.members.ALL, orderby=~db.members.id)
    return dict(members=members)

def updateMember():
    memberId = request.args(0) or redirect(URL())
    member = db.members(memberId) or redirect(URL())
    form = SQLFORM(db.members, memberId)
    if form.process(session=None, formname='member_update').accepted:
        redirect(URL('showMembersAdmin'))
    return dict(member=member)




def deleteMember():
    if db(db.members.id == request.args(0)).delete():
        response.flash = 'Member Deleted Successfully'
    else:
        response.flash = 'An Error Occurred while deleting member'
    redirect(request.env.http_referer)

def addPage():
    memberId = request.args(0, cast=int) or redirect(URL())
    form = SQLFORM(db.pages)
    if form.process(session=None, formname='page').accepted:
        response.flash = 'note added successfully'
        redirect(URL('showPages', args=memberId))
    else:
        response.flash = 'error occurred while adding note'
    return dict(form=form, memberId=memberId)

def showPages():
    memberId = request.args(0) or redirect(URL())
    pages = db(db.pages.member_id==memberId).select(orderby=db.pages.id)
    return dict(pages=pages, memberId=memberId)

   
def contact():
    return dict()

def deletePage():
    pageId = request.args(0) or redirect(URL())
    if db(db.pages.id == pageId).delete():
        response.flash = 'Progress Deleted Successfully'
    else:
        response.flash = 'An Error Occurred while deleting progress'
    redirect(request.env.http_referer)

def update():
    submitted_week = request.vars.week
    submitted_file = request.vars.file
    submitted_kilograms = request.vars.kilograms
    submitted_centimetres = request.vars.centimetres
    submitted_id = request.vars.id
    memberId = request.vars.memberid

    if db(db.pages.id == submitted_id).select():


        db(db.pages.id == submitted_id).update(
            week=submitted_week,
            file=submitted_file,
            kilograms=submitted_kilograms,
            centimetres=submitted_centimetres
            )
        return redirect(URL('showPages', args=memberId))
    else:
        return 'An Error Occurred while deleting progress'



def updatePage():
    parameters = request.args
    submitted_id=parameters[0]
    memberId=parameters[1]
    page=db(db.pages.id==submitted_id).select()[0]
    return dict(page=page, memberId=memberId)

