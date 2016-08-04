#lang racket
(require srfi/1)
(require "racketspecific.rkt")
(require "functions-sets.rkt")
(require "k-ary.rkt")
(require rackunit)
(require json)
(require 2htdp/image)
(require memoize)

(define limit 400)

(display "0")
(newline)

(define cmap-vector (let* (
	[output-str (with-output-to-string (lambda () (system* "./viridis.py" (number->string limit))))]
	[output-list (string->jsexpr output-str)]
	[output-vector (apply vector
		(map
			(lambda (row) (apply vector (map
				(lambda (cell) (apply make-color cell))
				row)))
			output-list))])
	output-vector))

(display "1")
(newline)

(define (get-color value) (let* (
	[row (vector-ref cmap-vector (denominator value))]
	[cell (vector-ref row (numerator value))])
	cell))

(define (make-cell n level sq-size text-size max-level val render-caption)
	(if val
		(let* (
			[color (get-color (/ val max-level))]
			[text-contents (text (format "~a" val) text-size "red")]
			[rect-contents (rectangle sq-size sq-size "solid" color)])
			(if render-caption (overlay text-contents rect-contents) rect-contents))
		(rectangle sq-size sq-size "solid" "white")))

(define (grid f levels sq-size text-size render-caption) (let*
	([make-row (lambda (level)
		(let* (
			[padding-length (- levels level)]
			[half-padding (rectangle (/ sq-size 2) sq-size "solid" "gray")]
			[padding (make-list padding-length half-padding)]
			[make-content (lambda (n) (make-cell n level sq-size text-size levels (f n level) render-caption))]
			[content (map make-content (rangei 0 level))])
			(display (format "level: ~a" level))
			(newline)
			(apply beside (append padding content padding))))]
	[rows (map make-row (rangei 0 levels))])
	(apply above rows)))


(define (f n level) (if (= level 0) 0 
	(if (infinitary-divides-pow? n level)
		(find (curry k-ary-divides-pow? n level) (rangei 1 level 2))
		(find (compose not (curry k-ary-divides-pow? n level)) (rangei 0 level 2)))))

;; (check-equal? (f 0 10) 1)
;; (check-equal? (f 1 2) 2)
;; (check-equal? (f 2 6) 3)

;; (save-image
;; 	(grid f limit 18 10)
;; 	"pyramid.png")

(define (f-odd n level) (if (= level 0) 0 
	(if (infinitary-divides-pow? n level)
		(find (curry k-ary-divides-pow? n level) (rangei 1 level 2))
		#f)))

(define (f-even n level) (if (= level 0) 0 
	(if (infinitary-divides-pow? n level)
		#f
		(find (compose not (curry k-ary-divides-pow? n level)) (rangei 0 level 2)))))

(display "2")
(newline)

;; (save-image
;; 	(grid f-odd limit 18 10 #t)
;; 	"pyramid_odd_numbers.png")

;; (save-image
;; 	(grid f-even limit 18 10 #t)
;; 	"pyramid_even_numbers.png")

;; (save-image
;; 	(grid f-odd limit 4 10 #f)
;; 	"pyramid_odd.png")

;; (save-image
;; 	(grid f-even limit 4 10 #f)
;; 	"pyramid_even.png")

(save-image
	(grid f limit 1 10 #f)
	"bigpyramid.png")
