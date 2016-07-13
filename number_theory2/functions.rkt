#lang scheme
(require srfi/1)
(require "general.rkt")

; https://en.wikipedia.org/wiki/Iverson_bracket
; #t -> 1 and #f -> 0
(define (iverson s) (if s 1 0))

(define (sum list1) (fold + 0 list1))
(assert "Sum" (= 55 (sum (rangei 1 10))))
(assert "Empty sum" (= 0 (sum '())))

(define (indicator set) (lambda (x) (iverson (contains set x))))
(assert "Positive indicator" (= 1 ((indicator '(1 2)) 2)))
(assert "Negative indicator" (= 0 ((indicator '(1 2)) 3)))

; The following function tests to see if two functions are equal for the
; first 100 natural numbers
(define (fun= f g) (list==
	(map f (range 1 100))
	(map g (range 1 100))))
(assert "Function equals"
	(fun= (indicator '(3)) (lambda (x) (iverson (= x 3)))))

(define intersection ((curry lset-intersection) equal?))
(assert "Intersection" (list== '(1 3) (intersection (range 1 6) '(0 1 3))))

(define seteq ((curry lset=) equal?))
(define subseteq ((curry lset<=) equal?))
(define subset (lambda args (and
	(apply subseteq args)
	(not (apply seteq args)))))
(define superseteq (rev-args subseteq))
(define superset (rev-args subset))
(assert "Superseteq 1" (superseteq '(1 2 3) '(1 2)))
(assert "Superseteq 2" (superseteq '(1 2 3) '(1 2 3)))
(assert "Not superseteq" (not (superseteq '(1 2 3) '(1 2 3 4))))
(assert "Superset" (superset '(1 2 3) '(1 2)))
(assert "Not superset" (not (superset '(1 2 3) '(1 2 3))))

(provide iverson sum indicator fun= intersection subseteq subset superseteq
	superset seteq)
