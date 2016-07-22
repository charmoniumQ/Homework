(module functions racket/base
	(require srfi/1)
	(require "racketspecific.rkt")
	(require "general.rkt")

	(module+ test (require rackunit))

	; https://en.wikipedia.org/wiki/Iverson_bracket
	; #t -> 1 and #f -> 0
	(define (iverson s) (if s 1 0))

	(define (sum list1) (fold + 0 list1))
	(module+ test (check-eqv? 55 (sum (rangei 1 10))))
	(module+ test (check-eqv? 0 (sum '())))

	(define (indicator set) (lambda (x) (iverson (contains set x))))
	(module+ test (check-eqv? 1 ((indicator '(1 2)) 2)))
	(module+ test (check-eqv? 0 ((indicator '(1 2)) 3)))

	; The following function tests to see if two functions are equal for the
	; first 1000 natural numbers
	(define (fun= f g)
		(list= =
			(map f (rangei 1 1000))
			(map g (rangei 1 1000))))
	(module+ test (check-true
		(fun= (indicator '(3)) (lambda (x) (iverson (= x 3))))))

	(define intersection (curry lset-intersection equal?))
	(module+ test (check-true
		(list==
			'(1 3)
			(intersection (rangei 1 6) '(0 1 3)))))

	(define seteq (curry lset= =))
	(define subseteq (curry lset<= =))
	(define subset
		(lambda args
			(and
				(apply subseteq args)
				(not (apply seteq args)))))
	(define superseteq (rev-args subseteq))
	(define superset (rev-args subset))
	(module+ test (check-true (superseteq '(1 2 3) '(1 2))))
	(module+ test (check-true (superseteq '(1 2 3) '(1 2 3))))
	(module+ test (check-false (superseteq '(1 2 3) '(1 2 3 4))))
	(module+ test (check-true (superset '(1 2 3) '(1 2))))
	(module+ test (check-false (superset '(1 2 3) '(1 2 3))))

	(define (sorted-set-intersection seta setb)
		(define (loop seta setb acc)
			(if (or (empty? seta) (empty? setb))
				acc
				(if (< (car seta) (car setb))
					(loop (cdr seta) setb acc)
					(if (> (car seta) (car setb))
						(loop seta (cdr setb) acc)
						(loop (cdr seta) (cdr setb)
								(append acc (list (car seta))))))))
		(loop seta setb '()))

	(module+ test (check-true (list==
		(sorted-set-intersection '(1 2 3) '(1 3 4))
		'(1 3))))

	(provide iverson sum indicator fun= intersection subseteq subset superseteq
		superset seteq cartesian-product sorted-set-intersection)
)
