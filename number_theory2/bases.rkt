(module bases racket/base
	(require srfi/1)
	(require "racketspecific.rkt")
	(require "functions-sets.rkt")

	(module+ test (require rackunit))

	; Little-Endian
	(define (digits-le n base) (let loop ([n n] [place-value 1])
		(if (= 0 n)
			'()
			(let* (
				[digit (quotient (remainder n (* base place-value)) place-value)]
				[n (- n (* digit place-value))]
				[place-value (* base place-value)])
				(cons digit (loop n place-value))))))

	; Big-Endian (normal convention for humans)
	(define (digits-be n base) (reverse (digits-le n base)))
	(module+ test (check-equal?
		'(1 0 0 1 1)
		(digits-be 19 2)))
	(module+ test (check-equal?
		'()
		(digits-be 0 2)))
	(module+ test (check-equal?
		'(1 2 0)
		(digits-be 15 3)))

	(define (undigits-le digits base) (fold
		(lambda (pair sum)
			; (first pair) -> digit, (second pair) -> place-index
			(+ sum (* (first pair) (expt base (second pair)))))
		0
		(zip digits (range 0 (length digits)))))
	(define (undigits-be digits base) (undigits-le (reverse digits) base))

	(module+ test (check-eq? 19 (undigits-le (digits-le 19 2) 2)))
	(module+ test (check-eq? 0 (undigits-le (digits-le 0 2) 2)))

	(provide digits-le digits-be undigits-le undigits-be ))
