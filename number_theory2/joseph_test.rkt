#lang racket
(require anaphoric)
(require srfi/1)
(require "racketspecific.rkt")
(require "functions-sets.rkt")
(require "bases.rkt")

(require rackunit)

(define (theta-k-ary-divisors-of-power a k) (let ([n (length (digits-be a k))]) (map
	(lambda (digit-multiset)
		(undigits-be (unumerate digit-multiset n) k))
	(power-multiset (enumerate (digits-be a k))))))
(define th_k-div-pow theta-k-ary-divisors-of-power)
(check-equal?
	'(0 3 6 9 12 15)
	(th_k-div-pow 15 3))
(check-equal?
	(range 0 16)
	(th_k-div-pow 15 2))
(check-equal?
	'(0 1 2 4 5 6 8 9 10 12 13 14)
	(th_k-div-pow 14 4))

(require 2htdp/image)

(define size 24)

(define (white-square n)
	(rectangle size size "solid" "white"))

(define (black-square n)
	(overlay
		(text (format "p^~a" n) 8 "blue")
		(rectangle size size "solid" "black")))

(define half-padding
	(rectangle (/ size 2) size "solid" "gray"))

(define (grid size f) (let*
	([make-row (lambda (level)
		(let* (
			[padding-size (- size level)]
			[padding (make-list padding-size half-padding)]
			[make-cell (lambda (n) (if (f level n) (black-square n) (white-square n)))]
			[content (map make-cell (rangei 0 level))])
			(apply beside (append padding content padding))))]
	[rows (map make-row (rangei 0 size))])
	(apply above rows)))

(define limit 20)
(map
	(lambda (k) (let*
		([my-function (lambda (n d)
			(member d (th_k-div-pow n k)))]
		[caption (format "t_k = ~a" k)]
		[my-image (overlay/xy
			(text caption 36 "black")
			-10
			-10
			(grid limit my-function))]
		[file-name (format "output/theta_~a.png" k)])
		(save-image my-image file-name)
		(display (format "\\includegraphics{~a}~n\\newpage~n" file-name))))
	(range 2 limit))
