;Header and description

(define (domain TeleportingSokobanDomainWithoutTyping)

    ;remove requirements that are not needed
    (:requirements :strips :equality :adl)

    ; un-comment following line if constants are needed
    ;(:constants )

    (:predicates ;todo: define predicates here
        (at ?what ?where)
        (adj_horizontal ?sq1 ?sq2)
        (adj_vertical ?sq1 ?sq2)
        (pushable ?what)
        (alive ?who)
        (occupied ?sq) ;there is a box in the square
        (teleport_avaliable ?who)
    )

    ; (:functions ;todo: define numeric functions here
    ; )

    (:action move_horizontal
        :parameters (?who ?from ?to)
        :precondition (and
            (at ?who ?from)
            (adj_horizontal ?from ?to)
            (not (occupied ?to))
            (alive ?who)
        )
        :effect (and
            (at ?who ?to)
            (not (at ?who ?from))

        )
    )
    (:action move_vertical
        :parameters (?who ?from ?to)
        :precondition (and
            (at ?who ?from)
            (adj_vertical ?from ?to)
            (not (occupied ?to))
            (alive ?who)
        )
        :effect (and
            (at ?who ?to)
            (not (at ?who ?from))

        )
    )

    (:action push_horizontal
        :parameters (?who ?what ?where_who ?where_what ?to)
        :precondition (and
            (at ?who ?where_who)
            (at ?what ?where_what)
            (adj_horizontal ?where_who ?where_what)
            (adj_horizontal ?where_what ?to)
            (not (= ?where_who ?to))
            (pushable ?what)
            (not (occupied ?to))
            (alive ?who)
            (occupied ?where_what)
        )
        :effect (and
            (at ?who ?where_what)
            (at ?what ?to)
            (not (occupied ?where_what))
            (not (at ?who ?where_who))
            (not (at ?what ?where_what))
            (occupied ?to)
        )
    )
    (:action push_vertical
        :parameters (?who ?what ?where_who ?where_what ?to)
        :precondition (and
            (at ?who ?where_who)
            (at ?what ?where_what)
            (adj_vertical ?where_who ?where_what)
            (adj_vertical ?where_what ?to)
            (not (= ?where_who ?to))
            (pushable ?what)
            (not (occupied ?to))
            (alive ?who)
            (occupied ?where_what)
        )
        :effect (and
            (at ?who ?where_what)
            (at ?what ?to)
            (not (occupied ?where_what))
            (not (at ?who ?where_who))
            (not (at ?what ?where_what))
            (occupied ?to)
        )
    )
    (:action teleport
        :parameters (?who ?from ?to)
        :precondition (and
            (teleport_avaliable ?who)
            (alive ?who)
            (at ?who ?from)
            (not (occupied ?to))

        )
        :effect (and
            (at ?who ?to)
            (not (at ?who ?from))
            (not (teleport_avaliable ?who))
        )
    )

)