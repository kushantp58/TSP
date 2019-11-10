########## importing useful libraries #########
import math
import sys
import time
import random
import matplotlib.pyplot as plt

file_change = 1 ##### set to 1 for checking soulutions for 36 cities......
number_of_iterations = 20  ### set to the number of iterations you want to use for the simulated annealing.
plot = 1 ### set plot to 1 if you want to view detailed plot of travelling salesman's path            
coolingfactor    = float(.99) ### set the cooling factor to .99 by default...change it according to your needs
temperaturestart = float(1e+90) ### set the start temperature ..change it according to your needs
temperatureend   = float(.1) #### set the stopping temperature....change it according to your needs

#########  filename to be searched for #######
if(file_change ==1):
    file = "E:\\intro_to_ai\\Assignments\\randTSP\\problem36" ##replace with the file you want to check
else:
    file = "E:\\intro_to_ai\\Assignments\\randTSP\\16\\instance_10.txt" ### you can replace the file with which you want for checking your tsp....
places_pair = []

######### get the list of places from the csv files ###############
def io_file():
    file_path = file  #for testing the inputs change the path in which you have files
    l = []
    with open(file_path) as f:
        for line in f:
            l.append(line.strip().split(' '))
            for i in range(len(l)):
                if(i==0):
                    a = l[i]
    a = [int(i) for i in a]
    n = a[0]
    places = [place(r[0],i,float(r[1]),float(r[2]))for i, r in enumerate(l[1:])]
    return places

        



######## defining a class for a place/location/place with the values of lattitude and longitude ########
class place:
    def __init__(self,name=" ",i=0,lat=0,long=0):
        self.name = name
        self.i = i # for determining position
        self.lat = lat
        self.long = long
        
    ### for informal string display ###
    def __str__(self):
        return '%s %d %f %f' % (self.name, self.i,self.lat, self.long)    
    
    #### for official string display ####
    def __repr__(self):
        return self.__str__()
    
    ### using euclidean distance for finding the distance #### 
    def euc_dist(self,place):
        lat = float(self.lat - place.lat)
        long = float(self.long -place.long)
        d = math.sqrt(pow(lat,2)+pow(long,2))
        print(d)
        return d
    
    def euc_dist_km(self,place):
        global places_pair
        if self.i != place.i:
            k = [self.i,place.i]
            return places_pair[max(k)][min(k)]
        return 0
    
def places_dist_pair(places):
    global places_pair
    for s in places:
        places_pair.append([0 for r in range(s.i)])
        for d in places[:s.i]:
            places_pair[s.i][d.i] = s.euc_dist(d)

def final_kms(places):
    kms = [places[i].euc_dist_km(places[(i+1) % len(places)])for i in range(len(places))]
    print(sum(kms))
    return sum(kms)

# def final_kms1(places):
#     kms = [places[13].euc_dist_km(places[(14) % len(places)])for i in range(len(places))]
#     print(sum(kms))
#     return sum(kms)
    
    
def pmap(places,fid):
    fmap = plt.figure(fid)
    amap = fmap.add_subplot(111)

    places_x = [place.long for place in places + [places[0]]]
    places_y = [place.lat for place in places + [places[0]]]

    link = '-'
    amap.plot(places_x,places_y,'go'+link)
    amap.grid()
    gaps = math.fabs(min(places_x)-max(places_x))* .1
    amap.set_xlim(min(places_x)-gaps,max(places_x)+gaps*3)
    amap.set_ylim(min(places_y)-gaps,max(places_y)+gaps)

    for i , place in enumerate(places):
        amap.text(place.long,
                 place.lat,
                '%d: %s' % (i + 1, place.name),
                withdash = False,
                   )
    return amap
    
def dplot(dcurr,fid,dbest,ids_iteration,n_places,n_iterations,cfactor,tstart,tend):
        fdist = plt.figure(fid)
        adist = fdist.add_subplot(111)
        lcurr = adist.plot(dcurr,linewidth=1)
        lbest = adist.plot(dbest,'r',linewidth=2)
        print(type(n_iterations))
        adist.set_title('Simulated annealing for %d cities on %d iteration(s)\nc_factor: %.4f, t_start: %g, t_end: %.4f' % (n_places, len(n_iterations), cfactor, tstart, tend))

        l  = None
        for step in ids_iteration[:-1]:
            y_min = min(dcurr)
            y_max = max(dcurr)
            l = adist.plot([step,step],[y_max,y_min],'g',linewidth=2)
            
            adist.set_xlabel('Number of step(s)')
            adist.set_ylabel('Distance in kms')
            
            i_legend = 3 if len(ids_iteration) > 1 else 2
            plt.legend( (lcurr, lbest, l)[:i_legend],('Tested distance', 'Shortest distance', 'Restart')[:i_legend],loc='upper right' )     
def comput_swap_i(i,n_places):
    i_prev = (i-1+n_places)% n_places
    i_nxt  = (i+1) % n_places
    return(i_prev,i_nxt)


def swap_dist(places,i_a,i_b):
    i_a = min(i_a,i_b)
    i_b = max(i_a,i_b)
    (i_a_prev,i_a_next) = comput_swap_i(i_a,len(places))
    (i_b_prev,i_b_next) = comput_swap_i(i_b,len(places))
    
    dist = [ ]
    dist.append(places[i_a_prev].euc_dist_km(places[i_a]))
    dist.append(places[i_b].euc_dist_km(places[i_b_next]))
    if i_a == i_b_prev:
        dist.append(places[i_a].euc_dist_km(places[i_b]))
        
    else:
        dist.append(places[i_a].euc_dist_km(places[i_a_next]))
        dist.append(places[i_b_prev].euc_dist_km(places[i_b]))
        
    return sum(dist)

#### algorithm #####

def s_ann(places, t_start=1.0e+300, t_end=.1, cf=.99, nb_i=1):

    places_best = places[:]
    d_best = final_kms(places_best)

    d_curr = []
    dst_best = []
    ids_i = []

    
    for i in range(nb_i):

        t = t_start
        places_curr = places_best[:]
        dst_curr = d_best
        dst_new = d_best
        places_new = places_best[:]

        step = 0
        while t > t_end:

            index = random.sample(range(len(places_new) - 1), 2)
            index[0] += 1
            index[1] += 1

            bf_swap = swap_dist(places_new, index[0], index[1])
            places_new[index[0]], places_new[index[1]] = places_new[index[1]], places_new[index[0]]
            af_swap = swap_dist(places_new, index[0], index[1])

            dst_new = dst_new - bf_swap + af_swap

            diff = dst_new - dst_curr
            if diff < 0 or  math.exp( -diff / t ) > random.random():
                places_curr = places_new[:]
                dst_curr = dst_new
            else:
                dst_new = dst_curr
                places_new = places_curr[:]

            if dst_curr < d_best:
                places_best = places_curr[:]
                d_best = dst_curr

            if True:
                d_curr.append(dst_curr)
                dst_best.append(d_best)
            t = t * cf
            step = step + 1

        ids_i.append(len(d_curr))

    return places_best, d_curr, dst_best, ids_i


if(__name__ == "__main__"):

    #plot = 'plot'           
    nb_iterations     = number_of_iterations
    nb_places         = -1 
    cf    = coolingfactor
    tp_start = temperaturestart
    tp_end   = temperatureend
    print("starting the time for calculation of solution......\n")
    t_start = time.time()
    places = io_file()
    print(places)
    places_dist_pair(places)
    nb_places = len(places) if nb_places <= 0 else nb_places
    
    places = places[:nb_places]
    print("Done with the calculation.......Wait for some time to observe the results for different temperature and cooling factor values.....")
    (places_new,dst_curr,dst_best,ids_i) = s_ann(places,tp_start,tp_end,cf,nb_iterations)
    t_end = time.time()
    print("places_new:",places_new)
    dst_start = final_kms(places)
    dst_end = final_kms(places_new)
    print('Improvement:          %8.0f %%'  % (100 * (dst_start - dst_end) / dst_start))
    print('Time:                 %8.0f sec' % (t_end - t_start))
    print('Initial distance:     %8.0f km'  % dst_start)
    print('Optimal distance:     %8.0f km'  % dst_end)

    amap = pmap(places, 1)
    amap.set_title('Initial tour on %d places\nDistance: %.0f km' % (len(places), dst_start))

    if nb_iterations:
        amap = pmap(places_new, 2)
        amap.set_title('Optimal tour on %d places\nDistance: %.0f km on %d iteration(s)' % (len(places), dst_end, nb_iterations))
        dplot(dst_curr, 3, dst_best, ids_i, len(places), ids_i,cf, tp_start, tp_end)

    if plot ==1:
        plt.show()
