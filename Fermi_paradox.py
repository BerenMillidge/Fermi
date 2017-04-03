from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

# In (-/when? Enrico Fermi asked a question: Where are all the aliens.
#a general explanation. He performed a Fermi calculation. Exlpain about this

#A bit later this general idea was formulated by Francis Drake as the Drake equation. The basic idea is simple. We take the factors we think are necessary for the development of life,
#we estimate their probabilities, we multiply those probabilities together and voila! we have estimated the probability of life occuring in the universe.
#The drake equation in its standard form is given below:
#do this, does Jupyter support Latex?
#Obviously some of the factors are debatable and others can be split into smaller sub factors, or coalesced into larger factors, but the basic point remains the same

# Here I'll use a slightly modified versoin of the drake equation, for interest. I've filled in the parameters with their best estimated values (some are more guesswork than others), so you can
#simply run the cell to see the results. It's also fun to play arodn with the values, so do that.

frac_stars_planets = 0.8
frac_stars_sunlike = 0.2
num_planets_per_star = 5
frac_habitable_planets = 0.025
frac_life_developing = 0.01
frac_multicellular_life = 1
frac_civilised_life =  0.00001

def drake_equation(num_stars, frac_stars_planets, frac_stars_sunlike, num_planets_per_star, frac_habitable_planets, frac_life_developing, frac_multicellular_life, frac_civilised_life):
    unicellular = num_stars*frac_stars_planets*frac_stars_sunlike*num_planets_per_star*frac_habitable_planets*frac_life_developing
    multicellular = unicellular*frac_multicellular_life
    civilisations = multicellular*frac_civilised_life
    return unicellular, multicellular, civilisations

stars_in_universe =1e24
num_aliens_universe = drake_equation(stars_in_universe, frac_stars_planets,frac_stars_sunlike, num_planets_per_star, frac_habitable_planets, frac_life_developing, frac_multicellular_life, frac_habitable_planets)
print("In the whole universe there are:" , str(int(num_aliens_universe[0])) , "unicellular life forms," , str(int(num_aliens_universe[1])) , "multicellular life forms, and " , str(int(num_aliens_universe[2])) , "alien civilisations.")

stars_in_galaxy = 1e11
num_aliens_galaxy = drake_equation(stars_in_galaxy, frac_stars_planets, frac_stars_sunlike, num_planets_per_star, frac_habitable_planets, frac_life_developing, frac_multicellular_life, frac_habitable_planets)
print("In the galaxy there are:" , str(int(num_aliens_galaxy[0])) , "unicellular life forms," , str(int(num_aliens_galaxy[1])) , "multicellular life forms, and " , str(int(num_aliens_galaxy[2])) , "alien civilisations.")

stars_in_5000LY = 6e8
num_aliens_5000LY = drake_equation(stars_in_5000LY, frac_stars_planets, frac_stars_sunlike, num_planets_per_star, frac_habitable_planets, frac_life_developing, frac_multicellular_life, frac_habitable_planets)
print("In the closest 5000 light years there are:" , str(int(num_aliens_5000LY[0])) , "unicellular life forms," + str(int(num_aliens_5000LY[1])) , "multicellular life forms, and " , str(int(num_aliens_5000LY[2])) , "alien civilisations.")

#let's think about how this isgoign to work. We're going to have a simple "statistical galaxy". We'll run it for, say, 10 billion years. We don't know much about when the first stars started forming.
#We've also got to figure out how to express star formation rate, which is probably quite hard to do. We'll likely do it as a really simple exponential imho, because that seems like an easy model
#each star formation rate adds to the number of stars so we see what's up there. At some point we should add a star death rate, but I'm not sure how we'll do that, so we'll start with a simple model first
# we could do the stellar death rate with just a pretty simple lack of exponential hanging around, which should be fairly easy imho. Then we'll figure out the time intervals to make it seem reasonabel
#I'm pretty happy thinking that I could have already "solved" the fermi paradox by adding time, that seems fairly reasonable imho. Ironically, I think we just solved the fermi paradox right here. I'm n
#not sure how closely we should model star formation and death imho. That seems a bit weird. we can chuck in this kind of things for a while if we want, but to be honest, and it would be quite cool to do so
#we cuold also chuck in a huge number of things. I'm not even sure. If we do 1million year step sizes, then it would be unfortunate but that would reduce the number of steps we have to do by 10
#doing 1 million steps is pretty unfortunate though, and cuold take a while, even if computers are fast. A big problem is that we need a good way to simulate time lags, and currently we don't have 1
#like we can't keep track of all these stars at once, so we can't assign each one a thing, a label. So we've got to lag it. Basically we one way to do it would be to have the frac_habitable itself follow
#an exponential distribution. I'm really not sure how to slow down the rate of things We need reasonable exponential wiles imo. and this is pretty annoying. Like I'm not sure how to get the correct amount
#of stars forming, and how many dying either. We can still make a pretty smiple model most likely as a first step! # we cuold just have a tiny percentage probability ofdeath. that seems reasonable overall
# also seriously, we can actually figure out this equation imho if we're smart, AND we know the initial conditions rate. otherwise we havetoo many variables!

def exp(alpha, tau):
    return 1- np.exp(-1*alpha*tau)

def simulate_galaxy(frac_stars_planets, frac_stars_sunlike, num_planets_per_star, frac_habitable_planets, frac_life_developing, frac_multicellular_life, frac_civilised_life):
    timespan = 1e9 # i.e. ten billion years(!)
    step = 10000 # that means we'll still have to do tenthousand steps. ugh lol! We
    epochs = int(timespan / step)
    print(epochs)
    current_stars = 1e10
    star_birth_rate = 5.78e-6
    star_death_rate = 3.783e-6
    world_habitability_rate = 1.8e-5
    #frac_life = frac_life_developing/epochs
    frac_multicellular = frac_multicellular_life/epochs
    frac_civilisation  =frac_civilised_life/epochs


    unicellulars = [0]
    multicellulars = [0]
    civilisations = [0]
    epochs_list = [0]
    worlds = [0]
    civs = [0]
    for i in range(epochs):
        current_stars += (7*step)*exp(star_birth_rate, i)
        current_stars -= current_stars*0.0001*exp(star_death_rate, i)
        frac_habitable = frac_habitable_planets * exp(world_habitability_rate, i)
        num_worlds = current_stars*frac_stars_planets*num_planets_per_star* frac_stars_sunlike*frac_habitable # -(num_unicellular+num_mulicellular_ + num_civilisation)
        #worlds.append(num_worlds)
        num_unicellular = unicellulars[i-1] + frac_life_developing*num_worlds #- multicellulars[i-1]
        num_multicellular =multicellulars[i-1] + frac_multicellular*num_unicellular #- civilisations[i-1]
        num_civilisations = frac_civilisation * num_multicellular
        unicellulars.append(num_unicellular- num_multicellular)
        multicellulars.append(num_multicellular - - num_civilisations)
        civilisations.append(num_civilisations)
        civs.append(np.random.poisson(num_civilisations))
        epochs_list.append(i)

    #print(len(epochs_list))
    #print(len(num_civilisations))
    plt.plot(epochs_list, civs)
    plt.show()

simulate_galaxy(frac_stars_planets, frac_stars_sunlike, num_planets_per_star, frac_habitable_planets, frac_life_developing, frac_multicellular_life, frac_civilised_life)


## okay, we've actually got quite an interesting model here, esp. with our poisson and various other variables. It does take a long time to run for 100 billion years,




def plot(n, alpha):
    axes = []
    vals = []
    for i in range(n):
        axes.append(i)
        val = exp(alpha, i)
        vals.append(val)
    plt.plot(axes,vals)
    plt.show()

#plot(800000, 1.76e-5)