variable
   bool  r1, g1, g2, g3, g4, g5, g6, e1, g7, e2, g8, e3, g9, e4, g10, e5, g11, g12, g13, g14, g15, g16, g17, e6, g18, e11, e7, e8, e9, e10, g19, g20, g21, g22, g23, g24, g25, e12, g26, e13, g27, e14, e15, e16, e17, g28, e18, g29, e19, g30, e20, g31, g32, g33, g34, g35, g36, g37, g38, g39, e21, e22, e25, e26, e29, e30, e23, e27, e31, e24, e28, e32;

rule
   (r1==( 3 == ( g1 + g2 + g3 + g4 + g5 )) );
   (g1==(g6 || e1));
   (g2==(g7 || e2));
   (g3==(g8 || e3));
   (g4==(g9 || e4));
   (g5==(g10 || e5));
   (g6==(g11 && g12));
   (g7==(g13 && g12));
   (g8==(g14 && g12));
   (g9==(g15 && g12));
   (g10==(g16 && g12));
   (g11==(g17 || e6));
   (g12==(g18 || e11));
   (g13==(g17 || e7));
   (g14==(g17 || e8));
   (g15==(g17 || e9));
   (g16==(g17 || e10));
   (g17==( 2 == ( g19 + g20 + g21 )) );
   (g18==( 2 == ( g22 + g23 + g24 )) );
   (g19==(g25 || e12));
   (g20==(g26 || e13));
   (g21==(g27 || e14));
   (g22==(g25 || e15));
   (g23==(g26 || e16));
   (g24==(g27 || e17));
   (g25==(g28 || e18));
   (g26==(g29 || e19));
   (g27==(g30 || e20));
   (g28==( 2 == ( g31 + g32 + g33 )) );
   (g29==( 2 == ( g34 + g35 + g36 )) );
   (g30==( 2 == ( g37 + g38 + g39 )) );
   (g31==(e21 || e22));
   (g32==(e25 || e26));
   (g33==(e29 || e30));
   (g34==(e23 || e22));
   (g35==(e27 || e26));
   (g36==(e31 || e30));
   (g37==(e24 || e22));
   (g38==(e28 || e26));
   (g39==(e32 || e30));
