;Header and description 

(define (domain MonkeyDomain)

    ;remove requirements that are not needed
    (:requirements :strips :negative-preconditions)

    (:predicates
        (at ?x ?place) ; place of the subject or object in the world
        (agent ?x) ; indicates the agency
        (edible ?x) ; something that can be consumed (in this case bananas)
        (usable ?x) ; something that can be pushed or climbed as tool (chair, box)
        (eaten ?x) ; indicates if the food is eaten or not
        (high ?x) ; the height of the agent, high if it's climbed on the chair
    )

    (:functions ;todo: define numeric functions here

    )

    ;define actions here
    (:action go
        :parameters (?subject ?from ?to)
        :precondition (and 
        (at ?subject ?from) 
        (not (high ?subject)) 
        (agent ?subject)
        )
        :effect (and 
        (at ?subject ?to) 
        (not (at ?subject ?from))
        )
    )

    (:action climbUp
        :parameters (?subject ?object ?place)
        :precondition (and 
        (usable ?object) 
        (not (high ?subject)) 
        (at ?object ?place) 
        (at ?subject ?place) 
        (agent ?subject)
        )
        :effect (and 
        (not (usable ?object)) 
        (high ?subject)
        )
    )

    (:action climbDown
        :parameters (?subject ?object ?place)
        :precondition (and 
        (not (usable ?object)) 
        (high ?subject) 
        (agent ?subject)
        )
        :effect (and 
        (usable ?object) 
        (not (high ?subject))
        )
    )

    (:action push
        :parameters (?subject ?object ?from ?to)
        :precondition (and 
        (usable ?object) 
        (not (high ?subject)) 
        (at ?object ?from) 
        (at ?subject ?from) 
        (agent ?subject)
        )
        :effect (and 
        (at ?object ?to) 
        (at ?subject ?to) 
        (not (at ?object ?from)) 
        (not (at ?subject ?from))
        )
    )

    (:action eat
        :parameters (?subject ?object ?place)
        :precondition (and 
        (high ?subject) 
        (at ?object ?place) 
        (at ?subject ?place) 
        (not (eaten ?object)) 
        (edible ?object) 
        (agent ?subject)
        )
        :effect (and 
        (eaten ?object)
        )
    )
    

)
