;Header and description

(define (domain monkeyDomain)

    ;remove requirements that are not needed
    (:requirements :strips)

    ; un-comment following line if constants are needed
    ;(:constants )

    (:predicates ;todo: define predicates here
        (at ?what ?where)
        (eaten ?banana)
        (has ?who ?what)
        (takeable ?what)
        (alive ?who)
        (edible ?what)
    )

    ; (:functions ;todo: define numeric functions here
    ; )

    (:action move
        :parameters (?who ?from ?to)
        :precondition (and (at ?who ?from)
            (alive ?who)
        )
        :effect (and (not (at ?who ?from))
            (at ?who ?to))
    )

    (:action take
        :parameters (?who ?what ?where)
        :precondition (and (at ?what ?where)
            (at ?who ?where)
            (takeable ?what)
            (alive ?who)
        )
        :effect (and (has ?who ?what)
            (not (at ?what ?where))
        )
    )
    (:action eat
        :parameters (?who ?what ?where ?chair)
        :precondition (and (has ?who ?chair)
            (at ?who ?where)
            (at ?what ?where)
            (alive ?who)
            (edible ?what)

        )
        :effect (and (eaten ?what)
            (not (at ?what ?where))
        )
    )

)