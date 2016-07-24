#lang racket
(require srfi/1)
(require "k-ary.rkt")
(require "general.rkt")
(require "functions.rkt")

(define (k-limit n) (let loop ([k 0]) (if (equal? (k-ary-divisors n (+ 1 k)) (k-ary-divisors n k)) k (loop (+ 1 k)))))

;; (map (lambda (n) (begin
;; 	(display (biunitary-divisors n))
;; 	(newline)
;; 	(display (divisors n))
;; 	(newline)
;; )) (rangei 1 100))

;(display (map (compose last last) (filter (lambda (args) (not (apply list== args))) (zip (map divisors (rangei 1 100)) (map biunitary-divisors (rangei 1 100))))))

;; (let ((n (defactorize '((5 2) (2 2)))))
;; 	(display (k-ary-divisors n 0))
;; 	(newline)
;; 	(display (k-ary-divisors n 1))
;; 	(newline)
;; 	(display (k-ary-divisors n 2))
;; 	(newline)
;; 	(display (k-ary-divisors n 3))
;; 	(newline)
;; 	(display (k-ary-divisors n 4))
;; 	(newline)
;; 	(display (k-ary-divisors n 5))
;; 	(newline)
;; 	(display (k-limit n))
;; 	(newline)
;; )

;; (define data (map (lambda (n) (list (prime-exponents n) (k-limit n))) (rangei 1 100)))
;; (map (lambda (datum) 
;; 	(display datum)
;; 	(newline)
;; ) data)

;; (define (hypothesis n) (= (k-limit n) (- (apply max (prime-exponents n)) 1)))
;; (display (time (find (compose not hypothesis) (rangei 2 2000))))

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

(define (remove-ones lst)
	(filter (lambda (n) (not (= 1 n))) lst))
(define (k-ary-expts n k)
	(append
		'(0)
		(map (compose car prime-exponents) (remove-ones (k-ary-divisors n k)))))

;; (time (begin
;; 		(map
;; 			(lambda (k) (map
;; 				(lambda (n) (k-ary-divisors (expt 2 n) k))
;; 				(rangei 1 limit)))
;; 			(rangei 1 limit))
;; 	"hi"))

(define limit 8)
(map
	(lambda (k) (let*
		([my-function (lambda (n d)
			(member d (k-ary-expts (expt 2 n) k)))]
		[caption (format "k = ~a" k)]
		[my-image (overlay/xy
			(text caption 36 "black")
			-10
			-10
			(grid limit my-function))]
		[file-name (format "output/~a-ary_convolution.png" k)])
		(save-image my-image file-name)))
	(range 0 limit))

(display (format "LaTeX code:~n"))
(map (lambda (k) (display (format "\\includegraphics{~a-ary_convolution.png}~n\\newpage~n" k))) (range 20 40))
