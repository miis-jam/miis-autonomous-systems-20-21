;Header and description

(define (domain monkey-republic)

;remove requirements that are not needed
(:requirements :typing :negative-preconditions)

(:types
    monkey chair places
)

(:predicates
    (at-monkey ?p - places)         ;true if monkey is at place x
    (at-chair ?p - places)          ;true if chair is at place x
    (at-banana ?p - places)         ;true if banana is at place x
    (carry ?m - monkey ?c - chair)  ;true if monkey holds chair
)

(:action move
    :parameters (?from ?to - places)
    :precondition (at-monkey ?from)
    :effect (and (at-monkey ?to) (not (at-monkey ?from)))
)

(:action pick
    :parameters (?p - places ?c - chair ?m - monkey)
    :precondition (and (at-monkey ?p) (at-chair ?p))
    :effect (and (not (at-chair ?p)) (carry ?m ?c))
)

(:action drop
    :parameters (?p - places ?c - chair ?m - monkey)
    :precondition (and (carry ?m ?c) (at-monkey ?p))
    :effect (and (not (carry ?m ?c)) (at-chair ?p))
)

(:action eat
    :parameters (?p - places)
    :precondition (and (at-monkey ?p) (at-banana ?p) (at-chair ?p))
    :effect (not (at-banana ?p))
)

)