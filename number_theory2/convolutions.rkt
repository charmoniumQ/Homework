#lang scheme
(require srfi/1)
(require math/number-theory)
(require "general.rkt")
(require "functions.rkt")
(require "k-ary.rkt")

; The number of not-necessarily-distinct prime factors where 2^2 is treated
; as {2, 2}
; https://en.wikipedia.org/wiki/Prime_factor#Omega_functions
(define (multi-prime-divisors n)
	(append-map
		(lambda (pair) (apply make-list (reverse pair)))
		(factorize n)))
(assert "Multi-prime-divisors" (list==
	'(2 2 2 3 3)
	(multi-prime-divisors 72)))

(define (liouville n) (expt -1 (length (multi-prime-divisors n))))
(assert "Liouville" (list==
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
(assert "$1 * \\mu = e$" (fun=
	(dirichlet-convolution (const 1) moebius-mu)
	(indicator '(1))))
(assert "$1 * 1 = \\sigma$" (fun=
	(dirichlet-convolution (const 1) (const 1))
	((curryr divisor-sum) 0)))
(assert "$\\lambda * \\lvert \\mu \\rvert = e$" (fun=
	(dirichlet-convolution liouville (compose1 abs moebius-mu))
	(indicator '(1))))
(assert "$\\phi * 1 = Id$" (fun=
	(dirichlet-convolution totient (const 1))
	identity))
(assert "$Id^3 * 1 = \\sigma_3$" (fun=
	(dirichlet-convolution ((curryr expt) 3) (const 1))
	((curryr divisor-sum) 3)))

(define unitary-convolution (k-ary-convolution 1))
(define biunitary-convolution (k-ary-convolution 2))

(define unitary-divisors ((curryr k-ary-divisors) 1))
(define biunitary-divisors ((curryr k-ary-divisors) 2))
(define triunitary-divisors ((curryr k-ary-divisors) 3))
(define tetrary-divisors ((curryr k-ary-divisors) 4))
(define pentary-divisors ((curryr k-ary-divisors) 5))
(define hexary-divisors ((curryr k-ary-divisors) 6))
(define septary-divisors ((curryr k-ary-divisors) 7))
(define octary-divisors ((curryr k-ary-divisors) 8))

(display (time
	(every superseteq (map
		(lambda (n)
			(list (septary-divisors n) (pentary-divisors n) (triunitary-divisors n) (unitary-divisors n)))
		(rangei 1 500)))))
(newline)

(display (time
	(every superseteq (map
		(lambda (n)
			(list (octary-divisors n) (hexary-divisors n) (tetrary-divisors n) (biunitary-divisors n)))
	(rangei 1 500)))))
(newline)

(provide identity const liouville k-convolution A-convolution k-ary-convolution dirichlet-convolution unitary-convolution biunitary-convolution)
