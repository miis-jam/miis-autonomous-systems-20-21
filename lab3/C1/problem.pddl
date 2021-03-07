(define (problem get-bananas) (:domain monkey-republic)
(:objects 
    m1 - monkey
    c - chair
    p1 p2 p3 p4 - places
)

(:init
    (at-monkey p1)
    (at-banana p1)
    (at-banana p2)
    (at-banana p3)
    (at-chair p4)
)

(:goal (and
    (not (at-banana p1))
    (not (at-banana p2))
    (not (at-banana p3))
))

)