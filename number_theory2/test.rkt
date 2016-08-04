#lang racket
(require srfi/1)
(require "racketspecific.rkt")
(require "functions-sets.rkt")
(require "k-ary.rkt")
(require 2htdp/image)

(define (make-cell n level sq-size color)
	(rectangle sq-size sq-size "solid" color))

(define (grid f levels sq-size) (let*
	([make-row (lambda (level)
		(let* (
			[padding-length (- levels level)]
			[half-padding (rectangle (/ sq-size 2) sq-size "solid" "gray")]
			[padding (make-list padding-length half-padding)]
			[make-content (lambda (n) (make-cell n level sq-size (f n level)))]
			[content (map make-content (rangei 0 level))])
			(apply beside (append padding content padding))))]
	[rows (map make-row (rangei 0 levels))])
	(apply above rows)))


(define (value-to-cell n) (let* (
	[color (if (second n) (make-color 0 0 0) (make-color 255 255 255))]
	[cell (rectangle sq-size)])
	(overlay cell symbol)))


(define (cell-to-value d n k) (list
	(k-ary-divides-pow? d n (- k 1))
	(k-ary-divides-pow? d n k)))

(define limit 40)
(define sq-size 10)

(map
	(lambda (k) (let* (
		[my-grid (grid (lambda (n level) (value-to-color (cell-to-value n level k))) limit 10)]
		[caption (format "k = ~a" k)]
		[my-image (overlay/xy
			(text caption 20 "black")
			-10
			-10
			my-grid)]
		[file-name (format "output/~a-ary_conv.png" k)])
		(save-image my-image file-name)
		(display (format "\\includegraphics{~a}~n\\newpage~n" file-name))))
	(range 2 limit))
