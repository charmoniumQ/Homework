(module factoring racket/base
	(require srfi/1)
	(require "racketspecific.rkt")
	(require "functions-sets.rkt")

	(define (primes-leq n) (let loop ([i 0] [lst '()])
		(let ([prime (nth-prime i)])
			(if (<= prime n)
				(loop (+ 1 i) (cons prime lst))
				(reverse lst)))))
	(module+ test (check-equal? '(2 3 5) (primes-leq 6)))
	(module+ test (check-equal? '(2 3 5 7) (primes-leq 7)))

	(define (divides? a b) (= 0 (remainder b a)))

	(define (max-dividing-power p n) (let loop ([a 0])
		(if (divides? (expt p a) n) (loop (+ 1 a)) (- a 1))))
	(module+ test (check-equal? 3 (max-dividing-power 2 24)))
	(module+ test (check-equal? 0 (max-dividing-power 5 24)))

	(define (prime-divisors n) (filter (curryr divides? n) (primes-leq n)))

	(define (prime-exponents n) (map (curryr max-dividing-power n) (prime-divisors n)))

	(define (factorize n) (zip (prime-divisors n) (prime-exponents n)))

	(module+ test (check-equal? '((2 3) (5 1)) (factorize 40)))
	(module+ test (check-equal? '((7 1)) (factorize 7)))

	(define (divisors n) (sort (map
		(lambda (factor-multiset) (fold * 1 (multiset->list factor-multiset)))
		(power-multiset (factorize n))) <))
	(module+ test (check-equal? '(1) (divisors 1)))
	(module+ test (check-equal? '(1 2 3 4 6 8 12 24) (divisors 24)))

	(provide primes-leq divides? max-dividing-power prime-divisors prime-exponents factorize divisors))

