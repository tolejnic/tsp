#!/usr/bin/python
# -*- coding: utf-8 -*-

#################################TSP.py##########################################
import random
import shutil
import pickle
import sys
import getopt
import os
from math import sqrt
import gpolyencode

def google5e77efedbb728120():
    return dict(message='google-site-verification: google5e77efedbb728120.html')

def index():
    return dict()

def map_test():
    return dict()

def charts():
    return dict()


def getLatLng(addresses):
    from GoogleMaps import GoogleMaps
    latlng=[]
    gmaps = GoogleMaps('ABQIAAAA3IBuOitfkPwNDWiqqQcHCBT2yXp_ZAY8_ufC3CFXhHIE1NvwkxSfoUckXCUPUmN3veq7-AVDtPiLIA')
    for address in addresses:
        lat, lng = gmaps.address_to_latlng(address) 
        latlng.append((float(lat),float(lng)))
    return latlng

def unpackRoute():
    routes = pickle.load(open( "save.p", "rb" ))
              
def routes():
    route_table=SQLFORM.grid(db.routes, details=True, editable=True, deletable=True)
    return dict(table=route_table)

  
def addresses():
    addr_table=SQLFORM.grid(db.addresses, details=True, editable=True, selectable= lambda ids: update(ids), deletable=True)
    return dict(table=addr_table)
    
        
def parameters():
    response.files.append(URL('static', 'css/unicorn.main.css'))
    headers = {
           'parameters.id': 'ID',
           'parameters.image_file_name': 'img_file', 
           'parameters.created_on': 'created on',
           'parameters.verbose': 'verbose',
           'parameters.routes': 'actions',
          
           }
    
    fields = (db.parameters.id, db.parameters.image_file_name, db.parameters.created_on, db.parameters.verbose)

    par_table=SQLFORM.grid(db.parameters, details=False, headers=headers, fields=fields, links = 
       [lambda row: A('run',_href=URL("map",args=[row.id])), 
        lambda row: A('duplicate',_href=URL("duplicate_parameters",args=[row.id]))]) 

    return dict(table=par_table)

def update(ids):
    to_update=db(db.addresses.id.belongs(ids)).select()
    for record in to_update:
        if record.active==False:
            record.update_record(active=True)
        else:
            record.update_record(active=False)
    
def tables():
    return dict()  
        
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)



def show_parameters():
     this_page = db.parameters(request.args(0) or redirect(URL('parameters')))
     return dict(page=this_page)
    

def duplicate_parameters():
     row = db.parameters[request.args(0)]               # get current row 
     db.parameters.insert(image_file_name=row.image_file_name, image_file_store=row.image_file_store, 
     move_operator=row.move_operator, max_iterations = row.max_iterations, algorithm=row.algorithm, start_temp=row.start_temp, picture=row.picture, 
     alpha=row.row.alpha, verbose=row.verbose)
     return redirect(URL('manage'))


def rand_seq(size):
    '''generates values in random order
    equivalent to using shuffle in random,
    without generating all values at once'''
    values=range(size)
    for i in xrange(size):
        # pick a random index into remaining values
        j=i+int(random.random()*(size-i))
        # swap the values
        values[j],values[i]=values[i],values[j]
        # return the swapped value
        yield values[i] 

def all_pairs(size):
    '''generates all i,j pairs for i,j from 0-size'''
    for i in rand_seq(size):
        for j in rand_seq(size):
            yield (i,j)

def reversed_sections(tour):
    '''generator to return all possible variations where the section between two cities are swapped'''
    for i,j in all_pairs(len(tour)):
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour: # no point returning the same tour
                yield copy

def swapped_cities(tour):
    '''generator to create all possible variations where two cities have been swapped'''
    for i,j in all_pairs(len(tour)):
        if i < j:
            copy=tour[:]
            copy[i],copy[j]=tour[j],tour[i]
            yield copy

def cartesian_matrix(coords):
    '''create a distance matrix for the city coords that uses straight line distance'''
    from GoogleMaps import GoogleMaps
    gmaps = GoogleMaps('AIzaSyAVbFFRee1cluzDx2G3aTBvpmgeN1glxbI')
    
    matrix={}
    
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            x = str(x1)+', '+str(y1)
            y = str(x2)+', '+str(y2)
            dirs = gmaps.directions(x, y)                  
            distance  = dirs['Directions']['Distance']['meters']           # get distance in meters
            distance = round(distance/1609.344)                            # convert to miles   
            matrix[i,j]=distance
    return matrix
    
    '''
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy=x1-x2,y1-y2
            dist=sqrt(dx*dx + dy*dy)
            matrix[i,j]=dist
    return matrix
'''


def tour_length(matrix,tour):
    '''total up the total length of the tour based on the distance matrix'''
    total=0
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        total+=matrix[city_i,city_j]
    return total

def write_tour_to_img(coords,tour,title,img_file):
    padding=20
    # shift all coords in a bit
    coords=[(x+padding,y+padding) for (x,y) in coords]
    maxx,maxy=0,0
    for x,y in coords:
        maxx=max(x,maxx)
        maxy=max(y,maxy)
    maxx+=padding
    maxy+=padding
    img=Image.new("RGB",(int(maxx),int(maxy)),color=(255,255,255))
    
    font=ImageFont.load_default()
    d=ImageDraw.Draw(img);
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        x1,y1=coords[city_i]
        x2,y2=coords[city_j]
        d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
        d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))
    
    
    for x,y in coords:
        x,y=int(x),int(y)
        d.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill=(196,196,196))
    
    d.text((1,1),title,font=font,fill=(0,0,0))
    
    del d
    #response.headers['Content-Type']="image/png" 
    #img.save(response.body, "PNG") 
    #return response.body.getvalue()
    img.save(request.folder + 'static/' + 'image.png') 
    db.parameters[request.args(0)].update(image_file_store=(request.folder + 'static/' + 'image.png'))
    #img.save(img_file, "PNG")

def init_random_tour(tour_length):
   tour=range(tour_length)
   random.shuffle(tour)
   return tour

def run_hillclimb(init_function,move_operator,objective_function,max_iterations):
    from hillclimb import hillclimb_and_restart
    iterations,score,best=hillclimb_and_restart(init_function,move_operator,objective_function,max_iterations)
    return iterations,score,best

def run_anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha):
    if start_temp is None or alpha is None:
        usage();
        print "missing --cooling start_temp:alpha for annealing"
        sys.exit(1)
    #from sa import anneal
    iterations,score,best=anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha)
    return iterations,score,best

def usage():
    print "usage: python %s [-o <output image file>] [-v] [-m reversed_sections|swapped_cities] -n <max iterations> [-a hillclimb|anneal] [--cooling start_temp:alpha] <city file>" % sys.argv[0]

def download():
    return response.download(request, db)

def read_coords(i):
    data=[]
    row = db(db.routes).select().last()
    (filename, stream) = db.routes.route.retrieve(row.route)
    shutil.copyfileobj(stream,open(filename,'wb'))
    data = pickle.load(open(filename, 'rb'))
    
    
    coords=[]
    for row in data:
        x, y = row.split(',')
        coords.append((float(x),float(y)))
    return coords

def buildRoute():
    route=[]
    rows=db().select(db.addresses.ALL)
    route=getLatLng(rows)

            
    pickle.dump(route, open(request.folder + 'static/route.p', "wb" ) )
    #route_file = file(request.folder + 'static/route.p')
    try:
        stream=open(request.folder + 'static/route.p', 'rb')        
        db.routes.insert(route=db.routes.route.store(stream, 'route.p'), route_data=stream.read())
 
        return "success!" 
    except:
        return "Could not insert into db" 

def map():
    try:
        row = db.parameters[request.args(0)]
    except getopt.GetoptError:
        print "parameters could not be loaded."
        sys.exit(2)
    out_file_name="image.png"
    max_iterations=row.max_iterations
    verbose=row.verbose
    move_operator=row.move_operator
    run_algorithm="anneal"   
    start_temp,alpha=float(row.start_temp),float(row.alpha)
    

    if move_operator=="reversed_sections":
        move_operator = reversed_sections
    elif move_operator=="swapped_cities":
        move_operator=swapped_cities

    if run_algorithm == "hillclimb":
        run_algorithm=run_hillclimb
    elif run_algorithm == "anneal":
        # do this to pass start_temp and alpha to run_anneal
        def run_anneal_with_temp(init_function,move_operator,objective_function,max_iterations):
            return run_anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha)
        run_algorithm=run_anneal_with_temp
  
    
    if max_iterations is None:
        print usage();
        #sys.exit(2)
    
    if out_file_name and not out_file_name.endswith(".png"):
        usage()
        print "output image file name must end in .png"
        #sys.exit(1)
    
    
    # enable more verbose logging (if required) so we can see workings
    # of the algorithms
    import logging
    format='%(asctime)s %(levelname)s %(message)s'
    if verbose:
        logging.basicConfig(level=logging.INFO,format=format)
    else:
        logging.basicConfig(format=format)
    
    #get addresses
    #convert addresses to coordinates
    #use distance api to build distance matrix
    #send matrix to run_algorithm
    #return best route
    #new addresses = addresses[best[i]]
    

    addresses = db(db.addresses.active==True).select()
    
    coords=getLatLng(addresses)
    
    #coords=read_coords(request.args(0))
    init_function=lambda: init_random_tour(len(coords))
    matrix=cartesian_matrix(coords)
    objective_function=lambda tour: -tour_length(matrix,tour)
    
    logging.info('using move_operator: %s'%move_operator)
    
    iterations,score,best=run_algorithm(init_function,move_operator,objective_function,max_iterations)
    # output results
    
    #if out_file_name:
    #    write_tour_to_img(coords,best,'%f'%(score),file(out_file_name,'w'))
    
    locs=[]
    best_coords=[]
    encoded_coords=[]
    best_route=''
    for i in best:
        best_route = best_route + addresses[i].address +'| '
        locs.append(XML(response.json(addresses[i].address)))
        best_coords.append(coords[i])

    db.routes[14].update_record(best=best_route)
    
    encoder = gpolyencode.GPolyEncoder()
    encoded_coords=encoder.encode(best_coords)
    
    return dict(iterations=iterations, score=score, best=best, coords=best_coords, locs=locs, encoded_coords=encoded_coords)

def route():
    route=db.routes[14].best
    best_route=route.split('| ')
    locs=[]
    for route in best_route:
        locs.append(XML(response.json(route)))
    return dict(locs=locs)
        
def main(row):
    try:
        row = db.parameters[row]
    except getopt.GetoptError:
        print "parameters could not be loaded."
        sys.exit(2)
    out_file_name="image.png"
    max_iterations=row.max_iterations
    verbose=row.verbose
    move_operator=row.move_operator
    run_algorithm="anneal"   
    start_temp,alpha=float(row.start_temp),float(row.alpha)
    

    if move_operator=="reversed_sections":
        move_operator = reversed_sections
    elif move_operator=="swapped_cities":
        move_operator=swapped_cities

    if run_algorithm == "hillclimb":
        run_algorithm=run_hillclimb
    elif run_algorithm == "anneal":
        # do this to pass start_temp and alpha to run_anneal
        def run_anneal_with_temp(init_function,move_operator,objective_function,max_iterations):
            return run_anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha)
        run_algorithm=run_anneal_with_temp
  
    
    if max_iterations is None:
        print usage();
        #sys.exit(2)
    
    if out_file_name and not out_file_name.endswith(".png"):
        usage()
        print "output image file name must end in .png"
        #sys.exit(1)
    
    
    # enable more verbose logging (if required) so we can see workings
    # of the algorithms
    import logging
    format='%(asctime)s %(levelname)s %(message)s'
    if verbose:
        logging.basicConfig(level=logging.INFO,format=format)
    else:
        logging.basicConfig(format=format)
    
    # setup the things tsp specific parts hillclimb needs\
    coords=read_coords(request.args(0))
    init_function=lambda: init_random_tour(len(coords))
    matrix=cartesian_matrix(coords)
    objective_function=lambda tour: -tour_length(matrix,tour)
    
    logging.info('using move_operator: %s'%move_operator)
    
    iterations,score,best=run_algorithm(init_function,move_operator,objective_function,max_iterations)
    # output results
    
    if out_file_name:
        write_tour_to_img(coords,best,'%f'%(score),file(out_file_name,'w'))
    


    return dict(iterations=iterations, score=score, best=best, coords=coords, i=0)



if __name__ == "__main__":
    main()



###################sa.py#########################################################
import random
import math
import logging

def P(prev_score,next_score,temperature):
    if next_score > prev_score:
        return 1.0
    else:
        return math.exp( -abs(next_score-prev_score)/temperature )

class ObjectiveFunction:
    '''class to wrap an objective function and 
    keep track of the best solution evaluated'''
    def __init__(self,objective_function):
        self.objective_function=objective_function
        self.best=None
        self.best_score=None
    
    def __call__(self,solution):
        score=self.objective_function(solution)
        if self.best is None or score > self.best_score:
            self.best_score=score
            self.best=solution
            logging.info('new best score: %f',self.best_score)
        return score

def kirkpatrick_cooling(start_temp,alpha):
    T=start_temp
    while True:
        yield T
        T=alpha*T

def anneal(init_function,move_operator,objective_function,max_evaluations,start_temp,alpha):
    
    # wrap the objective function (so we record the best)
    objective_function=ObjectiveFunction(objective_function)
    
    current=init_function()
    current_score=objective_function(current)
    num_evaluations=1
    
    cooling_schedule=kirkpatrick_cooling(start_temp,alpha)
    
    logging.info('anneal started: score=%f',current_score)
    
    for temperature in cooling_schedule:
        done = False
        # examine moves around our current position
        for next in move_operator(current):
            if num_evaluations >= max_evaluations:
                done=True
                break
            
            next_score=objective_function(next)
            num_evaluations+=1
            
            # probablistically accept this solution
            # always accepting better solutions
            p=P(current_score,next_score,temperature)
            if random.random() < p:
                current=next
                current_score=next_score
                break
        # see if completely finished
        if done: break
    
    best_score=objective_function.best_score
    best=objective_function.best
    logging.info('final temperature: %f',temperature)
    logging.info('anneal finished: num_evaluations=%d, best_score=%f',num_evaluations,best_score)
    return (num_evaluations,best_score,best)

#################hillclimb.py####################################################################
import logging

def hillclimb(init_function,move_operator,objective_function,max_evaluations):
    '''
    hillclimb until either max_evaluations is reached or we are at a local optima
    '''
    best=init_function()
    best_score=objective_function(best)
    
    num_evaluations=1
    
    logging.info('hillclimb started: score=%f',best_score)
    
    while num_evaluations < max_evaluations:
        # examine moves around our current position
        move_made=False
        for next in move_operator(best):
            if num_evaluations >= max_evaluations:
                break
            
            # see if this move is better than the current
            next_score=objective_function(next)
            num_evaluations+=1
            if next_score > best_score:
                best=next
                best_score=next_score
                move_made=True
                break # depth first search
            
        if not move_made:
            break # we couldn't find a better move (must be at a local maximum)
    
    logging.info('hillclimb finished: num_evaluations=%d, best_score=%f',num_evaluations,best_score)
    return (num_evaluations,best_score,best)

def hillclimb_and_restart(init_function,move_operator,objective_function,max_evaluations):
    '''
    repeatedly hillclimb until max_evaluations is reached
    '''
    best=None
    best_score=0
    
    num_evaluations=0
    while num_evaluations < max_evaluations:
        remaining_evaluations=max_evaluations-num_evaluations
        
        logging.info('(re)starting hillclimb %d/%d remaining',remaining_evaluations,max_evaluations)
        evaluated,score,found=hillclimb(init_function,move_operator,objective_function,remaining_evaluations)
        
        num_evaluations+=evaluated
        if score > best_score or best is None:
            best_score=score
            best=found
        
    return (num_evaluations,best_score,best)
