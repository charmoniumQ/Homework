; Uncomment for racket:
;#lang scheme
;(require srfi/1)

; Uncomment for guile:
;(use-modules (srfi srfi-1))
;(define void (lambda () (display "")))

; Uncomment for chicken:
(use srfi-1) (define void (lambda () 0))

;;;;;;;;;; Genereal Definitions
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

; Test to see if two lists are numerically equal
(define (list== a b) (list= = a b))

(define (repeat list1 count1)
	(if (= count1 0)
		(list)
		(append list1 (repeat list1 (- count1 1)))))
(assert "List repeat"
	(list== '(1 2 3 1 2 3 1 2 3) (repeat '(1 2 3) 3)))

; TODO: write this k-ary
(define (flat-map f list) (fold-right append '() (map f list)))
(assert "Flat map"
	(list== '(1 4 1 7 1 8) (flat-map (lambda (x) (list 1 x)) '(4 7 8))))

(define (range start stop)
	(iota (- (+ 1 stop) start) start))
(assert "Range" (list== '(1 2 3) (range 1 3)))
(assert "Empty range" (list== '(1) (range 1 1)))

(define (contains list1 elem) (any (lambda (elem2) (= elem elem2)) list1))
(assert "Contains" (contains '(1 2 3) 3))
(assert "Not contains" (not (contains '(1 2 3) 6)))

; No parenthesis around args allows variadic funcitons

(define (curry f . pre)
	(lambda post (apply f (append pre post))))

(define (right-curry f . post)
	(lambda pre
		(apply f (append pre post))))

;;;;;;;;;; Function and set definitions

; https://en.wikipedia.org/wiki/Iverson_bracket
; #t -> 1 and #f -> 0
(define (iverson s) (if s 1 0))

; TODO: write this k-ary
(define (cartesian-product-list list1 list2)
	(list
		(flat-map (curry make-list (length list2)) list1)
		(repeat list2 (length list1))))
(assert "Cartesian list" (list= list==
	'((1 1 2 2 3 3) (4 5 4 5 4 5))
	(cartesian-product-list '(1 2 3) '(4 5))))
; Note the syntax for comparing a list of list
; (list== list= list1 list2)

(define (cartesian-product list1 list2)
	(apply zip (cartesian-product-list list1 list2)))
(assert "Cartesian product" (list= list==
	(list '(1 4) '(1 5) '(2 4) '(2 5) '(3 4) '(3 5))
	(cartesian-product '(1 2 3) '(4 5))))

(define (sum list1) (fold + 0 list1))
(assert "Sum" (= 55 (sum (range 1 10))))
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

(define (intersection a b) (lset-intersection = a b))
(assert "Intersection" (list== '(1 3) (intersection (range 1 5) '(0 1 3))))

; Another variadic lambda function
(define (compose f g) (lambda args (f (apply g args))))

;;;;;;;;;; Classical factoring definitions

(define (divides? d n) (= 0 (remainder n d)))
(assert "Divides" (divides? 1 10))
(assert"Negative divides" (not (divides? 3 10)))

(define (coprime? a b) (= 1 (gcd a b)))
(assert "Coprime" (coprime? 10 7))
(assert "Negative coprime" (not (coprime? 10 15)))

(define (divides-n n) (right-curry divides? n))

(define (divisor-list n) (filter (divides-n n) (range 1 n)))
(assert "Divisor list of 12" (list==
	'(1 2 3 4 6 12)
	(divisor-list 12)))
(assert "Divisor list of 9" (list==
	'(1 3 9)
	(divisor-list 9)))

(define (coprime-to a) (curry coprime? a))

(define (totient n) (count (coprime-to n) (range 1 n)))
(assert "Totient 9" (= 6 (totient 9)))
(assert "Totient 1" (= 1 (totient 1)))

(define (prime n) (list== (list 1 n) (divisor-list n)))
(assert "Prime" (prime 3))
(assert "Not prime" (not (prime 9)))

(define (prime-divisor-list n) (filter prime (divisor-list n)))

(define (largest-prime-power p n)
	(if (not (prime p))
		(error "p must be prime")
		(do
			((a 0 (+ 1 a)))
			((not (divides? (expt p a) n)) (- a 1)))))
(assert "$\\nu_2(24) = 3$" (= 3 (largest-prime-power 2 24)))
(assert "$\\nu_5(24) = 0$" (= 0 (largest-prime-power 5 24)))

; Returns a list of pairs of factors and exponents
(define (prime-factorization n)
	(map
		(lambda (p) (list p (largest-prime-power p n)))
		(prime-divisor-list n)))
(assert "Prime factorization" (list= list==
	(list '(2 3) '(3 1))
	(prime-factorization 24)))

; https://en.wikipedia.org/wiki/Square-free_integer
(define (square-free? n) (not
	(any
		(lambda (pair) (< 1 (second pair))) ; second element in pair is exponent
		(prime-factorization n))))
(assert "Square-free" (square-free? 15))
(assert "Negative square-free" (not (square-free? 18)))

; https://en.wikipedia.org/wiki/Divisor_function#Definition
(define (divisor-function x n) (sum (map
	(lambda (d) (expt d x))
	(divisor-list n))))
(assert "$\\sigma_1(12) = 28" (= (divisor-function 1 12) 28))

;;;;;;;;;; K-ary definitions

(define (k-ary-divides? d n k) (if
	(= k 0)
	(divides? d n)
	(and
		(= 0 (remainder n d))
		(k-ary-coprime? d (/ n d) (- k 1)))))

(define (k-ary-coprime? a b k) (= 1 (k-ary-gcd a b k)))

(define (k-ary-gcd a b k)
	(apply max (intersection
		(k-ary-divisor-list a k)
		(k-ary-divisor-list b k))))

(define (k-ary-divisor-list n k) (filter
	(k-ary-divides-n-with-k n k)
	(range 1 n)))

(define (k-ary-divides-n-with-k n k) (lambda (d) (k-ary-divides? d n k)))

; k-ary-divides -> k-ary-coprime? -> k-ary-gcd -> k-ary-divisor-list ->
; ->k-ary-divides-n-with-k -> k-ary-divides (again, but with k := k - 1)
; Note that since the functions defined here are mutually recursive
; these must be tested all at once
(assert "k-ary divisor list" (list== '(1 5 9 45) (k-ary-divisor-list 45 1)))
(assert "0-ary gcd equals regular gcd" (fun=
	(lambda (x) (gcd 10 x))
	(lambda (x) (k-ary-gcd 10 x 0))))
(assert "Unitary divides 45" (k-ary-divides? 9 45 1))
(assert "Unitary divides 12" (k-ary-divides? 12 60 1))

;;;;;;;;;; Convolution definitions

(define (identity x) x)

(define (constant-function x0) (lambda (x) x0))

; https://en.wikipedia.org/wiki/M%C3%B6bius_function
(define (mobius n) (if (square-free? n)
	(if (divides? 2 (length (prime-divisor-list n)))
		1
		-1)
	0))
(assert (list==
	'(1 -1 -1 0 -1 1 -1 0 0 1)
	(map mobius (range 1 10))) "Mobius function")

; The number of not-necessarily-distinct prime factors where 2^2 is treated
; as {2, 2}
; https://en.wikipedia.org/wiki/Prime_factor#Omega_functions
(define (multi-prime-factors n) (sum
	(map second (prime-factorization n)))) ; the second element is the exponent

(define (liouville n) (expt -1 (multi-prime-factors n)))

(define (k-convolution k)
	(lambda (f g) (lambda (n)
		(sum (map
			(lambda (d) (* (f d) (g (/ n d)) (k n d)))
			(divisor-list n))))))

(define (A-convolution A)
	(k-convolution
		(lambda (n d) (iverson (contains (A n) d)))))

(define (k-ary-convolution k)
	(A-convolution
		(lambda (n) (k-ary-divisor-list n k))))

(define dirichlet-convolution (k-ary-convolution 0))
(assert "$1 * \\mu = e$" (fun=
	(dirichlet-convolution (constant-function 1) mobius)
	(indicator '(1))))
(assert "$1 * 1 = \\sigma$" (fun=
	(dirichlet-convolution (constant-function 1) (constant-function 1))
	(curry divisor-function 0)))
(assert "$\\lambda * \\lvert \\mu \\rvert = e$" (fun=
	(dirichlet-convolution liouville (compose abs mobius))
	(indicator '(1))))
(assert "$\\phi * 1 = Id$" (fun=
	(dirichlet-convolution totient (constant-function 1))
	identity))
(assert "$Id^3 * 1 = \\sigma_3$" (fun=
	(dirichlet-convolution (right-curry expt 3) (constant-function 1))
	(curry divisor-function 3)))

(define unitary-convolution (k-ary-convolution 1))
