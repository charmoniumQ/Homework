(module racketspecific racket/base
	(require (only-in racket/base even? compose gcd remainder))
	(require (only-in racket/function curry curryr const identity))
	(require (only-in racket/list cartesian-product empty?))
	(require (only-in math/number-theory
		divides? divisors factorize prime-divisors prime-exponents divisor-sum totient))
	(require memoize); raco pkg install memoize

	(provide even? compose gcd remainder curry curryr const identity cartesian-product empty? divides? divisors factorize prime-divisors prime-exponents divisor-sum totient define/memo))
