(module convolutions racket/base
	(require srfi/1)
	(require "functions-sets.rkt")
	(require "k-ary.rkt")
	(require "racketspecific.rkt")

	(module+ test (require rackunit))
	
	(define (squarefree? n) (every (curry = 1) (prime-exponents n)))
	(module+ test (check-true (squarefree? 30)))
	(module+ test (check-false (squarefree? 40)))
	
	; https://en.wikipedia.org/wiki/M%C3%B6bius_function
	(define (mobius n) (if (squarefree? n)
		(if (divides? 2 (length (prime-divisors n)))
			1
			-1)
		0))
	(module+ test (check-equal?
		'(1 -1 -1 0 -1 1 -1 0 0 1)
		(map mobius (rangei 1 10))))
	
	; The number of not-necessarily-distinct prime factors where 2^2 is treated
	; as {2, 2}
	; https://en.wikipedia.org/wiki/Prime_factor#Omega_functions
	(define (multi-prime-divisors n)
		(append-map
			(lambda (pair) (apply make-list (reverse pair)))
			(factorize n)))
	(module+ test (check-equal?
		'(2 2 2 3 3)
		(multi-prime-divisors 72)))
	
	(define (liouville n) (expt -1 (length (multi-prime-divisors n))))
	(module+ test (check-equal?
		'(1 -1 -1 1 -1 1 -1 -1 1 1)
		(map liouville (rangei 1 10))))
	
	(define (k-convolution k)
		(lambda (f g) (lambda (n)
			(sum (map
				(lambda (d) (* (f d) (g (/ n d)) (k n d)))
				(divisors n))))))
	
	(define (A-convolution A)
		(k-convolution
			(lambda (n d) ((indicator (A n)) d))))
	
	(define (k-ary-convolution k)
		(A-convolution
			(lambda (n) (k-ary-divisors n k))))
	
	(define dirichlet-convolution (k-ary-convolution 0))
	(module+ test (check-true (fun=
		(dirichlet-convolution (const 1) mobius)
		(indicator '(1)))))
	(module+ test (check-true (fun=
		(dirichlet-convolution (const 1) (const 1))
		((curryr divisor-sum) 0))))
	(module+ test (check-true (fun=
		(dirichlet-convolution liouville (compose1 abs mobius))
		(indicator '(1)))))
	(module+ test (check-true (fun=
		(dirichlet-convolution totient (const 1))
		identity)))
	(module+ test (check-true (fun=
		(dirichlet-convolution ((curryr expt) 3) (const 1))
		((curryr divisor-sum) 3))))
	
	(define unitary-convolution (k-ary-convolution 1))
	(define biunitary-convolution (k-ary-convolution 2))
	
	;; (display (time
	;; 	(every superseteq (map
			;; (lambda (n)
			;; 	(list (septary-divisors n) (pentary-divisors n) (triunitary-divisors n) (unitary-divisors n) (octary-divisors n) (hexary-divisors n) (tetrary-divisors n) (biunitary-divisors n)))
	;; 		(rangei 1 1500)))))
	;; (newline)
	
	(provide identity const liouville k-convolution A-convolution k-ary-convolution dirichlet-convolution unitary-convolution biunitary-convolution))
