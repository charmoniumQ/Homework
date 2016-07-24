; Define replacement for module
; Define replacement for 

(module racketspecific racket/base
	(require (only-in racket/base compose sort format))
	(require (only-in racket/math exact-floor))
	(require (only-in racket/function curry curryr const identity))
	(require (only-in racket/list cartesian-product))
	(require (only-in math/number-theory
		divides? max-dividing-power prime-divisors prime-exponents factorize divisors divisor-sum totient))
	(require memoize); raco pkg install memoize
	(require (only-in rackunit check-true check-false check-equal?))
	(require (only-in anaphoric aif))
	(require (only-in racket/bool false?))

	; http://srfi.schemers.org/srfi-64/srfi-64.html
	; http://srfi.schemers.org/srfi-78/srfi-78.html
	; http://srfi.schemers.org/srfi-95/srfi-95.html
	; http://srfi.schemers.org/srfi-132/srfi-132.html

	; http://docs.racket-lang.org/guide/performance.html?q=modules#%28part._modules-performance%29

	(provide compose sort format exact-floor curry curryr const identity cartesian-product divides? max-dividing-power prime-divisors prime-exponents factorize divisors divisor-sum totient check-true check-false check-equal? define/memo aif false?))
