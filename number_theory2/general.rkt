#lang scheme
(require srfi/1)
(require racket/function)

(define (assert msg test)
	(if (not test)
		(begin
			(display "assert failed: ")
			(display msg)
			(newline))
		(void)))
; The assert method does two things
; (1) verifies correctness of my code
; (2) documents my code with an example for future readers

; since equal? will work on lists,
; the following funciton will work on nested lists
(define list== ((curry list=) equal?))
(assert "List equals" (list==
	(list '(1 2) '(2 3))
	(list '(1 2) '(2 3))))
(assert "List not equals" (not (list==
	(list '(1 2) '(2 3))
	(list '(1 2) '(3 3)))))

; Home on the range (inclusive)
(define (rangei start stop) (range start (+ 1 stop)))
(assert "Rangei" (list== '(1 2 3 4) (rangei 1 4)))

(define (contains list1 elem) (any ((curry =) elem) list1))
(assert "Contains" (contains '(1 2 3) 2))

(define (rev-args f) (lambda args (apply f (reverse args))))
(assert "Rev-args" (= 1 ((rev-args -) 2 3)))

(provide assert list== rangei contains rev-args)
