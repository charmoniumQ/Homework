(module functions-sets racket/base
	(require srfi/1)
	(require anaphoric) ; TODO: fix this
	(require "racketspecific.rkt")

	(module+ test (require rackunit))

	; Home on the range
	(define (range start stop) (iota (- stop start) start 1))

	; i for inclusive
	(define (rangei start stop) (iota (+ 1 (- stop start)) start 1))
	(module+ test
		(check-equal? '(1 2 3 4) (rangei 1 4)))

	(define (rev-args f) (lambda args (apply f (reverse args))))
	(module+ test
		(check-eqv? 1 ((rev-args -) 2 3)))

	; https://en.wikipedia.org/wiki/Iverson_bracket
	; #t -> 1 and #f -> 0
	(define (iverson s) (if s 1 0))

	(define (sum list1) (fold + 0 list1))
	(module+ test (check-equal? 55 (sum (rangei 1 10))))
	(module+ test (check-equal? 0 (sum '())))

	(define (indicator set) (lambda (x) (iverson (member x set))))
	(module+ test (check-equal? 1 ((indicator '(1 2)) 2)))
	(module+ test (check-equal? 0 ((indicator '(1 2)) 3)))

	; The following function tests to see if two functions are equal for the
	; first 1000 natural numbers
	(define (fun= f g [domain (rangei 1 1000)])
		(list= =
			(map f domain)
			(map g domain)))
	(module+ test (check-true
		(fun= (indicator '(3)) (lambda (x) (iverson (= x 3))))))

	(define intersection (curry lset-intersection equal?))
	(module+ test (check-equal?
		'(1 3)
		(intersection (rangei 1 6) '(0 1 3))))

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
			(if (or (null? seta) (null? setb))
				acc
				(if (< (car seta) (car setb))
					(loop (cdr seta) setb acc)
					(if (> (car seta) (car setb))
						(loop seta (cdr setb) acc)
						(loop (cdr seta) (cdr setb)
								(append acc (list (car seta))))))))
		(loop seta setb '()))

	(module+ test (check-equal?
		(sorted-set-intersection '(1 2 3) '(1 3 4))
		'(1 3)))

	; Like powerset, but for https://en.wikipedia.org/wiki/Multiset
	(define (power-multiset multiset)
		(if (null? multiset)
			'(())
			(append (power-multiset (cdr multiset)) (append-map (lambda (initial)
				(map (lambda (rest)
					(cons (list (first (car multiset)) initial) rest))
					(power-multiset (cdr multiset))))
				(rangei 1 (second (car multiset)))))))
	(module+ test (check-equal?
		'(
			()
			((2 1))
			((2 2))
			((2 3))
			((1 1))
			((1 1) (2 1))
			((1 1) (2 2))
			((1 1) (2 3)))
		(power-multiset '((1 1) (2 3)))))

	(define (multiset->list multiset) (append-map (lambda (pair) (make-list (second pair) (first pair))) multiset))
	(module+ test (check-equal? (multiset->list '((2 3) (4 1) (5 2))) '(2 2 2 4 5 5)))

	(define (enumerate lst) (zip (range 0 (length lst)) lst))
	(module+ test (check-equal?
		'((0 4) (1 7) (2 11))
		(enumerate '(4 7 11))))

	(define (unumerate lst n) (map
		(lambda (i) (aif (assq i lst)
			(second it)
			0))
		(range 0 n)))
	(module+ test (check-equal?
		'(4 7 3 0 3 0)
		(unumerate '((1 7) (4 3) (0 4) (2 3)) 6)))
	(define (unumerate* lst) (if (null? lst)
		'()
		(unumerate lst (+ 1 (apply max (map first lst))))))
	(module+ test (check-equal?
		'(4 7 3 0 3)
		(unumerate* '((1 7) (4 3) (0 4) (2 3)))))

	(provide range rangei rev-args iverson sum indicator fun= intersection seteq subseteq subset superseteq superset sorted-set-intersection power-multiset multiset->list enumerate unumerate unumerate*))
