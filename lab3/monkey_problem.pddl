(define (problem MonkeyProblem)
    (:domain MonkeyDomain)
    (:objects
        monkey 
        banana-1 
        banana-2 
        banana-3
        chair 
        sq-1-1 
        sq-1-2 
        sq-1-3 
        sq-2-1 
        sq-2-2 
        sq-2-3 
        sq-3-1 
        sq-3-2 
        sq-3-3
    )

    (:init
        (at monkey sq-1-1)
        (at banana-1 sq-3-1)
        (at banana-2 sq-1-2)
        (at banana-3 sq-1-3)
        (at chair sq-3-1)
        (usable chair)
        (agent monkey)
        (edible banana-1)
        (edible banana-2)
        (edible banana-3)
        (high banana-1)
        (high banana-2)
        (high banana-3)
    )

    (:goal
        (and
            (eaten banana-1)
            (eaten banana-2)
            (eaten banana-3)
        )
    )

    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))


    ; Answer:
    ; (go monkey sq-1-1 sq-3-1)
    ; (climbup monkey chair sq-3-1)
    ; (eat monkey banana-1 sq-3-1)
    ; (climbdown monkey monkey sq-3-3)
    ; (push monkey monkey sq-3-1 sq-1-3)
    ; (climbup monkey monkey sq-1-3)
    ; (eat monkey banana-3 sq-1-3)
    ; (climbdown monkey monkey sq-3-3)
    ; (push monkey monkey sq-1-3 sq-1-2)
    ; (climbup monkey monkey sq-1-2)
    ; (eat monkey banana-2 sq-1-2)
)
