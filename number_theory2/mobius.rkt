#lang scheme
(require srfi/1)
(require anaphoric)
(require "k-ary.rkt")
(require "functions-sets.rkt")
(require "convolutions.rkt")

(define mobius-table '((1 . 1)))

(define (mobius-extend n k)
	(let
		([mobius-extend-of-n (* -1 (apply + (map (lambda (n) (aif (assq n mobius-table) (cdr it) 0)) (k-ary-divisors n k))))])
		(set! mobius-table (cons `(,n . ,mobius-extend-of-n) mobius-table))))

(map
	(lambda (k)
		(set! mobius-table '((1 . 1)))
		(map ((curryr mobius-extend) k) (iota 3500 1))
		(display (filter (lambda (pair) (not (memq (cdr pair) '(-1 0 1)))) mobius-table)))
	'(4))

;(define (mobius-lookup))

(display (filter
	(lambda (n) (not (= 0 (((k-ary-convolution 4) (compose cdr ((curryr assq) mobius-table)) (const 1)) (+ 1 n)))))
	(iota 3499 1)))
