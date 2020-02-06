 variable
   bool r1,g1,g2,e1,e2,e3,e4,e5;

rule
   (r1==(g1 && g2));
   (g1==(e1 || e2 || e3));
   (g2==(e4 || e5));
