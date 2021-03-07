;Header and description

(define (domain SokobanDomain)

    ;remove requirements that are not needed
    (:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        place
        object
        agent
    )

    ; un-comment following line if constants are needed
    ;(:constants )

    (:predicates ;todo: define predicates here
        (free ?x - place)
        (box ?x - place)
        (goal ?x - place)
        (agent ?x - place)
        (adjacent-h ?x - place ?y - place)
        (adjacent-v ?x - place ?y - place)
        (teleported ?x - object)
        (goal-achieved ?x - place)
    )

    (:functions ;todo: define numeric functions here
    )

    (:action move-h
        :parameters (?from - place ?to - place)
        :precondition (and

            (agent ?from)
            (adjacent-h ?from ?to)
            (free ?to)

        )

        :effect (and

            (agent ?to)
            (not (agent ?from))
            (free ?from)
            (not (free ?to))

        )
    )

    (:action move-v
        :parameters (?from - place ?to - place)
        :precondition (and

            (agent ?from)
            (adjacent-v ?from ?to)
            (free ?to)

        )
        :effect (and

            (agent ?to)
            (not (agent ?from))
            (free ?from)
            (not (free ?to))

        )
    )

    (:action push-h
        :parameters (?subj - agent ?from - place ?to - place)
        :precondition (and

            (agent ?subj)
            (free ?to)
            (box ?from)
            (adjacent-h ?subj ?from)
            (adjacent-h ?from ?to)

        )

        :effect (and

            (agent ?from)
            (not (agent ?subj))
            (box ?to)
            (not (box ?from))
            (free ?subj)
            (not (free ?to))
            (when (goal ?to) (goal-achieved ?to))
            (when (goal ?from) (not (goal-achieved ?from)))

        )
    )

    (:action push-v
        :parameters (?subj - agent ?from - place ?to - place)
        :precondition (and

            (agent ?subj)
            (free ?to)
            (box ?from)
            (adjacent-v ?subj ?from)
            (adjacent-v ?from ?to)

        )

        :effect (and

            (agent ?from)
            (not (agent ?subj))
            (box ?to)
            (not (box ?from))
            (free ?subj)
            (not (free ?to))
            (when (goal ?to) (goal-achieved ?to))
            (when (goal ?from) (not (goal-achieved ?from)))

        )
    )

    (:action teleport
        :parameters (?teleporter - object ?from - place ?to - place)
        :precondition (and

            (agent ?from)
            (free ?to)
            (not (teleported ?teleporter))

        )

        :effect (and

            (agent ?to)
            (not (agent ?from))
            (free ?from)
            (teleported ?teleporter)

        )
    )

)
