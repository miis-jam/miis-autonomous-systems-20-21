(define (problem sokoban-easy) (:domain sokoban)
(:objects 
x0y0 x1y0 x2y0 x3y0 x4y0 x5y0 x6y0 x7y0 x8y0 
x0y1 x1y1 x2y1 x3y1 x4y1 x5y1 x6y1 x7y1 x8y1 
x0y2 x1y2 x2y2 x3y2 x4y2 x5y2 x6y2 x7y2 x8y2 
x0y3 x1y3 x2y3 x3y3 x4y3 x5y3 x6y3 x7y3 x8y3 
x0y4 x1y4 x2y4 x3y4 x4y4 x5y4 x6y4 x7y4 x8y4 
x0y5 x1y5 x2y5 x3y5 x4y5 x5y5 x6y5 x7y5 x8y5 
x0y6 x1y6 x2y6 x3y6 x4y6 x5y6 x6y6 x7y6 x8y6 
x0y7 x1y7 x2y7 x3y7 x4y7 x5y7 x6y7 x7y7 x8y7 
x0y8 x1y8 x2y8 x3y8 x4y8 x5y8 x6y8 x7y8 x8y8 
 - location
tele - teleporter
)

(:init 
(at-agent x4y4 )
(is-target x6y1 )
(is-target x6y2 )
(is-target x1y6 )
(is-target x2y6 )
(is-wall x4y0 )
(is-wall x3y1 )
(is-wall x4y6 )
(is-wall x8y0 )
(is-wall x0y2 )
(is-wall x8y3 )
(is-wall x0y5 )
(is-wall x2y2 )
(is-wall x1y0 )
(is-wall x8y6 )
(is-wall x0y8 )
(is-wall x1y3 )
(is-wall x2y8 )
(is-wall x7y4 )
(is-wall x7y7 )
(is-wall x6y5 )
(is-wall x6y8 )
(is-wall x5y0 )
(is-wall x5y6 )
(is-wall x4y8 )
(is-wall x8y2 )
(is-wall x0y1 )
(is-wall x0y7 )
(is-wall x0y4 )
(is-wall x7y0 )
(is-wall x1y8 )
(is-wall x6y4 )
(is-wall x6y7 )
(is-wall x7y6 )
(is-wall x3y2 )
(is-wall x4y1 )
(is-wall x4y7 )
(is-wall x3y8 )
(is-wall x5y5 )
(is-wall x8y4 )
(is-wall x8y1 )
(is-wall x1y1 )
(is-wall x2y0 )
(is-wall x1y4 )
(is-wall x0y6 )
(is-wall x2y3 )
(is-wall x6y0 )
(is-box x4y3 )
(is-box x2y5 )
(is-box x3y4 )
(is-box x5y2 )
;horizontal
(connected-h x5y1  x6y1 )
(connected-h x6y1  x7y1 )
(connected-h x6y1  x5y1 )
(connected-h x7y1  x6y1 )
(connected-h x4y2  x5y2 )
(connected-h x5y2  x6y2 )
(connected-h x5y2  x4y2 )
(connected-h x6y2  x7y2 )
(connected-h x6y2  x5y2 )
(connected-h x7y2  x6y2 )
(connected-h x3y3  x4y3 )
(connected-h x4y3  x5y3 )
(connected-h x4y3  x3y3 )
(connected-h x5y3  x6y3 )
(connected-h x5y3  x4y3 )
(connected-h x6y3  x7y3 )
(connected-h x6y3  x5y3 )
(connected-h x7y3  x6y3 )
(connected-h x2y4  x3y4 )
(connected-h x3y4  x4y4 )
(connected-h x3y4  x2y4 )
(connected-h x4y4  x5y4 )
(connected-h x4y4  x3y4 )
(connected-h x5y4  x4y4 )
(connected-h x1y5  x2y5 )
(connected-h x2y5  x3y5 )
(connected-h x2y5  x1y5 )
(connected-h x3y5  x4y5 )
(connected-h x3y5  x2y5 )
(connected-h x4y5  x3y5 )
(connected-h x7y5  x8y5 )
(connected-h x8y5  x7y5 )
(connected-h x1y6  x2y6 )
(connected-h x2y6  x3y6 )
(connected-h x2y6  x1y6 )
(connected-h x3y6  x2y6 )
(connected-h x1y7  x2y7 )
(connected-h x2y7  x3y7 )
(connected-h x2y7  x1y7 )
(connected-h x3y7  x2y7 )
(connected-h x7y8  x8y8 )
(connected-h x8y8  x7y8 )
;vertical
(connected-v x5y1  x5y2 )
(connected-v x6y1  x6y2 )
(connected-v x7y1  x7y2 )
(connected-v x4y2  x4y3 )
(connected-v x5y2  x5y1 )
(connected-v x5y2  x5y3 )
(connected-v x6y2  x6y1 )
(connected-v x6y2  x6y3 )
(connected-v x7y2  x7y1 )
(connected-v x7y2  x7y3 )
(connected-v x3y3  x3y4 )
(connected-v x4y3  x4y2 )
(connected-v x4y3  x4y4 )
(connected-v x5y3  x5y2 )
(connected-v x5y3  x5y4 )
(connected-v x6y3  x6y2 )
(connected-v x7y3  x7y2 )
(connected-v x2y4  x2y5 )
(connected-v x3y4  x3y3 )
(connected-v x3y4  x3y5 )
(connected-v x4y4  x4y3 )
(connected-v x4y4  x4y5 )
(connected-v x5y4  x5y3 )
(connected-v x1y5  x1y6 )
(connected-v x2y5  x2y4 )
(connected-v x2y5  x2y6 )
(connected-v x3y5  x3y4 )
(connected-v x3y5  x3y6 )
(connected-v x4y5  x4y4 )
(connected-v x1y6  x1y5 )
(connected-v x1y6  x1y7 )
(connected-v x2y6  x2y5 )
(connected-v x2y6  x2y7 )
(connected-v x3y6  x3y5 )
(connected-v x3y6  x3y7 )
(connected-v x1y7  x1y6 )
(connected-v x2y7  x2y6 )
(connected-v x3y7  x3y6 )
(connected-v x5y7  x5y8 )
(connected-v x8y7  x8y8 )
(connected-v x5y8  x5y7 )
(connected-v x8y8  x8y7 )
)

(:goal (and 
(target-satisfied x6y1 )
(target-satisfied x6y2 )
(target-satisfied x1y6 )
(target-satisfied x2y6 )
))
)