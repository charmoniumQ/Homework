; Define replacement for module
; Define replacement for 

(module racketspecific racket/base
	(require (only-in racket/base compose sort))
	(require (only-in racket/math exact-floor))
	(require (only-in racket/function curry curryr const identity))
	(require (only-in racket/list cartesian-product))
	(require (only-in math/number-theory
		nth-prime
		divisor-sum totient))
	(require memoize); raco pkg install memoize
	(require (only-in rackunit check-true check-false check-equal?))
	(require (only-in anaphoric aif))

	; http://docs.racket-lang.org/guide/performance.html?q=modules#%28part._modules-performance%29

	(provide compose sort exact-floor curry curryr const identity cartesian-product nth-prime divisor-sum totient check-true check-false check-equal? define/memo aif))
