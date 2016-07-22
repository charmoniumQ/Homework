(module general racket/base
	(require srfi/1)
	(require "racketspecific.rkt")

	; the test module will contain unittests. I need to begin that module with
	; by requireing rackunit
	; Note that module+ appends to the module named `test' in subsequent
	;occurences
	(module+ test (require rackunit))

	; since equal? will work on lists,
	; the following funciton will work on nested lists
	(define list== (curry list= equal?))
	(module+ test
		(check-true (list==
			(list '(1 2) '(2 3))
			(list '(1 2) '(2 3))))
		(check-false(list==
			(list '(1 2) '(2 3))
			(list '(1 2) '(3 3)))))

	; Home on the range (inclusive)
	(define (rangei start stop) (iota (+ 1 (- stop start)) start 1))
	(module+ test
		(check-true (list== '(1 2 3 4) (rangei 1 4))))

	(define (contains list1 elem) (any ((curry =) elem) list1))
	;; (module+ test
	;; 	(check-pred (contains '(1 2 3) 2)))

	(define (rev-args f) (lambda args (apply f (reverse args))))
	(module+ test
		(check-eqv? 1 ((rev-args -) 2 3)))

	(provide list== rangei contains rev-args fold))
