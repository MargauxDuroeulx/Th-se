;Tokens convertis en format smt2:
;;
(set-logic QF_UFLIA)
(declare-fun r1 () Bool)
(declare-fun g1 () Bool)
(declare-fun g2 () Bool)
(declare-fun e1 () Bool)
(declare-fun e2 () Bool)
(declare-fun e3 () Bool)
(declare-fun e4 () Bool)
(declare-fun e5 () Bool)
;;
(assert (or (not r1) (and g1 g2)))
(assert (or (not (and g1 g2)) r1))
;;
(assert (or (not g1) e1 e2 e3))
(assert (or (not (or e1 e2 e3)) g1))
;;
(assert (or (not g2) e4 e5))
(assert (or (not (or e4 e5)) g2))
;;
(assert r1)
;;
(check-sat)
(get-model)
