#lang scheme
(require math/number-theory)
(require memoize) ; raco pkg install memoize
(require "general.rkt")
(require "functions.rkt")

(define (k-ary-divides? d n k) (if
	(= k 0)
	(divides? d n)
	(and
		(= 0 (remainder n d))
		(k-ary-coprime? d (/ n d) (- k 1)))))

(define (k-ary-coprime? a b k) (= 1 (k-ary-gcd a b k)))

(define (k-ary-gcd a b k)
	(apply max (intersection
		(k-ary-divisors a k)
		(k-ary-divisors b k))))

(define/memo (k-ary-divisors n k) (filter
	((curryr k-ary-divides?) n k)
	(rangei 1 n)))

; k-ary-divides -> k-ary-coprime? -> k-ary-gcd -> k-ary-divisors ->
; ->k-ary-divides-n-with-k -> k-ary-divides (again, but with k := k - 1)
; Note that since the functions defined here are mutually recursive
; these must be tested all at once
(assert "k-ary divisor list" (list== '(1 5 9 45) (k-ary-divisors 45 1)))
(assert "0-ary gcd equals regular gcd" (fun=
	(lambda (x) (gcd 10 x))
	(lambda (x) (k-ary-gcd 10 x 0))))
(assert "Unitary divides 45" (k-ary-divides? 9 45 1))
(assert "Unitary divides 12" (k-ary-divides? 12 60 1))

(provide k-ary-divides? k-ary-coprime? k-ary-gcd k-ary-divisors)
