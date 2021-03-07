;Author:    J. Fischer
;Date:      06.03.21

(define (domain sokoban)

;remove requirements that are not needed
(:requirements :typing :conditional-effects :negative-preconditions :equality)

(:types 
    location
    teleporter
)

(:predicates
    (is-wall ?l - location)
    
    (is-box ?l - location)

    (is-target ?l - location)
    
    (at-agent ?l - location)
    
    (target-satisfied ?l - location)

    (connected-h ?l1 ?l2 - location)
    (connected-v ?l1 ?l2 - location)

    (teleported-once ?t - teleporter)
)

(:action move-horizontal
    :parameters (?from ?to - location)
    :precondition   (and 
                        (at-agent ?from)
                        (not (is-wall ?to))
                        (not (is-box ?to))
                        (connected-h ?from ?to)
                    )
    :effect (and 
                (at-agent ?to)
                (not (at-agent ?from))
                ;(when (is-target ?to) (target-satisfied ?to))
            )
)

(:action move-vertical
    :parameters (?from ?to - location)
    :precondition   (and 
                        (at-agent ?from)
                        (not (is-wall ?to))
                        (not (is-box ?to))
                        (connected-v ?from ?to)
                    )
    :effect (and 
                (at-agent ?to)
                (not (at-agent ?from))
                ;(when (is-target ?to) (target-satisfied ?to))
            )
)

(:action move-box-vertical
    :parameters (?agentPos ?from ?to - location)
    :precondition (and 
                    (at-agent ?agentPos)
                    (not (is-wall ?from))
                    (not (is-wall ?to))
                    (is-box ?from)
                    (not (is-box ?to))
                    (connected-v ?agentPos ?from)
                    (connected-v ?from ?to)
                    (not (= ?agentPos ?to))
                 )
    :effect (and 
                ;move agent
                (not (at-agent ?agentPos))
                (at-agent ?from)
                ;move box
                (not (is-box ?from))
                (is-box ?to)
                ;check if target
                (when (is-target ?to) (target-satisfied ?to))
                (when (is-target ?from) (not (target-satisfied ?from)))
            )
)

(:action move-box-horizontal
    :parameters (?agentPos ?from ?to - location)
    :precondition (and 
                    (at-agent ?agentPos)
                    (not (is-wall ?from))
                    (not (is-wall ?to))
                    (is-box ?from)
                    (not (is-box ?to))
                    (connected-h ?agentPos ?from)
                    (connected-h ?from ?to)
                    (not (= ?agentPos ?to))
                 )
    :effect (and 
                ;move agent
                (not (at-agent ?agentPos))
                (at-agent ?from)
                ;move box
                (not (is-box ?from))
                (is-box ?to)
                ;check if target
                (when (is-target ?to) (target-satisfied ?to))
                (when (is-target ?from) (not (target-satisfied ?from)))
            )
)

(:action teleport
    :parameters (?from ?to - location ?t - teleporter)
    :precondition (and 
                    (at-agent ?from)
                    (not (is-wall ?to))
                    (not (is-box ?to))
                    (not (teleported-once ?t))
                    )
    :effect (and 
                (at-agent ?to)
                (not (at-agent ?from))
                (teleported-once ?t))
)

)