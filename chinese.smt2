;Tokens convertis en format smt2:
;;
(set-logic QF_UFLIA)
(declare-fun g1 () Bool)
(declare-fun g2 () Bool)
(declare-fun e1 () Bool)
(declare-fun e2 () Bool)
(declare-fun e3 () Bool)
(declare-fun g3 () Bool)
(declare-fun g4 () Bool)
(declare-fun g5 () Bool)
(declare-fun g6 () Bool)
(declare-fun g7 () Bool)
(declare-fun e4 () Bool)
(declare-fun e5 () Bool)
(declare-fun e6 () Bool)
(declare-fun e7 () Bool)
(declare-fun g8 () Bool)
(declare-fun e8 () Bool)
(declare-fun g9 () Bool)
(declare-fun e9 () Bool)
(declare-fun e10 () Bool)
(declare-fun e11 () Bool)
(declare-fun g10 () Bool)
(declare-fun e12 () Bool)
(declare-fun e13 () Bool)
(declare-fun g11 () Bool)
(declare-fun g12 () Bool)
(declare-fun g13 () Bool)
(declare-fun g14 () Bool)
(declare-fun g15 () Bool)
(declare-fun g16 () Bool)
(declare-fun e14 () Bool)
(declare-fun e15 () Bool)
(declare-fun e16 () Bool)
(declare-fun g17 () Bool)
(declare-fun g18 () Bool)
(declare-fun g19 () Bool)
(declare-fun g20 () Bool)
(declare-fun g21 () Bool)
(declare-fun e17 () Bool)
(declare-fun e18 () Bool)
(declare-fun e19 () Bool)
(declare-fun e20 () Bool)
(declare-fun e21 () Bool)
(declare-fun g22 () Bool)
(declare-fun g23 () Bool)
(declare-fun e22 () Bool)
(declare-fun e23 () Bool)
(declare-fun e24 () Bool)
(declare-fun e25 () Bool)
(declare-fun g24 () Bool)
(declare-fun g25 () Bool)
(declare-fun g26 () Bool)
(declare-fun g27 () Bool)
(declare-fun g28 () Bool)
(declare-fun g29 () Bool)
(declare-fun g30 () Bool)
(declare-fun g31 () Bool)
(declare-fun g32 () Bool)
(declare-fun g33 () Bool)
(declare-fun g34 () Bool)
(declare-fun g35 () Bool)
;;
(assert (and g1 g2))
;;
(assert (or (not g1) e1 e2 e3 g3)
(assert (or (not (or e1 e2 e3 g3)) g1)
;;
(assert (or (not g2) (and g4 g5))
(assert (or (not (and g4 g5)) g2)
;;
(assert (or (not g3) (and g6 g7))
(assert (or (not (and g6 g7)) g3)
;;
(assert (or (not g4) e4 e5 e6 e7 g8)
(assert (or (not (or e4 e5 e6 e7 g8)) g4)
;;
(assert (or (not g5) e8 g9)
(assert (or (not (or e8 g9)) g5)
;;
(assert (or (not g6) e9 e10 e11 g10)
(assert (or (not (or e9 e10 e11 g10)) g6)
;;
(assert (or (not g7) e12 e13)
(assert (or (not (or e12 e13)) g7)
;;
(assert (or (not g8) (and g11 g12))
(assert (or (not (and g11 g12)) g8)
;;
(assert (or (not g9) (and g13 g14))
(assert (or (not (and g13 g14)) g9)
;;
(assert (or (not g10) (and g15 g16))
(assert (or (not (and g15 g16)) g10)
;;
(assert (or (not g11) e14 e15 e16 g17)
(assert (or (not (or e14 e15 e16 g17)) g11)
;;
(assert (or (not g12) (and g18 g19))
(assert (or (not (and g18 g19)) g12)
;;
(assert (or (not g13) e1 e2 e3 g20)
(assert (or (not (or e1 e2 e3 g20)) g13)
;;
(assert (or (not g14) e4 e5 e6 e7 g21)
(assert (or (not (or e4 e5 e6 e7 g21)) g14)
;;
(assert (or (not g15) e17 e18)
(assert (or (not (or e17 e18)) g15)
;;
(assert (or (not g16) e19 e20 e21)
(assert (or (not (or e19 e20 e21)) g16)
;;
(assert (or (not g17) (and g22 g23))
(assert (or (not (and g22 g23)) g17)
;;
(assert (or (not g18) e22 e23)
(assert (or (not (or e22 e23)) g18)
;;
(assert (or (not g19) e24 e25)
(assert (or (not (or e24 e25)) g19)
;;
(assert (or (not g20) (and g24 g25))
(assert (or (not (and g24 g25)) g20)
;;
(assert (or (not g21) (and g26 g27))
(assert (or (not (and g26 g27)) g21)
;;
(assert (or (not g22) e17 e18 e21)
(assert (or (not (or e17 e18 e21)) g22)
;;
(assert (or (not g23) e19 e20)
(assert (or (not (or e19 e20)) g23)
;;
(assert (or (not g24) e14 e15 e16 g28)
(assert (or (not (or e14 e15 e16 g28)) g24)
;;
(assert (or (not g25) (and g29 g30))
(assert (or (not (and g29 g30)) g25)
;;
(assert (or (not g26) e9 e10 e11 g31)
(assert (or (not (or e9 e10 e11 g31)) g26)
;;
(assert (or (not g27) e12 e13)
(assert (or (not (or e12 e13)) g27)
;;
(assert (or (not g28) (and g32 g33))
(assert (or (not (and g32 g33)) g28)
;;
(assert (or (not g29) e22 e23)
(assert (or (not (or e22 e23)) g29)
;;
(assert (or (not g30) e24 e25)
(assert (or (not (or e24 e25)) g30)
;;
(assert (or (not g31) (and g34 g35))
(assert (or (not (and g34 g35)) g31)
;;
(assert (or (not g32) e17 e18 e21)
(assert (or (not (or e17 e18 e21)) g32)
;;
(assert (or (not g33) e19 e20)
(assert (or (not (or e19 e20)) g33)
;;
(assert (or (not g34) e19 e20 e21)
(assert (or (not (or e19 e20 e21)) g34)
;;
(assert (or (not g35) e17 e18)
(assert (or (not (or e17 e18)) g35)
;;
(check-sat)
(get-model)