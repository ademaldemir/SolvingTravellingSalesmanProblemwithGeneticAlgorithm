from RouteManager import RouteManager
from Route import Route
import math
import random
import numpy as np



class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.015, tournament_size=5, elitism=True):
        #GA parameters
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism
        
        
    # Evolves a population over one generation
    def evolve(self, routes):
        
        newPop = RouteManager(self.cities, routes.__len__())
        
        # Keep our best individual if elitism is enabled
        elitismBalance = 0    
        if self.elitism:
            newPop.set_route(0, routes.find_best_route())
            elitismBalance = 1


        # Crossover population
        # Loop over the new population's size and create individuals from
        # Current population
        for i in range(elitismBalance, newPop.__len__()):
            # Select routes
            route_1 = self.tournament(routes)
            route_2 = self.tournament(routes)
            # Crossover routes
            altered = self.crossover(route_1, route_2)
            # Add altered to new population
            newPop.set_route(i, altered)

        # Mutate the new population a bit to add some new genetic material
        for i in range(elitismBalance, newPop.__len__()):
            self.mutate(newPop.get_route(i))
         
        return newPop


    # Applies crossover to a set of parents and creates offspring
    def crossover(self, route_1, route_2): 
        # Create new child named altered
        altered = Route(self.cities)

        # Get start and end sub altered points for route_1's route
        firstPoint = int(random.random() * route_1.__len__())
        secondPoint = int(random.random() * route_1.__len__())
      
        # Loop and add the sub route from route_1 to our child
        for i in range(0, altered.__len__()):
            # If our first point is less than the second point
            if firstPoint < secondPoint and i > firstPoint and i < secondPoint:
                altered.assign_city(i, route_1.get_city(i))
            
            # If our first point is larger
            elif firstPoint > secondPoint:
                if not (i < firstPoint and i > secondPoint):
                    altered.assign_city(i, route_1.get_city(i))

        # Loop through route_2's city route
        for i in range(0, route_2.__len__()):
            # If altered doesn't have the city add it
            if not altered.__contains__(route_2.get_city(i)):
                # Loop to find a spare point in the altered's tour
                for ii in range(0, altered.__len__()):
                    # Spare point found, add city
                    if altered.get_city(ii) == None:
                        altered.assign_city(ii, route_2.get_city(i))
                        break
      
        return altered
        
        
    # Mutate a route using swap mutation
    def mutate(self, route):
        # Loop through route cities
        for routePoint1 in range(0, route.__len__()):
            # Apply mutation rate
            if random.random() < self.mutation_rate:
                # Get a second random point in the route
                routePoint2 = int(route.__len__() * random.random())
                
                # Get the cities at target point in route
                city1 = route.get_city(routePoint1)
                city2 = route.get_city(routePoint2)
                
                # Swap them around
                route.assign_city(routePoint2, city1)
                route.assign_city(routePoint1, city2)

        
    # Selects candidate routes for crossover
    def tournament(self, routes): 
        # Create a tournament population
        tournament = RouteManager(self.cities, self.tournament_size)
        # For each place in the tournament get a random candidate routes and
        # add it 
        for i in range(0, self.tournament_size):
            haphazardId = int(random.random() * routes.__len__())
            tournament.set_route(i, routes.get_route(haphazardId))
        # Get the appropriate routes
        appropriate = tournament.find_best_route()
        return appropriate