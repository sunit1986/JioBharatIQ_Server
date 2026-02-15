import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcBurgerMenu = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M4 7h16a1 1 0 100-2H4a1 1 0 000 2zm16 10H4a1 1 0 000 2h16a1 1 0 000-2zm0-6H4a1 1 0 000 2h16a1 1 0 000-2z"
      fill="currentColor"
     />
    </RnSvg>);
};
