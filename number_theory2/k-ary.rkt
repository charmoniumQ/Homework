(module k-ary racket/base
	(require srfi/1)
	(require "racketspecific.rkt")
	(require "functions-sets.rkt")

	(module+ test (require rackunit))

	(define (k-ary-divides? d n k)
		(if (= k 0)
			(divides? d n)
			(and
				(= 0 (remainder n d))
				(k-ary-coprime? d (/ n d) (- k 1)))))
	(define (k-ary-divides-pow? a b k)
		(if (= k 0)
			(<= a b)
			(k-ary-coprime-pow? a (- b a) (- k 1))))

	(define (k-ary-coprime? a b k) (= 1 (k-ary-gcd a b k)))
	(define (k-ary-coprime-pow? a b k) (= 0 (k-ary-gcd-pow a b k)))

	(define (k-ary-gcd a b k)
			(sorted-set-intersection-max
				(k-ary-divisors a k)
				(k-ary-divisors b k)))
	(define (k-ary-gcd-pow a b k)
			(sorted-set-intersection-max
				(k-ary-divisors-pow a k)
				(k-ary-divisors-pow b k)))

	(define/memo (k-ary-divisors n k)
		(filter
			(curryr k-ary-divides? n k)
			(divisors n)))
	(define/memo (k-ary-divisors-pow n k)
		(filter
			(curryr k-ary-divides-pow? n k)
			(rangei 0 n)))

	(define unitary-divisors (curryr k-ary-divisors 1))
	(define biunitary-divisors (curryr k-ary-divisors 2))
	(define triunitary-divisors (curryr k-ary-divisors 3))

	; k-ary-divides -> k-ary-coprime? -> k-ary-gcd -> k-ary-divisors ->
	; ->k-ary-divides-n-with-k -> k-ary-divides (again, but with k := k - 1)
	; Note that since the functions defined here are mutually recursive
	; these must be tested all at once
	(module+ test (check-equal? '(1 5 9 45) (k-ary-divisors 45 1)))
	(module+ test (check-true (fun=
		(lambda (x) (gcd 10 x))
		(lambda (x) (k-ary-gcd 10 x 0)))))
	(module+ test (check-true (k-ary-divides? 9 45 1)))
	(module+ test (check-true (k-ary-divides? 12 60 1)))
	(module+ test (check-equal? '(0 2 8 10) (k-ary-divisors-pow 10 5)))

	(module+ test (time (begin
		(map
			(lambda (k) (map
				(lambda (n) (k-ary-divisors n k))
			(rangei 1 1000)))
		(rangei 1 20)) (void))))
	(module+ test (time (begin
		(map
			(lambda (k) (map
				(lambda (n) (k-ary-divisors-pow n k))
			(rangei 1 10)))
		(rangei 1 20)) (void))))

	(provide
		k-ary-divides? k-ary-coprime? k-ary-gcd k-ary-divisors divisors
		unitary-divisors biunitary-divisors triunitary-divisors
		k-ary-divides-pow? k-ary-coprime-pow? k-ary-gcd-pow k-ary-divisors-pow))
