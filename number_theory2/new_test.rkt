#lang racket/base
(require srfi/1)
(require srfi/13)
(require anaphoric)
(require "racketspecific.rkt")
(require "functions-sets.rkt")
(require "k-ary.rkt")

;; (define (filter-map f lst) (let
;; 	([out (filter (compose not false?) (map f lst))])
;; 	(if (null? out) #f out)))

;; (define k 9)

;; (display
;; (filter-map
;; 	(lambda (c) (filter-map
;; 		(lambda (b) (filter-map
;; 			(lambda (a) (if (k-ary-divides-pow? a c k) #f (list a b c)))
;; 			(k-ary-divisors-pow b k)))
;; 		(k-ary-divisors-pow c k)))
;; 	(rangei 1 20)))

(define security 200)
(define (stable? i k)
	(every
		(lambda (i*) (list= =
			(k-ary-divisors-pow i* k)
			(k-ary-divisors-pow i* (- k 2))))
		(rangei i (+ security i))))

(define/memo (first-stable-line k)
	(let loop ([i (if (> k 5) (first-stable-line (- k 2)) k)])
		(if (stable? i k)
			i
			(loop (+ 1 i)))))

;; (require profile)
;; (profile (map first-stable-line (rangei 3 20)))

;(define data (zip (rangei 3 50) (map first-stable-line (rangei 3 50))))
;(display data)

(define data '((3 7) (4 11) (5 15) (6 27) (7 23) (8 43) (9 31) (10 59) (11 47) (12 91) (13 63) (14 123) (15 79) (16 155) (17 95) (18 187) (19 111) (20 219) (21 127) (22 251) (23 159) (24 315) (25 191) (26 379) (27 223) (28 443) (29 255) (30 507) (31 287) (32 571) (33 319) (34 635) (35 351) (36 699) (37 383) (38 763) (39 415) (40 827) (41 447) (42 891) (43 479) (44 955) (45 511) (46 1019) (47 575) (48 1147) (49 639) (50 1275)))

(define (even? n) (divides? 2 n))
(define (odd? n) (not (divides? 2 n)))
(define evens (filter (lambda (pair) (even? (first pair))) data))
(define odds (filter (lambda (pair) (odd? (first pair))) data))

(require plot)
;; (plot-height 800)
;; (plot-width 1000)
;; (plot (list (lines evens) (lines odds) (points data)) #:out-file "output.png" #:x-label "k-ary convolution" #:y-label "first stable line")

(define (display-list lst) (string-join (map (lambda (row) (string-join (map (lambda (cell) (format "~a" cell)) row) ",")) lst) "\n"))
(display (format "~a" (display-list evens)))
(newline)
(display (format "~a" (display-list odds)))
